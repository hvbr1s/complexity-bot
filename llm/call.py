import os
import math
import json
from dotenv import load_dotenv
from anthropic import AsyncAnthropic
from system.prompt_sol import prepare_sol_prompt, prepare_sol_prompt_manual_only
from system.prompt_evm import prepare_evm_prompt
from system.prompt_move import prepare_move_prompt
from system.prompt_scheduler import prepare_scheduler_prompt

# Load secrets
load_dotenv()

# Set up OpenAI
claude_client = AsyncAnthropic(api_key=os.environ['CLAUDE_API_KEY'])
claude_model_prod = "claude-3-5-sonnet-20240620"

# Function to run the bot on a file and get the complexity score
async def get_complexity_score(file_path, file_info, chain):
    try:
        code = file_info['file_content']
        code_lines = str(file_info['code_lines'])
        comment_lines = str(file_info['comment_lines'])
        # Compute code to comment ratio
        code_to_comment_ratio = math.ceil((int(comment_lines) / int(code_lines)) * 100)
        # Prepare system prompt based on chain
        if chain == "sol":
            system_prompt = await prepare_sol_prompt(file_path, code_lines , file_info['comment_lines'], code_to_comment_ratio, code)
        elif chain == "evm":
            system_prompt= await prepare_evm_prompt(file_path, code_lines , file_info['comment_lines'], code_to_comment_ratio, code)
        elif chain == "move":
            system_prompt= await prepare_move_prompt(file_path, code_lines , file_info['comment_lines'], code_to_comment_ratio, code)

        response = await claude_client.chat.completions.create(
            temperature=0.0,
            model=claude_model_prod,
            messages=[
                {"role": "user", "content": system_prompt}
            ],
        )
        content = response.choices[0].message.content
        parsed_content = json.loads(content)
        score = parsed_content.get("complexity")
        rationale = parsed_content.get("rationale")
        
        if score is not None and rationale is not None:
            print(f'Program {file_path} got assigned a complexity score of {score}. {rationale}')
            return score, rationale, code_lines, code_to_comment_ratio
        else:
            print(f"Couldn't generate complexity info for {file_path}: Missing 'complexity' or 'rationale' in API response")
            return None
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response for {file_path}: {e}")
        return None
    except Exception as e:
        print(f"Failed to generate complexity info for {file_path}: {e}")
        return None

# Function to prepare a schedule
async def schedule(adjusted_time_estimate, report, project_name):
    try:
        system_prompt = await prepare_scheduler_prompt(adjusted_time_estimate, project_name)
        string_report = json.dumps(report)
        response = await claude_client.chat.completions.create(
            temperature=0.0,
            model=claude_model_prod,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": string_report}
            ],
            timeout=60,
        )
        schedule = response.choices[0].message.content
        return schedule
    except Exception as e:
        print(e)
        return("Oops, I wasn't able to schedule this audit")
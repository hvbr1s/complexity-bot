import os
import math
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI
from system.prompt_sol import prepare_sol_prompt
from system.prompt_evm import prepare_evm_prompt

# Load secrets
load_dotenv()

# Set up OpenAI
openai_key = os.environ['OPENAI_API_KEY']
openai_client = AsyncOpenAI(api_key=openai_key)
openai_model_prod = "gpt-4o-2024-08-06"
openai_model_stg = "chatgpt-4o-latest"

# Function to run the bot on a file and get the complexity score
async def get_complexity_score(file_path, file_info, chain):
    try:
        file = file_info['file_content']
        code_lines = str(file_info['code_lines'])
        comment_lines = str(file_info['comment_lines'])
        # Compute code to comment ratio
        code_to_comment_ratio = math.ceil((int(comment_lines) / int(code_lines)) * 100)
        # Prepare system prompt based on chain
        if chain == "sol":
            system_prompt = await prepare_sol_prompt(file_path, code_lines , file_info['comment_lines'], code_to_comment_ratio)
        elif chain == "evm":
            system_prompt= await prepare_evm_prompt(file_path, code_lines , file_info['comment_lines'], code_to_comment_ratio)

        response = await openai_client.chat.completions.create(
            temperature=0.0,
            model=openai_model_prod,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": file}
            ],
            response_format= { "type": "json_object" },
            timeout=60,
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

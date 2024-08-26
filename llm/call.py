import os
import math
import json
import instructor
from pydantic import BaseModel
from dotenv import load_dotenv
from anthropic import AsyncAnthropic
from system.prompt_sol import prepare_sol_prompt, prepare_sol_prompt_manual_only
from system.prompt_evm import prepare_evm_prompt
from system.prompt_move import prepare_move_prompt
from system.prompt_scheduler import prepare_scheduler_prompt

# Load secrets
load_dotenv()

class Complexity(BaseModel):
    complexity: str
    rationale: str

# Set up OpenAI
claude_client = AsyncAnthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
claude_model_prod = "claude-3-5-sonnet-20240620"

# Set up Instructor wrapper:
instructor_client = instructor.from_anthropic(AsyncAnthropic(), mode=instructor.Mode.ANTHROPIC_JSON)

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
            prompt = await prepare_sol_prompt(file_path, code_lines , file_info['comment_lines'], code_to_comment_ratio, code)
            system= "You are an expert security researcher specializing in manual audits and formal verification of Rust-based Solana programs."
        elif chain == "evm":
            prompt= await prepare_evm_prompt(file_path, code_lines , file_info['comment_lines'], code_to_comment_ratio, code)
            system="You are an expert Ethereum smart contract analyzer specializing in security audits and formal verification assessments of Solidity-based smart contracts."
        elif chain == "move":
            prompt= await prepare_move_prompt(file_path, code_lines , file_info['comment_lines'], code_to_comment_ratio, code)
            system="You are an expert Move smart contract analyzer specializing in security audits and formal verification assessments of Move-based smart contracts for the Aptos blockchain."

        response = await instructor_client.messages.create(
            temperature=0.0,
            model=claude_model_prod,
            system=system,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,
            response_model=Complexity    
        )
        
        score = response.complexity
        rationale = response.rationale
        
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
        string_report = json.dumps(report)
        prompt = await prepare_scheduler_prompt(adjusted_time_estimate, project_name, string_report)
        response = await claude_client.messages.create(
            temperature=0.0,
            model=claude_model_prod,
            system="You are an AI assistant specializing in scheduling audits, including formal verification for smart contracts and programs on the Solana and Ethereum blockchains.",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=	8192
        )
        schedule = response.content[0].text
        return schedule
    except Exception as e:
        print(e)
        return("Oops, I wasn't able to schedule this audit")
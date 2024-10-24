import os
import math
import json
import instructor
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic, RateLimitError
from system.prompt_sol import prepare_sol_prompt
from system.prompt_evm import prepare_evm_prompt
from system.prompt_move import prepare_move_prompt
from system.prompt_go import prepare_go_prompt
from system.prompt_ts import prepare_ts_prompt
from system.prompt_scheduler import prepare_scheduler_prompt
from system_fv.prompts import prepare_evm_prompt_fv, prepare_sol_prompt_fv

# Load secrets
load_dotenv()

class Complexity(BaseModel):
    complexity: str
    rationale: str
    purpose: str | None

# Set up clients
claude_client = AsyncAnthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
claude_model_prod = "claude-3-5-sonnet-latest"
openai_client = AsyncOpenAI(api_key=os.environ['OPENAI_API_KEY'])
openai_model_prod = "o1-mini"

# Set up Instructor wrapper:
instructor_client_anthropic = instructor.from_anthropic(AsyncAnthropic(), mode=instructor.Mode.ANTHROPIC_JSON)
instructor_client_openai =  instructor.from_openai(AsyncOpenAI(), mode=instructor.Mode.JSON_O1)

# Function to run the bot on a file and get the complexity score
async def get_complexity_score_manual(file_path, file_info, chain, bot, protocol):
    try:
        code = file_info['file_content']
        code_lines = str(file_info['code_lines'])
        comment_lines = str(file_info['comment_lines'])
        # Compute code to comment ratio
        code_to_comment_ratio = math.ceil((int(comment_lines) / int(code_lines)) * 100)
        # Prepare system prompt based on chain
        if chain == "sol":
            prompt = await prepare_sol_prompt(file_path, code_lines , file_info['comment_lines'], code_to_comment_ratio, code, protocol)
            system= "You are an expert security researcher specializing in manual security audits of Rust-based Solana programs."
        elif chain == "evm":
            prompt= await prepare_evm_prompt(file_path, code_lines , file_info['comment_lines'], code_to_comment_ratio, code, protocol)
            system="You are an expert security researcher specializing in manual security audits of Solidity-based Ethereum smart contracts."
        elif chain == "move":
            prompt= await prepare_move_prompt(file_path, code_lines , file_info['comment_lines'], code_to_comment_ratio, code, protocol)
            system="You are an expert Move smart contract analyzer specializing in security audits and manual review of Move-based smart contracts for the Aptos blockchain."
        elif chain == "go":
            prompt= await prepare_go_prompt(file_path, code_lines , file_info['comment_lines'], code_to_comment_ratio, code, protocol)
            system="You are an expert security researcher specializing in manual audits of Go-based projects intended to interact with the Ethereum ecosystem."
        elif chain == "ts":
            prompt= await prepare_ts_prompt(file_path, code_lines , file_info['comment_lines'], code_to_comment_ratio, code, protocol)
            system="You are an expert security researcher specializing in manual audits of TypeScript-based projects."
        print(f'Conjuring {chain.upper()} bot 🤖')
        
        if bot == "claude":
            try:
                print(f'{bot.upper()} will take a look at {file_path} 🦾')
                response = await instructor_client_anthropic.messages.create(
                    temperature=0.0,
                    model=claude_model_prod,
                    system=system,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1024,
                    response_model=Complexity,
                    max_retries=3   
                )
                score = response.complexity
                rationale = response.rationale
                purpose = response.purpose
            except Exception as e:
                print(f'Claude encountered an issue{e}, trying GPT 🔧')
                response = await instructor_client_openai.chat.completions.create(
                    temperature=0.0,
                    model=openai_model_prod,
                    messages=[
                        #{"role": "system", "content": system},
                        {"role": "user", "content": prompt}
                    ],
                    timeout=60,
                    response_model=Complexity  
                )
                score = response.complexity
                rationale = response.rationale
                purpose = response.purpose
                
            
        elif bot == "gpt":
            try:
                print(f'{bot.upper()} will take a look at {file_path} 🦾')
                response = await instructor_client_openai.chat.completions.create(
                    temperature=0.0,
                    model=openai_model_prod,
                    messages=[
                        #{"role": "system", "content": system},
                        {"role": "user", "content": prompt}
                    ],
                    timeout=60,
                    response_model=Complexity,
                    max_retries=3  
                )
                score = response.complexity
                rationale = response.rationale
                purpose = response.purpose
            except Exception as e:
                print(f'GPT encountered an issue{e}, trying Claude 🔧')
                response = await instructor_client_anthropic.messages.create(
                    temperature=0.0,
                    model=claude_model_prod,
                    system=system,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1024,
                    response_model=Complexity, 
                )
                score = response.complexity
                rationale = response.rationale
                purpose = response.purpose
                
            
        if score is not None and rationale is not None:
            print(f'Program {file_path} got assigned a complexity score of {score}. {rationale}')
            return score, rationale, code_lines, code_to_comment_ratio, purpose
        else:
            print(f"Couldn't generate complexity info for {file_path}: Missing 'complexity' or 'rationale' in API response")
            return None
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response for {file_path}: {e}")
        return None
    except Exception as e:
        print(f"Failed to generate complexity info for {file_path}: {e}")
        return None
    
# Function to run the bot on a file and get the complexity score
async def get_complexity_score_fv(file_path, file_info, chain, bot, protocol):
    try:
        code = file_info['file_content']
        code_lines = str(file_info['code_lines'])
        comment_lines = str(file_info['comment_lines'])
        # Compute code to comment ratio
        code_to_comment_ratio = math.ceil((int(comment_lines) / int(code_lines)) * 100)
        # Prepare system prompt based on chain
        if chain == "sol":
            prompt = await prepare_sol_prompt_fv(file_path, code_lines , file_info['comment_lines'], code_to_comment_ratio, code, protocol)
            system= "You are an expert security engineer specializing in formal verification of Rust-based Solana programs."
        elif chain == "evm":
            prompt= await prepare_evm_prompt_fv(file_path, code_lines , file_info['comment_lines'], code_to_comment_ratio, code, protocol)
            system="You are an expert security engineer specializing in formal verification of Solidity-based Ethereum smart contracts."
        print(f'Conjuring {chain.upper()} FV bot 🧙‍♂️')
        
        if bot == "claude":
            try:
                print(f'{bot.upper()} will take a look at {file_path} 🦾')
                response = await instructor_client_anthropic.messages.create(
                    temperature=0.0,
                    model=claude_model_prod,
                    system=system,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1024,
                    response_model=Complexity,
                    max_retries=3   
                )
                score_fv = response.complexity
                rationale_fv = response.rationale
                
            except Exception as e:
                print(f'Claude encountered an issue{e}, trying GPT 🔧')
                response = await instructor_client_openai.chat.completions.create(
                    temperature=0.0,
                    model=openai_model_prod,
                    messages=[
                        #{"role": "system", "content": system},
                        {"role": "user", "content": prompt}
                    ],
                    timeout=60,
                    response_model=Complexity  
                )
                score_fv = response.complexity
                rationale_fv = response.rationale
                               
        elif bot == "gpt":
            try:
                print(f'{bot.upper()} will take a look at {file_path} 🦾')
                response = await instructor_client_openai.chat.completions.create(
                    temperature=0.0,
                    model=openai_model_prod,
                    messages=[
                        #{"role": "system", "content": system},
                        {"role": "user", "content": prompt}
                    ],
                    timeout=60,
                    response_model=Complexity,
                    max_retries=3  
                )
                score_fv = response.complexity
                rationale_fv = response.rationale
            except Exception as e:
                print(f'GPT encountered an issue{e}, trying Claude 🔧')
                response = await instructor_client_anthropic.messages.create(
                    temperature=0.0,
                    model=claude_model_prod,
                    system=system,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1024,
                    response_model=Complexity, 
                )
                score_fv = response.complexity
                rationale_fv = response.rationale
            
        if score_fv is not None and rationale_fv is not None:
            print(f'Program {file_path} got assigned a complexity score (FV) of {score_fv}. {rationale_fv}')
            return score_fv, rationale_fv
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

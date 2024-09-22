import subprocess
import json
from llm.call import get_complexity_score
from calculate.import_lines import count_import_lines_solidity

# Function to run CLOC on 'docs' directories and get file information
async def get_files_info(language):
    if language == 'evm':
        result = subprocess.run(['cloc', './files', '--json', '--include-lang=Solidity', '--by-file'], capture_output=True, text=True)
    elif language == 'sol':
        result = subprocess.run(['cloc', './files', '--json', '--include-lang=Rust', '--by-file'], capture_output=True, text=True)
    elif language == 'move':
        result = subprocess.run(['cloc', './files', '--json', '--read-lang-def=./lang_files/move_lang_def.txt', '--by-file'], capture_output=True, text=True)
    elif language == 'ts':
        result = subprocess.run(['cloc', './files', '--json', '--include-lang=TypeScript', '--by-file'], capture_output=True, text=True)
    else:
        result = subprocess.run(['cloc', './files', '--json', '--include-lang=Go', '--by-file'], capture_output=True, text=True)
     
    cloc_output = json.loads(result.stdout)
    
    files = {}
    for file_path, file_info in cloc_output.items():
        if file_path != 'header' and file_path != 'SUM':
            
            # Read the file content
            try:
                with open(file_path, 'r') as file:
                    file_content = file.read()
            except IOError as e:
                print(f"Error reading file {file_path}: {e}")
                file_content = ""
            
            # Count import lines
            import_lines = await count_import_lines_solidity(file_content)
            
            files[file_path] = {
                "file_name": file_path,
                "code_lines": file_info.get('code', 0) - int(import_lines),
                "comment_lines": file_info.get('comment', 0),
                "blank_lines": file_info.get('blank', 0),
                "file_content": file_content
            }

    return files

# Function to analyze all project files
async def analyze_contract(LANGUAGE, LLM_ENGINE, PROJECT_NAME):
    files = await get_files_info(language=LANGUAGE)
    results = []
    program_counter = 0
    
    for file_path, file_info in files.items():
        score, rationale, code_lines, code_to_comment_ratio, purpose = await get_complexity_score(file_path, file_info, chain=LANGUAGE, bot=LLM_ENGINE, protocol=PROJECT_NAME.capitalize())
        program_counter += 1
        if score is not None:
            results.append({
                'file': file_path,
                'purpose': purpose,
                'score': score,
                'rationale': rationale,
                'ncloc': code_lines,
                'code to comment ratio': str(code_to_comment_ratio)
            })
            
    print(f'Number of files in this repo: {program_counter}')  
    return results, program_counter
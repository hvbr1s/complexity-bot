import os
import json
import asyncio
import aiofiles
import subprocess
from llm.call import get_complexity_score, schedule
from calculate.summary import calculate_summary_statistics
from calculate.import_lines import count_import_lines_solidity
from calculate.adjusted_time import calculate_adjusted_time_estimate_base, calculate_adjusted_time_estimate_loc_weighted

project = input("👋 Hello there!\nPlease type in the name of the project: ")
PROJECT_NAME = project.strip().lower()
ecosystem = input("👋 Ok!\nWhat ecosystem is the project based on, choose SOL, EVM or GO: ")
language = str(ecosystem.strip().lower())

# Function to run CLOC on 'docs' directories and get Solidity file information
async def get_files_info(language):
    if language == 'evm':
        result = subprocess.run(['cloc', './files', '--json', '--include-lang=Solidity', '--by-file'], capture_output=True, text=True)
    elif language == 'sol':
        result = subprocess.run(['cloc', './files', '--json', '--include-lang=Rust', '--by-file'], capture_output=True, text=True)
    else:
        result = subprocess.run(['cloc', './files', '--json', '--include-lang=Go', '--by-file'], capture_output=True, text=True)
     
    cloc_output = json.loads(result.stdout)
    
    solidity_files = {}
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
            
            solidity_files[file_path] = {
                "file_name": file_path,
                "code_lines": file_info.get('code', 0) - int(import_lines),
                "comment_lines": file_info.get('comment', 0),
                "blank_lines": file_info.get('blank', 0),
                "file_content": file_content
            }

    return solidity_files

# Function to analyze all Solidity files
async def analyze_solidity_contract():
    solidity_files = await get_files_info(language=language)
    results = []
    program_counter = 0
    
    for file_path, file_info in solidity_files.items():
        score, rationale, code_lines, code_to_comment_ratio = await get_complexity_score(file_path, file_info, chain=language)
        program_counter += 1
        if score is not None:
            results.append({
                'file': file_path,
                'score': score,
                'rationale': rationale,
                'cloc': code_lines,
                'code to comment ratio': str(code_to_comment_ratio)
            })
            
    print(f'Number of files in this repo: {program_counter}')  
    return results, program_counter

# Function to save results to a json file
async def save_results(results, output_file):
    async with aiofiles.open(output_file, 'w') as f:
        json_data = {"complexity_report": results}
        await f.write(json.dumps(json_data, indent=2))
        
# Function to save summary to a txt file
async def save_summary(total_cloc, avg_complexity, median_complexity, time_estimate, output_file, program_counter):
    prover_complexity = int(avg_complexity)/2 
    summary = f"""Summary for {PROJECT_NAME.capitalize()}:
Total CLOC: {total_cloc}
Number of files: {program_counter}
Average Complexity Score: {avg_complexity:.2f}/10
Median Complexity Score: {median_complexity:.2f}/10
How complicated is it for the Prover? {str(prover_complexity)}/5 
Estimated Time for Audit and Formal Verification: {time_estimate} week(s)
"""
    async with aiofiles.open(output_file, 'w') as f:
        await f.write(summary)
        
## Main function
async def main():
    
    # Define files 
    output_folder = f'./reports/{PROJECT_NAME}/'
    complexity_report_file = f'{output_folder}{PROJECT_NAME}_complexity_report.json'
    summary_file = f'{output_folder}{PROJECT_NAME}_project_summary.txt'
    output_schedule_file = f"{output_folder}{PROJECT_NAME}_schedule.md"
    
    # Check if the output folder exists, if not create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder} 📁")
    
    print("Analyzing Solidity files...🕵️‍♂️")
    results, program_counter = await analyze_solidity_contract()
    
    await save_results(results, complexity_report_file)
    print(f"Analysis complete. Complexity report saved to {complexity_report_file} 💾✅")
    
    print("Calculating summary statistics...🤔")
    total_cloc, avg_complexity, median_complexity = await calculate_summary_statistics(results)
    
    # Calculate adjusted time estimate
    adjusted_time_estimate = await calculate_adjusted_time_estimate_base(total_cloc, avg_complexity)

    await save_summary(total_cloc, avg_complexity, median_complexity, adjusted_time_estimate, summary_file, program_counter)
    print(f"Project summary saved to {summary_file} 💾✅")
    
    print("Preparing schedule...🗓️")
    with open(complexity_report_file, 'r') as file:
        report = json.load(file)
    schedule_result = await schedule(adjusted_time_estimate, report, PROJECT_NAME.capitalize())
    with open(output_schedule_file, 'w') as md_file:
        md_file.write(schedule_result)
    print(f"Schedule has been written to {output_schedule_file}💾✅")
    
    print(f"Estimated time for audit and formal verification: {adjusted_time_estimate} week(s) 🗓️✅")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
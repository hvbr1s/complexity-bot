import os
import json
import asyncio
import statistics
import aiofiles
import subprocess
from llm.call import get_complexity_score
from calculate.adjusted_time import calculate_adjusted_time_estimate_base, calculate_adjusted_time_estimate_loc_weighted

# Function to run CLOC on 'docs' directories and get Rust file information
async def get_rust_files_info():
    result = subprocess.run(['cloc', './docs', '--json', '--include-lang=Solidity', '--by-file'], capture_output=True, text=True)
    cloc_output = json.loads(result.stdout)
    
    rust_files = {}
    for file_path, file_info in cloc_output.items():
        if file_path != 'header' and file_path != 'SUM':
            
            # Read the file content
            try:
                with open(file_path, 'r') as file:
                    file_content = file.read()
            except IOError as e:
                print(f"Error reading file {file_path}: {e}")
                file_content = ""
            
            rust_files[file_path] = {
                "file_name": file_path,
                "code_lines": file_info.get('code', 0),
                "comment_lines": file_info.get('comment', 0),
                "blank_lines": file_info.get('blank', 0),
                "file_content": file_content
            }

    return rust_files

# Function to analyze all Rust files
async def analyze_rust_programs():
    rust_files = await get_rust_files_info()
    results = []
    program_counter = 0
    
    for file_path, file_info in rust_files.items():
        score, rationale, code_lines, code_to_comment_ratio = await get_complexity_score(file_path, file_info, chain="evm")
        program_counter += 1
        if score is not None:
            results.append({
                'file': file_path,
                'score': score,
                'rationale': rationale,
                'cloc': code_lines,
                'code to comment ratio': str(code_to_comment_ratio)
            })
            
    print(f'Number of programs in this repo: {program_counter}')  
    return results, program_counter

# Function to save results to a json file
async def save_results(results, output_file):
    async with aiofiles.open(output_file, 'w') as f:
        json_data = {"complexity_report": results}
        await f.write(json.dumps(json_data, indent=2))
        
# Function to calculate summary statistics
async def calculate_summary(results):
    total_cloc = sum(int(result['cloc']) for result in results)
    complexity_scores = [float(result['score']) for result in results]
    avg_complexity = statistics.mean(complexity_scores)
    median_complexity = statistics.median(complexity_scores)
    return total_cloc, avg_complexity, median_complexity

# Function to save summary to a txt file
async def save_summary(total_cloc, avg_complexity, median_complexity, time_estimate, output_file, program_counter):
    summary = f"""Project Summary:
Total CLOC: {total_cloc}
Number of files: {program_counter}
Average Complexity Score: {avg_complexity:.2f}
Median Complexity Score: {median_complexity:.2f}
Estimated Time for Audit and Formal Verification: {time_estimate} week(s)
"""
    async with aiofiles.open(output_file, 'w') as f:
        await f.write(summary)
        
## Main function
async def main():
    output_folder = './output'
    complexity_report_file = f'{output_folder}/evm_complexity_report.json'
    summary_file = './output/evm_project_summary.txt'
    
    # Check if the output folder exists, if not create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder} 📁")
    
    print("Analyzing Solidity files...🕵️‍♂️")
    results, program_counter = await analyze_rust_programs()
    
    print("Saving complexity report...💾")
    await save_results(results, complexity_report_file)
    
    print("Calculating summary statistics...🤔")
    total_cloc, avg_complexity, median_complexity = await calculate_summary(results)
    
    # Calculate adjusted time estimate
    adjusted_time_estimate = await calculate_adjusted_time_estimate_loc_weighted(total_cloc, avg_complexity)
    
    print("Saving project summary...💾")
    await save_summary(total_cloc, avg_complexity, median_complexity, adjusted_time_estimate, summary_file, program_counter)
    
    print(f"Analysis complete. Complexity report saved to {complexity_report_file} 💾")
    print(f"Project summary saved to {summary_file} 💾")
    print(f"Estimated time for audit and formal verification: {adjusted_time_estimate} week(s) 🗓️")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())

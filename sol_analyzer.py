import os
import json
import math
import asyncio
import statistics
import aiofiles
import subprocess
from llm.call import get_complexity_score

# Function to run CLOC on 'docs' directories and get Rust file information
async def get_rust_files_info():
    result = subprocess.run(['cloc', './docs', '--json', '--include-lang=Rust', '--by-file'], capture_output=True, text=True)
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
        score, rationale, code_lines, code_to_comment_ratio = await get_complexity_score(file_path, file_info, chain="sol")
        program_counter += 1
        if score is not None:
            results.append({
                'file': file_path,
                'score': score,
                'rationale': rationale,
                'cloc': code_lines,
                'code to comment percent ratio': str(code_to_comment_ratio)
            })
            
    print(f'Number of files in this repo: {program_counter} 📁')  
    return results, program_counter

# Function to save results to a json file
async def save_results(results, output_file):
    async with aiofiles.open(output_file, 'w') as f:
        json_data = {"complexity_report": results}
        await f.write(json.dumps(json_data, indent=2))
        
async def calculate_adjusted_time_estimate(total_loc, avg_complexity):
    """
    Calculate the adjusted time estimate based on lines of code (LOC) and average complexity.

    Steps:
    1. Start with the base estimate of 1 week per 1000 lines of code.
    2. Apply a complexity multiplier based on the average complexity score:
        - For low complexity (1-3), reduce the estimate by 20%.
        - For medium complexity (4-7), apply a linear adjustment, increasing or decreasing the estimate by up to 20%.
        - For high complexity (8-10), increase the estimate more significantly, up to 110% more for a complexity of 10.
    3. Multiply the base estimate by this complexity multiplier.
    4. Round up to the nearest whole week.
    """
    
    # Step 1: Calculate the base estimate (in weeks)
    base_estimate_weeks = total_loc / 1000
    print(f'Base estimate weeks: {base_estimate_weeks}')
    
    # Step 2: Determine the complexity multiplier
    if avg_complexity <= 3:
        # Low complexity: reduce time by 20%
        complexity_multiplier = 0.8
    elif 3 < avg_complexity <= 7:
        # Medium complexity: linear adjustment
        complexity_multiplier = 1 + (avg_complexity - 5) * 0.1
    else:
        # High complexity: significant increase
        complexity_multiplier = 1.5 + (avg_complexity - 7) * 0.2
    
    # Step 3: Adjust the base estimate with the complexity multiplier
    adjusted_estimate_weeks = base_estimate_weeks * complexity_multiplier
    
    # Step 4: Round up to the nearest whole week
    return math.ceil(adjusted_estimate_weeks)

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
    complexity_report_file = f'{output_folder}/sol_complexity_report.json'
    summary_file = './output/sol_project_summary.txt'
    
    # Check if the output folder exists, if not create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder} 📁")
    
    print("Analyzing Rust files...🕵️‍♂️")
    results, program_counter = await analyze_rust_programs()
    
    print("Saving complexity report...💾")
    await save_results(results, complexity_report_file)
    
    print("Calculating summary statistics...🤔")
    total_cloc, avg_complexity, median_complexity = await calculate_summary(results)
    
    # Calculate adjusted time estimate
    adjusted_time_estimate = await calculate_adjusted_time_estimate(total_cloc, avg_complexity)
    
    print("Saving project summary...💾")
    await save_summary(total_cloc, avg_complexity, median_complexity, adjusted_time_estimate, summary_file, program_counter)
    
    print(f"Analysis complete. Complexity report saved to {complexity_report_file} 💾")
    print(f"Project summary saved to {summary_file} 💾")
    print(f"Estimated time for audit and formal verification: {adjusted_time_estimate} week(s) 🗓️")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
    
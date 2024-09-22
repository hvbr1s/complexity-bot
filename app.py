import os
import json
import asyncio
from llm.call import schedule
from llm.analyze import analyze_contract
from utils.save import save_results, save_summary
from calculate.summary import calculate_summary_statistics
from calculate.adjusted_time import calculate_adjusted_time_estimate_base, calculate_adjusted_time_estimate_loc_weighted

# User input

PROJECT_NAME = input("👋 Welcome! Please enter the project name: ").strip().lower()

while True:
    LLM_ENGINE = input("🤖 Should we analyze it using Claude or GPT? (CLAUDE/GPT): ").strip().lower()
    if LLM_ENGINE in ["claude", "gpt"]:
        break
    else:
        print("❌ Invalid input. Please choose CLAUDE or GPT.")

while True:
    ecosystem = input("🌐 Great! Which ecosystem is the project based on? (SOL/EVM/MOVE/GO/TS): ").strip().lower()
    if ecosystem in ["sol", "evm", "move", "go", "ts"]:
        LANGUAGE = ecosystem
        break
    else:
        print("❌ Invalid input. Please choose SOL, EVM, MOVE, TS or GO.")
        
print(f"🚀 Excellent! Let's use {LLM_ENGINE.capitalize()} to analyze {PROJECT_NAME.capitalize()} built on the {LANGUAGE.upper()} ecosystem.")

   
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
    
    print("Analyzing files...🕵️‍♂️")
    results, program_counter = await analyze_contract(LANGUAGE, LLM_ENGINE, PROJECT_NAME)
    
    await save_results(results, complexity_report_file)
    print(f"Analysis complete. Complexity report saved to {complexity_report_file} 💾✅")
    
    print("Calculating summary statistics...🤔")
    total_cloc, avg_complexity, median_complexity = await calculate_summary_statistics(results)
    
    # Calculate adjusted time estimate
    adjusted_time_estimate = await calculate_adjusted_time_estimate_base(total_cloc, avg_complexity, LANGUAGE)

    await save_summary(total_cloc, avg_complexity, median_complexity, adjusted_time_estimate, summary_file, program_counter, PROJECT_NAME)
    print(f"Project summary saved to {summary_file} 💾✅")
    
    print("Preparing schedule...🗓️")
    with open(complexity_report_file, 'r') as file:
        report = json.load(file)
    schedule_result = await schedule(adjusted_time_estimate, report, PROJECT_NAME.capitalize())
    with open(output_schedule_file, 'w') as md_file:
        md_file.write(schedule_result)
    print(f"Schedule has been written to {output_schedule_file}💾✅")
    
    print(f"Estimated time for audit: {adjusted_time_estimate} week(s) 🗓️✅")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())

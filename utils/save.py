import aiofiles
import json

# Function to save results to a json file
async def save_results(results, output_file):
    async with aiofiles.open(output_file, 'w') as f:
        json_data = {"complexity_report": results}
        await f.write(json.dumps(json_data, indent=2))
        
# Function to save summary to a txt file
async def save_summary(total_cloc, avg_complexity, avg_complexity_fv, median_complexity, time_estimate, output_file, program_counter, PROJECT_NAME):
    prover_complexity = int(avg_complexity_fv)/2 
    summary = f"""Summary for {PROJECT_NAME.capitalize()}:
Total nCLOC: {total_cloc}
Number of files: {program_counter}
Average Complexity Score: {avg_complexity:.2f}/10
Median Complexity Score: {median_complexity:.2f}/10
How complicated is it for the Prover? {str(prover_complexity)}/5 
Estimated Time for Audit: {time_estimate} week(s)
"""
    async with aiofiles.open(output_file, 'w') as f:
        await f.write(summary)
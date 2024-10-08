async def prepare_scheduler_prompt(adjusted_time_estimate, project_name, report):
    try:
        SCHEDULER = f'''     
Your task is to analyze the provided JSON report and create a comprehensive audit schedule for the {project_name} project. The schedule should cover {adjusted_time_estimate} business weeks (Monday to Friday).

Here is the JSON report containing entries for each file to be audited:
<json_report>
{report}
</json_report>
Follow these steps to create the audit schedule:

1. Analyze the JSON report:
   - Review each file's complexity score, lines of code (cloc), and code-to-comment ratio.
   - Consider the rationale provided for each complexity score.

2. Prioritize files:
   - Group similar files or those with dependencies for efficient auditing.
   - Prioritize files with higher complexity scores or larger code bases.

3. Allocate time:
   - Estimate time requirements based on complexity score, lines of code, and code-to-comment ratio.
   - Ensure a balanced workload across the weeks to maintain consistent progress.

4. Create the schedule:
   - Begin Week 1 with a 1-hour 'Project kick-off' on Monday.
   - Include time for documentation and team meetings throughout the schedule.
   - Add a weekly 1-hour progress review session between the {project_name} team and the Certora team, except for Week 1 and the final week.
   - End the final week with a 2-hour 'Wrap-up meeting and report Review' on Friday.

5. Review and adjust:
   - Ensure all files are accounted for in the schedule.
   - Check that the workload is balanced and realistic.

Present your schedule in a clear, organized manner using markdown formatting. Use tables, lists, and headers to improve readability. Your response should include:

<response>
1. A brief introduction explaining the audit schedule for {project_name}.

2. Weekly Overview:
   - Use a markdown table to summarize the focus of each week.

3. Detailed Schedule:
   - For each week, create a subsection with a daily breakdown.
   - Use markdown lists to detail the files to be audited each day, including estimated time and rationale.

4. Prioritization Explanation:
   - Provide a brief explanation of your prioritization strategy.

5. Conclusion:
   - Summarize the key points of the audit schedule.
</response>

Remember to think step-by-step and consider all the provided information when creating the schedule. Begin your response now.
        '''     
        return SCHEDULER
     
    except Exception as e:
        print(e)
        error =  {
           "error": "Something went wrong, I wasn't able to schedule the audit, please try again"
        }
        return error
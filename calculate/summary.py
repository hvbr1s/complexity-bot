import statistics

# Function to calculate summary statistics
async def calculate_summary_statistics(results):
    total_cloc = sum(int(result['ncloc']) for result in results)
    complexity_scores = [float(result['score']) for result in results]
    complexity_scores_fv = [float(result['score_fv']) for result in results]
    avg_complexity = statistics.mean(complexity_scores)
    median_complexity = statistics.median(complexity_scores)
    avg_complexity_fv = statistics.mean(complexity_scores_fv)
    median_complexity_fv = statistics.median(complexity_scores_fv)
    return total_cloc, avg_complexity, median_complexity, avg_complexity_fv, median_complexity_fv
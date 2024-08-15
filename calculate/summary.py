import statistics

# Function to calculate summary statistics
async def calculate_summary_statistics(results):
    total_cloc = sum(int(result['cloc']) for result in results)
    complexity_scores = [float(result['score']) for result in results]
    avg_complexity = statistics.mean(complexity_scores)
    median_complexity = statistics.median(complexity_scores)
    return total_cloc, avg_complexity, median_complexity
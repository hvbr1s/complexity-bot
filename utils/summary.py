import statistics

# Function to calculate summary statistics
async def calculate_summary_statistics(results):
    try:
        print(results)
        # Extract complexity scores, using 0 if 'score' key is missing
        complexity_scores = [float(result.get('score_manual', 0)) for result in results]
        
        # Calculate total lines of code, using 0 if 'code_lines' key is missing
        total_cloc = sum(int(result.get('ncloc', 0)) for result in results)
        
        # Calculate average complexity
        avg_complexity = sum(complexity_scores) / len(complexity_scores) if complexity_scores else 0
        
        # Calculate median complexity
        sorted_scores = sorted(complexity_scores)
        mid = len(sorted_scores) // 2
        median_complexity = (sorted_scores[mid] if len(sorted_scores) % 2 != 0 else (sorted_scores[mid - 1] + sorted_scores[mid]) / 2) if sorted_scores else 0
        
        # Extract formal verification complexity scores, using 0 if 'score_fv' key is missing
        complexity_scores_fv = [float(result.get('score_fv', 0)) for result in results]
        
        # Calculate average formal verification complexity
        avg_complexity_fv = sum(complexity_scores_fv) / len(complexity_scores_fv) if complexity_scores_fv else 0
        
        return total_cloc, avg_complexity, median_complexity, avg_complexity_fv
    except Exception as e:
        print(f"Error calculating summary statistics: {e}")
        return 0, 0, 0, 0
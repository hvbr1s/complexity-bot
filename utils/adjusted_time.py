import math

async def calculate_adjusted_time_estimate_base(total_loc, avg_complexity, avg_complexity_fv, language):
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
    
    # Step 0: Average manual and fv complexity
    adjusted_complexity = (avg_complexity + avg_complexity_fv) / 2
    
    # Step 1: Calculate the base estimate (in weeks)
    if language == 'ts':
        base_estimate_weeks = total_loc / 2000
    else:
        base_estimate_weeks = total_loc / 1000
    print(f'Base estimate weeks: {base_estimate_weeks}')
    
    # Step 2: Determine the complexity multiplier
    if avg_complexity <= 3:
        # Low complexity: reduce time by 20%
        complexity_multiplier = 0.8
    elif 3 < avg_complexity <= 7:
        # Medium complexity: linear adjustment
        complexity_multiplier = 1 + (adjusted_complexity - 5) * 0.1
    else:
        # High complexity: significant increase
        complexity_multiplier = 1.5 + (adjusted_complexity - 7) * 0.2
    
    # Step 3: Adjust the base estimate with the complexity multiplier
    adjusted_estimate_weeks = base_estimate_weeks * complexity_multiplier
    
    # Step 4: adjust estimation for large but simple code bases
    if total_loc >= 1000 and adjusted_estimate_weeks <= 1:
        adjusted_estimate_weeks += 1 
    if total_loc <= 1000 and adjusted_estimate_weeks <= 1:
        adjusted_estimate_weeks = 1
    print(f'Adjusted estimate weeks: {adjusted_estimate_weeks}')
    # Step 5: Round up to the nearest whole week
    return math.ceil(adjusted_estimate_weeks)


async def calculate_adjusted_time_estimate_loc_weighted(total_loc, avg_complexity):
    """
    Calculate the adjusted time estimate based on lines of code (LOC) and average complexity.

    Steps:
    1. Start with the base estimate of 1 week per 1000 lines of code.
    2. Apply a LOC multiplier that scales based on specific LOC ranges.
    3. Apply a complexity multiplier based on the average complexity score.
    4. Combine the LOC and complexity multipliers to get the final estimate.
    5. Round up to the nearest whole week.
    """
    
    # Step 1: Calculate the base estimate (in weeks)
    base_estimate_weeks = total_loc / 1000
    
    # Step 2: Calculate the LOC multiplier
    if total_loc < 500:
        loc_multiplier = 0.7  # -30%
    elif total_loc < 2000:
        loc_multiplier = 0.7  # -30%
    elif total_loc < 4000:
        loc_multiplier = 0.8  # -20%
    elif total_loc < 6000:
        loc_multiplier = 0.9  # -10%
    elif total_loc < 10000:
        loc_multiplier = 1.0  # 0%
    elif total_loc < 12000:
        loc_multiplier = 1.1  # +10%
    elif total_loc < 14000:
        loc_multiplier = 1.2  # +20%
    else:
        loc_multiplier = 1.3  # +30%
    
    # Step 3: Determine the complexity multiplier
    if avg_complexity <= 3:
        complexity_multiplier = 0.8
    elif 3 < avg_complexity <= 7:
        complexity_multiplier = 1 + (avg_complexity - 5) * 0.1
    else:
        complexity_multiplier = 1.5 + (avg_complexity - 7) * 0.2
    
    # Step 4: Combine multipliers and apply to base estimate
    adjusted_estimate_weeks = base_estimate_weeks * loc_multiplier * complexity_multiplier
    
    # Step 5: adjust estimation for large but simple code bases
    if total_loc >= 1000 and adjusted_estimate_weeks <= 1:
        adjusted_estimate_weeks += 1 
    
    # Step 5: Round up to the nearest whole week
    return math.floor(adjusted_estimate_weeks)
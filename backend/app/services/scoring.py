from typing import Optional


def calculate_points(
    bet_home: int,
    bet_away: int,
    actual_home: int,
    actual_away: int
) -> int:
    """
    Calculate points based on betting rules:
    - Exact score: 7 points
    - Correct winner: 5 points
    - Correct draw: 3 points
    - Wrong: 0 points
    
    Args:
        bet_home: Predicted home team score
        bet_away: Predicted away team score
        actual_home: Actual home team score
        actual_away: Actual away team score
    
    Returns:
        Points earned (0, 3, 5, or 7)
    """
    # Exact score match
    if bet_home == actual_home and bet_away == actual_away:
        return 7
    
    # Determine actual result
    if actual_home > actual_away:
        actual_result = 'CASA'
    elif actual_home < actual_away:
        actual_result = 'FORA'
    else:
        actual_result = 'EMPATE'
    
    # Determine bet result
    if bet_home > bet_away:
        bet_result = 'CASA'
    elif bet_home < bet_away:
        bet_result = 'FORA'
    else:
        bet_result = 'EMPATE'
    
    # Correct winner or draw
    if bet_result == actual_result:
        # Draw gets 3 points, winner gets 5 points
        return 3 if actual_result == 'EMPATE' else 5
    
    return 0


def calculate_score_difference(
    bet_home: int,
    bet_away: int,
    actual_home: int,
    actual_away: int
) -> float:
    """
    Calculate the absolute difference between predicted and actual scores.
    Used for tiebreaker (closest to last match score).
    
    Args:
        bet_home: Predicted home team score
        bet_away: Predicted away team score
        actual_home: Actual home team score
        actual_away: Actual away team score
    
    Returns:
        Sum of absolute differences
    """
    home_diff = abs(bet_home - actual_home)
    away_diff = abs(bet_away - actual_away)
    return float(home_diff + away_diff)


def validate_bet_timing(match_date, current_date) -> bool:
    """
    Check if bet can be placed (before match starts).
    
    Args:
        match_date: Match start datetime
        current_date: Current datetime
    
    Returns:
        True if bet can be placed, False otherwise
    """
    return current_date < match_date

# Made with Bob

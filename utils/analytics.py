from datetime import datetime

def detect_stagnation(weights):
    """Returns True if last 3 weights are the same"""
    if len(weights) >= 3:
        return weights[-1] == weights[-2] == weights[-3]
    return False

def calculate_streak(dates):
    """Calculates consecutive days streak"""
    if not dates:
        return 0
    dates = sorted(dates, reverse=True)
    streak = 1
    for i in range(len(dates)-1):
        diff = (datetime.strptime(dates[i], "%Y-%m-%d") -
                datetime.strptime(dates[i+1], "%Y-%m-%d")).days
        if diff == 1:
            streak += 1
        else:
            break
    return streak
# utils.py
import pandas as pd
from datetime import datetime, timedelta

def calculate_streak(dates):
    """Calculate current streak from list of dates"""
    if not dates:
        return 0
    
    sorted_dates = sorted(dates, reverse=True)
    streak = 1
    current_date = sorted_dates[0]
    
    for date in sorted_dates[1:]:
        if (current_date - date).days == 1:
            streak += 1
            current_date = date
        else:
            break
    
    return streak

def get_mood_trend(mood_history, days=7):
    """Get mood trend for last N days"""
    if not mood_history:
        return "neutral"
    
    recent = mood_history[-days:]
    avg_score = sum(m['score'] for m in recent) / len(recent)
    
    if avg_score >= 70:
        return "improving"
    elif avg_score >= 40:
        return "stable"
    else:
        return "declining"

def format_habit_report(habits):
    """Generate habit completion report"""
    completed = sum(1 for h in habits.values() if h['completed'])
    total = len(habits)
    return f"{completed}/{total} habits completed today"
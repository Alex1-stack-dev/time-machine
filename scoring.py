def calculate_team_scores(events, user_preferences):
    team_scores = {}
    for event in events:
        for team, score in event["results"].items():
            weighted_score = score * user_preferences.get(event["type"], 1)
            team_scores[team] = team_scores.get(team, 0) + weighted_score
    return team_scores

# Usage after event completion
events = [
    # Each event should have a "results" dict mapping team names to scores
    {"type": "race", "results": {"TeamA": 10, "TeamB": 8}},
    {"type": "quiz", "results": {"TeamA": 5, "TeamB": 10}},
]
user_preferences = {"race": 2, "quiz": 1}  # Example: user wants race weighted more
final_scores = calculate_team_scores(events, user_preferences)
print("Final Team Scores:", final_scores)

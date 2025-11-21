import os
import json

def create_analysis_files(app):
    analysis_path = "analysis/response_time.json"
    stats_path = "analysis/stats.json"
    if os.path.exists(analysis_path):
        with open(analysis_path, "r") as f:
            app.state.response_bot_time = json.load(f)
    else:
        app.state.response_bot_time = []
    if os.path.exists(stats_path):
        with open(stats_path, "r") as f:
            app.state.stats = json.load(f)
    else:
        app.state.stats = []

def save_data(app, phase, duration_time, stats_data, bot_name):
    response_info = {
            "phase": phase,
            "time": duration_time,
            "botName": bot_name,
    }
    app.state.response_bot_time.append(response_info)
    app.state.stats.append(stats_data)
    with open("analysis/response_time.json", "w") as rf:
        json.dump(app.state.response_bot_time, rf, indent=4)
    with open("analysis/stats.json", "w") as sf:
        json.dump(app.state.stats, sf, indent=4)
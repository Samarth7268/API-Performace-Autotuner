import json, math, os, random
from pathlib import Path

STATE_FILE = Path(__file__).parent / "tuner_state.json"

# Candidate configurations
CONFIGS = [
    {"users": 5, "spawn": 2},
    {"users": 10, "spawn": 5},
    {"users": 20, "spawn": 5},
    {"users": 30, "spawn": 10}
]

# Initialize state if missing
def _init_state():
    data = {}
    for i, cfg in enumerate(CONFIGS):
        data[str(i)] = {
            "config": cfg,
            "trials": 0,
            "total_reward": 0.0
        }
    save_state(data)
    return data


def load_state():
    if not STATE_FILE.exists():
        return _init_state()
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


# -------- BANDIT LOGIC -------- #

def select_config():
    state = load_state()
    total_trials = sum(v["trials"] for v in state.values())

    # If any config never tried, explore it first
    for k, v in state.items():
        if v["trials"] == 0:
            return k, v["config"]

    # Compute UCB score
    best_score = -1
    selected = None

    for k, v in state.items():
        avg = v["total_reward"] / v["trials"]
        bonus = math.sqrt((2 * math.log(total_trials)) / v["trials"])
        ucb = avg + bonus

        if ucb > best_score:
            best_score = ucb
            selected = k

    return selected, state[selected]["config"]


def update_reward(key, reward):
    state = load_state()
    state[key]["trials"] += 1
    state[key]["total_reward"] += reward
    save_state(state)


def get_tuner_report():
    state = load_state()
    trials = []

    for k, v in state.items():
        avg = v["total_reward"] / v["trials"] if v["trials"] else 0
        trials.append({
            "users": v["config"]["users"],
            "spawn": v["config"]["spawn"],
            "runs": v["trials"],
            "avg_score": round(avg, 2)
        })

    best = max(trials, key=lambda x: x["avg_score"], default=None)

    return {
        "best": best,
        "trials": trials
    }

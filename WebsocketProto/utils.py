import json
from pathlib import Path

LOCK_FILE = Path("lock_state.json")

def load_lock_states():
    if LOCK_FILE.exists():
        with open(LOCK_FILE, "r") as f:
            return json.load(f)
    return {}

def save_lock_states(states):
    with open(LOCK_FILE, "w") as f:
        json.dump(states, f, indent=4)

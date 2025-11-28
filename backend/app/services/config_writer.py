import json, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CFG = os.path.join(BASE_DIR, "runtime_config.json")

DEFAULT = {
  "workers": 1,
  "users": 20,
  "spawn_rate": 5,
  "keepalive": 5,
  "timeouts": 30
}

def get_config():
    if not os.path.exists(CFG):
        save_config(DEFAULT)
    with open(CFG, "r") as f:
        return json.load(f)

def save_config(cfg):
    with open(CFG, "w") as f:
        json.dump(cfg, f, indent=2)
    return cfg

def patch(update: dict):
    cfg = get_config()
    cfg.update(update)
    return save_config(cfg)

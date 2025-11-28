import os
from pathlib import Path


class Config:
    # Project root
    BASE_DIR = Path(__file__).resolve().parent

    # App metadata
    APP_NAME = "API Performance Autotuner"
    VERSION = "1.0.0"

    # Locust fallback (if manual)
    LOCUST_FILE = Path(os.getenv("LOCUST_FILE", BASE_DIR / "utils" / "locustfile.py"))

    # Profiling output
    TEMP_DIR = Path(os.getenv("TEMP", BASE_DIR / "tmp"))
    PROFILER_OUTPUT = Path(os.getenv("PROFILER_OUTPUT", TEMP_DIR))

    # Reports storage
    REPORTS_DIR = Path(os.getenv("REPORTS_DIR", BASE_DIR / "reports"))

    # Redis (future async mode)
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

    # AI Agent (Ollama)
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
    OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "90"))

    def init(self):
        self.PROFILER_OUTPUT.mkdir(parents=True, exist_ok=True)
        self.REPORTS_DIR.mkdir(parents=True, exist_ok=True)


config = Config()
config.init()

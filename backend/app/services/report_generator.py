import json
import uuid
from datetime import datetime
from pathlib import Path

from app.config import config
from app.utils.parser import sanitize_metrics

REPORT_DIR = Path(config.REPORTS_DIR)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------
# CLASSIFIER
# ------------------------------------------------------
def classify_performance(p95, error_rate):
    if error_rate is None:
        return "UNKNOWN"
    if error_rate > 0.05:
        return "CRITICAL"
    if p95 > 800:
        return "VERY SLOW"
    if p95 > 400:
        return "SLOW"
    if p95 > 250:
        return "WARNING"
    return "HEALTHY"


# ------------------------------------------------------
# SUMMARY GENERATOR
# ------------------------------------------------------
def generate_summary(status, p95, error_rate, rps):
    return (
        f"System status: {status}. "
        f"P95 latency = {p95} ms. "
        f"Error rate = {round(error_rate * 100, 2)}%. "
        f"Throughput = {rps} rps."
    )


# ------------------------------------------------------
# REPORT BUILDER
# ------------------------------------------------------
def generate_report(load_metrics, profile_metrics):
    # Clean metrics
    load_metrics = sanitize_metrics(load_metrics)
    profile_metrics = sanitize_metrics(profile_metrics)

    p95 = float(load_metrics.get("p95_latency", 0))
    error_rate = float(load_metrics.get("error_rate", 0))
    rps = float(load_metrics.get("rps", 0))

    status = classify_performance(p95, error_rate)
    summary = generate_summary(status, p95, error_rate, rps)

    report = {
        "id": str(uuid.uuid4()),
        "generated_at": datetime.utcnow().isoformat(),
        "health_status": status,
        "summary": summary,
        "load_metrics": load_metrics,
        "profile_metrics": profile_metrics,

        # ✅ Always exist so frontend never crashes
        "ai_advice": [],
        "auto_tuning": {},
        "score": 0,
        "tuner_config": {},
        "tuner_report": {}
    }

    return report


# ------------------------------------------------------
# SAVE REPORT
# ------------------------------------------------------
def save_report(report):
    path = REPORT_DIR / f"{report['id']}.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return {
        "report_id": report["id"],
        "file_path": str(path)
    }


# ------------------------------------------------------
# FETCH REPORT
# ------------------------------------------------------
def get_report(report_id):
    path = REPORT_DIR / f"{report_id}.json"
    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

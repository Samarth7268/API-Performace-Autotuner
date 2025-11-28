import subprocess
import tempfile
import os
import csv
from urllib.parse import urlparse
import glob
import time


def run_load_test(request):
    url = str(request.url)
    users = request.users
    spawn_rate = request.spawn_rate
    runtime = request.runtime

    parsed = urlparse(url)
    host = f"{parsed.scheme}://{parsed.netloc}"
    path = parsed.path if parsed.path else "/"

    locust_code = f"""
from locust import HttpUser, task, between

class LoadTestUser(HttpUser):
    wait_time = between(1, 2)
    host = "{host}"

    @task
    def hit_api(self):
        self.client.get("{path}")
"""

    # ---- TEMP DIR FOR CSV ----
    workdir = tempfile.mkdtemp(prefix="locust_")
    locust_file_path = os.path.join(workdir, "locustfile.py")
    csv_prefix = os.path.join(workdir, "stats")

    with open(locust_file_path, "w", encoding="utf-8") as f:
        f.write(locust_code)

    cmd = [
        "locust",
        "-f", locust_file_path,
        "--headless",
        "-u", str(users),
        "-r", str(spawn_rate),
        "--run-time", f"{runtime}s",
        "--csv", csv_prefix,
        "--csv-full-history",
        "--only-summary"
    ]

    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    time.sleep(1)

    stats_file = f"{csv_prefix}_stats_requests.csv"

    # ---- PARSE CSV IF EXISTS ----
    if os.path.exists(stats_file):
        metrics = _parse_locust_csv(stats_file)
        _cleanup(workdir)
        if metrics:
            return metrics

    # ---- FALLBACK PARSER FOR WINDOWS ----
    fallback = _parse_from_stdout(process.stderr + "\n" + process.stdout)
    _cleanup(workdir)

    if fallback:
        return fallback

    return {
        "error": "Locust ran but metrics could not be parsed",
        "stdout": process.stdout,
        "stderr": process.stderr,
        "workdir": workdir,
        "host": host,
        "path": path
    }


def _parse_locust_csv(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("Name") in ("Aggregated", "Total"):
                    req = float(row.get("Request Count", 0))
                    fail = float(row.get("Failure Count", 0))
                    avg = float(row.get("Average Response Time", 0))
                    return {
                        "median_latency": float(row.get("Median Response Time", 0)),
                        "p95_latency": float(row.get("95%", 0)),
                        "p99_latency": float(row.get("99%", 0)),
                        "rps": float(row.get("Requests/s", 0)),
                        "error_rate": fail / max(1, req),
                        "throughput": (float(row.get("Requests/s", 0)) * avg) / 1000
                    }
    except:
        return {}
    return {}


def _parse_from_stdout(text):
    import re

    # ✅ Parse Aggregated summary row
    m = re.search(
        r"Aggregated\s+(\d+)\s+\d+\(\d+\.\d+%\)\s+\|\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+\|\s+([\d.]+)",
        text
    )

    if not m:
        return {}

    reqs = int(m.group(1))
    avg = float(m.group(2))
    min_ = float(m.group(3))
    max_ = float(m.group(4))
    median = float(m.group(5))
    rps = float(m.group(6))

    def find_pct(label):
        p = re.search(rf"{label}\s+(\d+)", text)
        return float(p.group(1)) if p else median

    p95 = find_pct("95%")
    p99 = find_pct("99%")

    return {
        "median_latency": median,
        "p95_latency": p95,
        "p99_latency": p99,
        "rps": rps,
        "error_rate": 0.0,
        "throughput": (rps * avg) / 1000
    }


def _cleanup(workdir):
    try:
        for f in glob.glob(os.path.join(workdir, "*")):
            os.remove(f)
        os.rmdir(workdir)
    except:
        pass

import os
import subprocess
import tempfile
from app.utils.flamegraph_helper import extract_hotspots


def run_profiler():
    pid = os.getpid()
    svg_path = tempfile.NamedTemporaryFile(delete=False, suffix=".svg").name

    cmd = [
        "py-spy",
        "record",
        "-o",
        svg_path,
        "--pid",
        str(pid),
        "--duration",
        "6",
        "--format",
        "flamegraph",
    ]

    print("Running profiler:", " ".join(cmd))

    try:
        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            errors="ignore",
        )
    except Exception as e:
        return {"error": f"Profiler failed to start: {e}"}

    if process.returncode != 0 or not os.path.exists(svg_path):
        return {"error": "Profiler execution failed", "stderr": process.stderr}

    try:
        hotspots = extract_hotspots(svg_path)
    except Exception as e:
        hotspots = {"error": str(e)}

    return {
        "flamegraph_path": svg_path,
        "hotspots": hotspots,
    }

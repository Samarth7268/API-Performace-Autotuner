import subprocess
import os

OLLAMA_PATH = r"C:\Users\91636\AppData\Local\Programs\Ollama\ollama.exe"

def advise(report):
    metrics = report["load_metrics"]
    status = report["health_status"]

    prompt = f"""
You are a senior backend performance engineer.

Analyze this API performance report and give short optimization advice.

Status: {status}

Metrics:
- Median latency: {metrics.get("median_latency")} ms
- P95 latency: {metrics.get("p95_latency")} ms
- P99 latency: {metrics.get("p99_latency")} ms
- RPS: {metrics.get("rps")}
- Error rate: {metrics.get("error_rate")}
- Throughput: {metrics.get("throughput")}

Respond with bullet points only.
"""

    try:
        process = subprocess.Popen(
            [OLLAMA_PATH, "run", "llama3"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        output, err = process.communicate(input=prompt, timeout=180)

        if not output.strip():
            return ["AI Agent returned empty response. Try again."]

        return [line.lstrip("-• ").strip() for line in output.split("\n") if line.strip()]

    except subprocess.TimeoutExpired:
        process.kill()
        return ["AI Agent timeout: Model took too long to respond. Reduce prompt or retry."]

    except FileNotFoundError:
        return ["Ollama not found. Ensure it's installed and path is correct."]

    except Exception as e:
        return [f"AI Agent failure: {str(e)}"]

from .load_tester import run_load_test
from .scorer import score
import traceback


def auto_tune(url: str):
    """
    Try multiple load configs, score each result,
    return best config and improvement vs baseline.
    """

    configs = [
        {"users": 5, "spawn_rate": 2},
        {"users": 10, "spawn_rate": 5},
        {"users": 20, "spawn_rate": 5},
        {"users": 30, "spawn_rate": 10}
    ]

    results = []

    for cfg in configs:
        try:
            req = type("Req", (), {})()
            req.url = url
            req.users = cfg["users"]
            req.spawn_rate = cfg["spawn_rate"]
            req.runtime = 10

            metrics = run_load_test(req)
            if "error" in metrics:
                continue

            score_value = score(metrics)

            results.append({
                "config": cfg,
                "metrics": metrics,
                "score": round(score_value, 2)
            })

        except Exception as e:
            results.append({
                "config": cfg,
                "error": str(e),
                "trace": traceback.format_exc()
            })

    if not results:
        return {"error": "Auto-tuning failed: no valid runs"}

    scored = [r for r in results if "score" in r]
    best = max(scored, key=lambda r: r["score"])
    baseline = scored[0]

    # Improvement stats
    improvement = {
        "rps_gain": round(best["metrics"]["rps"] - baseline["metrics"]["rps"], 2),
        "p95_drop": round(baseline["metrics"]["p95_latency"] - best["metrics"]["p95_latency"], 2),
        "score_gain": round(best["score"] - baseline["score"], 2)
    }

    return {
        "baseline": baseline,
        "best_config": best,
        "improvement": improvement,
        "trials": scored
    }

def score(metrics):
    """
    Scoring function for Auto-Tuner

    Higher score = better performance

    Formula:
      score = RPS - (P95 latency penalty)
    """

    rps = float(metrics.get("rps", 0))
    p95 = float(metrics.get("p95_latency", 9999))

    # Penalize latency heavily
    latency_penalty = p95 / 10

    final_score = round(rps - latency_penalty, 3)

    return final_score

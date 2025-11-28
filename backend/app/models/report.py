from pydantic import BaseModel
from typing import Dict, List, Any, Optional


# ----------------------------------------------------
# LOAD TEST RESULTS
# ----------------------------------------------------
class LoadTestResult(BaseModel):
    median_latency: float
    p95_latency: float
    p99_latency: float
    rps: float
    error_rate: float
    throughput: float


# ----------------------------------------------------
# PROFILING RESULTS
# ----------------------------------------------------
class ProfileResult(BaseModel):
    flamegraph_path: Optional[str] = None
    hotspots: Dict[str, float] = {}
    error: Optional[str] = None


# ----------------------------------------------------
# FINAL REPORT MODEL
# ----------------------------------------------------
class FinalReport(BaseModel):
    id: str
    generated_at: str
    health_status: str
    summary: str

    load_metrics: LoadTestResult
    profile_metrics: Dict[str, Any]

    ai_advice: List[str] = []

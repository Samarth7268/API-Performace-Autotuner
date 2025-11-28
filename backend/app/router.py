from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from pathlib import Path

from .models.benchmark import BenchmarkRequest
from .services.load_tester import run_load_test
from .services.profiler import run_profiler
from .services.report_generator import generate_report, save_report, get_report
from .services.ai_agent import advise
from .services.auto_tuner import auto_tune
from .config import config

router = APIRouter(prefix="/api", tags=["API Performance Autotuner"])

# Directory where flamegraphs are stored
TEMP_DIR = Path(config.PROFILER_OUTPUT)


# --------------------------------------------------------
# MAIN BENCHMARK PIPELINE
# --------------------------------------------------------
@router.post("/benchmark")
def benchmark_api(request: BenchmarkRequest):
    """
    Full pipeline:
    Load testing → Profiling → Report → AI → Auto Tuning → Save
    """
    try:
        # ----------------------------
        # 1. Run load test
        # ----------------------------
        load_results = run_load_test(request)
        if isinstance(load_results, dict) and "error" in load_results:
            raise HTTPException(status_code=400, detail=load_results)

        # ----------------------------
        # 2. CPU profiling (non-fatal)
        # ----------------------------
        try:
            profile_results = run_profiler()
        except Exception as e:
            profile_results = {"error": str(e)}

        # ----------------------------
        # 3. Generate base report
        # ----------------------------
        report = generate_report(load_results, profile_results)

        # ----------------------------
        # 4. AI advisor (fail-safe)
        # ----------------------------
        try:
            ai_advice = advise(report)
        except Exception as e:
            ai_advice = [f"AI engine unavailable: {str(e)}"]

        report["ai_advice"] = ai_advice

        # ----------------------------
        # 5. Auto Tuning Engine
        # ----------------------------
        try:
            auto_tuning = auto_tune(str(request.url))
        except Exception as e:
            auto_tuning = {
                "status": "failed",
                "error": str(e),
                "recommended_config": None
            }

        report["auto_tuning"] = auto_tuning

        # ----------------------------
        # 6. Persist report
        # ----------------------------
        saved = save_report(report)

        # ----------------------------
        # 7. API response
        # ----------------------------
        return {
            "status": "success",
            "report_id": saved["report_id"],
            "report_file": saved["file_path"],
            "report": report,
            "ai_advice": ai_advice,
            "auto_tuning": auto_tuning
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------------------------------------------------------
# PROFILE ONLY
# --------------------------------------------------------
@router.get("/profile")
def profile_api():
    """
    Run profiler independently
    """
    try:
        return run_profiler()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------------------------------------------------------
# FETCH REPORT
# --------------------------------------------------------
@router.get("/report/{report_id}")
def fetch_report(report_id: str):
    """
    Fetch previously saved report.
    """
    report = get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return {
        "status": "success",
        "report": report
    }


# --------------------------------------------------------
# SERVE FLAMEGRAPH
# --------------------------------------------------------
@router.get("/flamegraph/{filename}")
def serve_flamegraph(filename: str):
    """
    Secure static serving for flamegraph SVG
    """
    safe_name = os.path.basename(filename)
    file_path = (TEMP_DIR / safe_name).resolve()

    # Prevent outside access
    if not str(file_path).startswith(str(TEMP_DIR.resolve())):
        raise HTTPException(status_code=403, detail="Invalid path")

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Flamegraph not found")

    return FileResponse(file_path, media_type="image/svg+xml")

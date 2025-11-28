import threading
import uuid
import time
from datetime import datetime

_jobs = {}
_lock = threading.Lock()


def run_async_task(func, *args, **kwargs):
    job_id = str(uuid.uuid4())

    with _lock:
        _jobs[job_id] = {
            "status": "QUEUED",
            "created_at": datetime.utcnow().isoformat(),
            "started_at": None,
            "finished_at": None,
            "error": None,
            "result": None
        }

    def task():
        with _lock:
            _jobs[job_id]["status"] = "RUNNING"
            _jobs[job_id]["started_at"] = datetime.utcnow().isoformat()

        try:
            output = func(*args, **kwargs)

            with _lock:
                _jobs[job_id]["status"] = "COMPLETED"
                _jobs[job_id]["result"] = output
                _jobs[job_id]["finished_at"] = datetime.utcnow().isoformat()

        except Exception as e:
            with _lock:
                _jobs[job_id]["status"] = "FAILED"
                _jobs[job_id]["error"] = str(e)
                _jobs[job_id]["finished_at"] = datetime.utcnow().isoformat()

    thread = threading.Thread(target=task, daemon=True)
    thread.start()

    return job_id


def job_status(job_id):
    with _lock:
        return _jobs.get(job_id) or {
            "status": "UNKNOWN",
            "message": "No such job ID"
        }

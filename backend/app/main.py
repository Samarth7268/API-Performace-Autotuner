from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .router import router

app = FastAPI(
    title="API Performance Autotuner",
    description="Automated API Load Testing, CPU Profiling, and AI Optimization Agent",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to exact domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "service": "API Performance Autotuner",
        "status": "running",
        "endpoints": [
            "/api/benchmark",
            "/api/profile",
            "/api/report/{id}",
            "/api/flamegraph/{file}"
        ]
    }

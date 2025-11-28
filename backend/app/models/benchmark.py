from pydantic import BaseModel, HttpUrl, Field


class BenchmarkRequest(BaseModel):
    url: HttpUrl = Field(..., description="Target API endpoint")
    
    users: int = Field(
        default=20,
        ge=1,
        le=500,
        description="Number of concurrent users"
    )
    
    spawn_rate: int = Field(
        default=5,
        ge=1,
        le=100,
        description="User ramp-up speed per second"
    )
    
    runtime: int = Field(
        default=10,
        ge=5,
        le=300,
        description="Load test duration in seconds"
    )

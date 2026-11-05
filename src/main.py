import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="FlashRoute Backend Engine",
    description="Production-grade logistics tracking API Engine",
    version="0.1.0",
)


@app.get("/api/v1/health", tags=["Infrastructure"])
async def health_check():
    """
    Global Health Check endpoint to verify server status.
    """
    return {"status": "healthy", "version": "0.1.0"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

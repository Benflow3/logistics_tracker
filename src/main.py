import uvicorn
from fastapi import FastAPI
from api.v1.auth import auth_router

app = FastAPI(
    title="FlashRoute Backend Engine",
    description="Production-grade logistics tracking API Engine",
    version="0.1.0",
)

app.include_router(auth_router)

@app.get("/api/v1/health", tags=["Infrastructure"])
async def health_check():
    """
    Global Health Check endpoint to verify server status.
    """
    return {"status": "healthy", "version": "0.1.0"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True,host="0.0.0.0",port=8000)

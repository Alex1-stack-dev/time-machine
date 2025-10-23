from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import logging
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Time Machine API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_current_time():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

def get_user():
    return "alexmack12343-cmyk"

@app.get("/")
async def root():
    return {
        "message": "Welcome to Time Machine API",
        "version": "1.0.0",
        "currentTime": get_current_time(),
        "user": get_user(),
        "project_id": "prj_9diwl2BK49d5XzxbZQW9eSXyptsn"
    }

@app.get("/api")
async def api_root():
    return {
        "message": "Time Machine API endpoint",
        "currentTime": get_current_time(),
        "user": get_user(),
        "endpoints": [
            "/",
            "/api",
            "/api/time",
            "/api/user",
            "/api/health"
        ]
    }

@app.get("/api/time")
async def get_current_timestamp():
    return {
        "timestamp": get_current_time(),
        "timezone": "UTC",
        "user": get_user()
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": get_current_time(),
        "user": get_user(),
        "environment": os.getenv("VERCEL_ENV", "development")
    }

@app.get("/api/user")
async def user_info():
    return {
        "login": get_user(),
        "timestamp": get_current_time()
    }

# Error handling
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": f"The requested path '{request.url.path}' was not found",
            "currentTime": get_current_time(),
            "user": get_user(),
            "availableEndpoints": [
                "/",
                "/api",
                "/api/time",
                "/api/user",
                "/api/health"
            ]
        }
    )

# Export for Vercel serverless function
from mangum import Mangum
handler = Mangum(app)

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000, reload=True)

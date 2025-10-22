from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict
import os
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Time Machine API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "online"
    }

@app.get("/health")
@app.get("/api/health")
async def health_check() -> Dict:
    """Health check endpoint"""
    logger.debug("Health check endpoint called")
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "environment": os.getenv("VERCEL_ENV", "development"),
            "python_version": sys.version,
            "user": "alexmack12343-cmyk",
            "debug": True
        }
    except Exception as e:
        logger.error("Health check failed", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/time")
async def get_time():
    """Current time endpoint"""
    return {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": "UTC"
    }

@app.get("/api/user")
async def get_user():
    """User information endpoint"""
    return {
        "login": "alexmack12343-cmyk",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }

# Error handling middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")
    try:
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Request failed: {str(e)}", exc_info=True)
        return await error_handler(request, e)

# Error handler
async def error_handler(request: Request, exc: Exception):
    error_id = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    logger.error(f"Error ID: {error_id}")
    logger.error(f"Path: {request.url.path}")
    logger.error(f"Method: {request.method}")
    logger.error("Traceback:", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "error_id": error_id,
            "message": "An unexpected error occurred. Our team has been notified."
        }
    )

# Not found handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": f"The requested path {request.url.path} was not found",
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "available_endpoints": [
                "/",
                "/health",
                "/api/health",
                "/api/time",
                "/api/user"
            ]
        }
    )

# Export for Vercel serverless function
from mangum import Mangum
handler = Mangum(app, enable_lifespan=False)

# Add this for local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)

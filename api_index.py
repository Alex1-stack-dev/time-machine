from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging
import sys

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

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Time Machine API",
        "version": "1.0.0",
        "currentTime": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "user": "alexmack12343-cmyk"
    }

# Health check endpoint
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "user": "alexmack12343-cmyk"
    }

# API endpoints
@app.get("/api")
async def api_root():
    return {
        "message": "Time Machine API endpoint",
        "currentTime": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "endpoints": [
            "/",
            "/health",
            "/api",
            "/api/time",
            "/api/user"
        ]
    }

@app.get("/api/time")
async def get_time():
    return {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": "UTC"
    }

@app.get("/api/user")
async def get_user():
    return {
        "login": "alexmack12343-cmyk",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }

# Error handling
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": f"The requested path '{request.url.path}' was not found",
            "availableEndpoints": [
                "/",
                "/health",
                "/api",
                "/api/time",
                "/api/user"
            ],
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Export for Vercel serverless function
from mangum import Mangum
handler = Mangum(app)

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)

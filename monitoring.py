from prometheus_client import Counter, Histogram
import time

REQUEST_COUNT = Counter(
    'app_request_count',
    'Application Request Count',
    ['endpoint']
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Application Request Latency',
    ['endpoint']
)

@app.middleware("http")
async def monitoring_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    
    REQUEST_COUNT.labels(endpoint=request.url.path).inc()
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(
        time.time() - start_time
    )
    
    return response

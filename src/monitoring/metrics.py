import logging
from prometheus_client import Counter, Histogram, start_http_server
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("shapeshifter")

# Prometheus Metrics
REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint']
)

WORKFLOW_COUNT = Counter(
    'workflow_executions_total',
    'Total workflow executions',
    ['type', 'status']
)

class MetricsManager:
    """Manager for application metrics and monitoring"""
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MetricsManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if not self.initialized:
            self.logger = logger
            self.initialized = True

    def start_server(self, port: int = 8000):
        """Start Prometheus metrics server"""
        try:
            start_http_server(port)
            self.logger.info(f"Metrics server started on port {port}")
        except Exception as e:
            self.logger.error(f"Failed to start metrics server: {e}")

    def log_request(self, method: str, endpoint: str, status: int, duration: float):
        """Log HTTP request metrics"""
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)
        self.logger.info(f"Request: {method} {endpoint} - {status} ({duration:.3f}s)")

    def log_workflow(self, workflow_type: str, status: str):
        """Log workflow execution metrics"""
        WORKFLOW_COUNT.labels(type=workflow_type, status=status).inc()
        self.logger.info(f"Workflow: {workflow_type} - {status}")

metrics = MetricsManager()

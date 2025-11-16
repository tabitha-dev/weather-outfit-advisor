"""
Production Observability Configuration

This module configures Cloud Monitoring, Cloud Logging, and Cloud Trace
for the Weather Outfit ADK system when deployed to Google Cloud.
"""

import os
import logging
import time
from typing import Optional

def setup_production_observability():
    """
    Configure production observability (metrics, logging, tracing).
    
    Automatically detects if running in Google Cloud and configures:
    - Cloud Logging (structured JSON logs)
    - Cloud Monitoring (custom metrics)
    - Cloud Trace (distributed tracing)
    
    Returns:
        dict: Configuration status
    """
    config = {
        "logging": False,
        "metrics": False,
        "tracing": False,
        "project_id": None,
        "region": None
    }
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    region = os.getenv("GCP_REGION", "us-central1")
    
    if not project_id:
        logging.info("ℹ️  Metrics disabled (GOOGLE_CLOUD_PROJECT not set)")
        return config
    
    config["project_id"] = project_id
    config["region"] = region
    
    enable_logging = os.getenv("ENABLE_LOGGING", "true").lower() == "true"
    enable_metrics = os.getenv("ENABLE_METRICS", "true").lower() == "true"
    enable_tracing = os.getenv("ENABLE_TRACING", "true").lower() == "true"
    
    if enable_logging:
        try:
            import google.cloud.logging  # type: ignore
            client = google.cloud.logging.Client(project=project_id)
            client.setup_logging()
            config["logging"] = True
            logging.info(f"✅ Cloud Logging enabled for project: {project_id}")
        except Exception as e:
            logging.warning(f"⚠️  Failed to setup Cloud Logging: {e}")
    
    if enable_metrics:
        try:
            from google.cloud import monitoring_v3  # type: ignore
            client = monitoring_v3.MetricServiceClient()
            config["metrics"] = True
            logging.info(f"✅ Cloud Monitoring enabled for project: {project_id}")
        except Exception as e:
            logging.warning(f"⚠️  Failed to setup Cloud Monitoring: {e}")
    
    if enable_tracing:
        try:
            from opentelemetry import trace  # type: ignore
            from opentelemetry.sdk.trace import TracerProvider  # type: ignore
            from opentelemetry.sdk.trace.export import BatchSpanProcessor  # type: ignore
            from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter  # type: ignore
            
            trace.set_tracer_provider(TracerProvider())
            
            cloud_trace_exporter = CloudTraceSpanExporter(project_id=project_id)
            trace.get_tracer_provider().add_span_processor(
                BatchSpanProcessor(cloud_trace_exporter)
            )
            
            config["tracing"] = True
            logging.info(f"✅ Cloud Trace enabled for project: {project_id}")
        except Exception as e:
            logging.warning(f"⚠️  Failed to setup Cloud Trace: {e}")
    
    return config


def get_structured_logger(service_name: str, level: str = "INFO") -> logging.Logger:
    """
    Get a structured logger for Cloud Logging.
    
    Args:
        service_name: Name of the service (e.g., 'frontend', 'coach_service')
        level: Log level (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(service_name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    
    if not project_id:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '{"time": "%(asctime)s", "level": "%(levelname)s", '
            '"service": "%(name)s", "message": "%(message)s"}'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    try:
        import google.cloud.logging  # type: ignore
        client = google.cloud.logging.Client(project=project_id)
        handler = client.get_default_handler()
        logger.addHandler(handler)
    except Exception as e:
        logging.warning(f"Failed to setup Cloud Logging handler: {e}")
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '{"time": "%(asctime)s", "level": "%(levelname)s", '
            '"service": "%(name)s", "message": "%(message)s"}'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


class MetricsClient:
    """
    Cloud Monitoring metrics client for recording custom metrics.
    """
    
    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.enabled = self.project_id is not None
        self.client = None
        
        if self.enabled:
            try:
                from google.cloud import monitoring_v3  # type: ignore
                self.client = monitoring_v3.MetricServiceClient()
                self.project_name = f"projects/{self.project_id}"
            except Exception as e:
                logging.warning(f"Failed to initialize metrics client: {e}")
                self.enabled = False
    
    def record_counter(self, metric_name: str, value: int, labels: Optional[dict] = None):
        """Record a counter metric."""
        if not self.enabled or not self.client:
            return
        
        try:
            from google.cloud import monitoring_v3  # type: ignore
            
            series = monitoring_v3.TimeSeries()
            series.metric.type = f"custom.googleapis.com/weather_outfit/{metric_name}"
            
            if labels:
                for key, val in labels.items():
                    series.metric.labels[key] = str(val)
            
            now = time.time()
            seconds = int(now)
            nanos = int((now - seconds) * 10**9)
            interval = monitoring_v3.TimeInterval(
                {"end_time": {"seconds": seconds, "nanos": nanos}}  # type: ignore
            )
            point = monitoring_v3.Point(
                {"interval": interval, "value": {"int64_value": value}}  # type: ignore
            )
            series.points = [point]
            
            self.client.create_time_series(
                name=self.project_name,
                time_series=[series]
            )
        except Exception as e:
            logging.warning(f"Failed to record metric {metric_name}: {e}")
    
    def record_gauge(self, metric_name: str, value: float, labels: Optional[dict] = None):
        """Record a gauge metric."""
        if not self.enabled or not self.client:
            return
        
        try:
            from google.cloud import monitoring_v3  # type: ignore
            
            series = monitoring_v3.TimeSeries()
            series.metric.type = f"custom.googleapis.com/weather_outfit/{metric_name}"
            
            if labels:
                for key, val in labels.items():
                    series.metric.labels[key] = str(val)
            
            now = time.time()
            seconds = int(now)
            nanos = int((now - seconds) * 10**9)
            interval = monitoring_v3.TimeInterval(
                {"end_time": {"seconds": seconds, "nanos": nanos}}  # type: ignore
            )
            point = monitoring_v3.Point(
                {"interval": interval, "value": {"double_value": value}}  # type: ignore
            )
            series.points = [point]
            
            self.client.create_time_series(
                name=self.project_name,
                time_series=[series]
            )
        except Exception as e:
            logging.warning(f"Failed to record metric {metric_name}: {e}")


def trace_request(func):
    """
    Decorator to trace function calls with Cloud Trace.
    
    Usage:
        @trace_request
        def my_function():
            ...
    """
    def wrapper(*args, **kwargs):
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        
        if not project_id:
            return func(*args, **kwargs)
        
        try:
            from opentelemetry import trace  # type: ignore
            
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span(func.__name__):
                return func(*args, **kwargs)
        except Exception as e:
            logging.warning(f"Tracing failed: {e}")
            return func(*args, **kwargs)
    
    return wrapper


if __name__ == "__main__":
    config = setup_production_observability()
    print(f"Observability Configuration:")
    print(f"  Project: {config['project_id']}")
    print(f"  Region: {config['region']}")
    print(f"  Logging: {'✅' if config['logging'] else '❌'}")
    print(f"  Metrics: {'✅' if config['metrics'] else '❌'}")
    print(f"  Tracing: {'✅' if config['tracing'] else '❌'}")

# Monitoring & Observability Guide

Complete guide to monitoring the Weather Outfit ADK system with Google Cloud Monitoring.

## 📊 Overview

The monitoring system provides three pillars of observability:

1. **Metrics** - Performance and usage metrics (Google Cloud Monitoring)
2. **Traces** - Distributed tracing across agents (OpenTelemetry + Cloud Trace)
3. **Logs** - Structured logging (Google Cloud Logging)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This includes:
- `google-cloud-monitoring` - Metrics collection
- `google-cloud-logging` - Centralized logging
- `opentelemetry-*` - Distributed tracing

### 2. Set Environment Variables

```bash
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_LOCATION=us-central1
```

### 3. Enable APIs

```bash
gcloud services enable monitoring.googleapis.com
gcloud services enable logging.googleapis.com
gcloud services enable cloudtrace.googleapis.com
```

## 📈 Metrics

### Available Metrics

The system automatically tracks:

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `agent_call_latency` | Gauge | agent | Time to complete agent call (ms) |
| `agent_calls` | Gauge | agent, status | Running total of agent invocations |
| `tool_execution_latency` | Gauge | tool | Tool execution time (ms) |
| `tool_calls` | Gauge | tool, status | Running total of tool invocations |
| `http_request_latency` | Gauge | service, method, path, status | HTTP request duration (ms) |
| `http_requests` | Gauge | service, method, status | Running total of HTTP requests |

**Note**: All metrics use GAUGE kind for simplicity. Counter metrics (agent_calls, tool_calls, http_requests) report running totals tracked in-memory.

### Using Metrics in Code

```python
from weather_outfit_adk.monitoring import agent_metrics

# Increment a counter
agent_metrics.increment_counter("agent_calls", labels={"agent": "coach", "status": "success"})

# Record latency
agent_metrics.record_latency("agent_call_latency", 125.5, labels={"agent": "weather"})

# Measure execution time
with agent_metrics.measure_time("tool_execution", labels={"tool": "get_weather"}):
    result = get_weather(city="Seattle")
```

### View Metrics

**Google Cloud Console:**
1. Go to **Monitoring** > **Metrics Explorer**
2. Search for `custom.googleapis.com/agent/`
3. Select metric and add filters

**Query with MQL:**
```
fetch global
| metric 'custom.googleapis.com/agent/agent_call_latency'
| group_by 1m, [value_agent_call_latency_mean: mean(value.agent_call_latency)]
| every 1m
```

## 📝 Structured Logging

### Setup Logging

```python
from weather_outfit_adk.monitoring import setup_logging

# Initialize logger for your service
logger = setup_logging(
    service_name="coach-agent",
    level="INFO",
    enable_cloud_logging=True
)

# Use logger
logger.info("Agent call started", extra={"user_id": "user-123", "city": "Seattle"})
logger.error("Weather API failed", extra={"error_code": "TIMEOUT"})
```

### Log Format

All logs are structured JSON:

```json
{
  "time": "2025-11-13T23:45:12",
  "level": "INFO",
  "service": "coach-agent",
  "message": "Agent call completed",
  "user_id": "user-123",
  "duration_ms": 245.5
}
```

### View Logs

**Google Cloud Console:**
1. Go to **Logging** > **Logs Explorer**
2. Filter: `resource.type="global" AND jsonPayload.service="coach-agent"`

**Query:**
```
resource.type="global"
jsonPayload.level="ERROR"
timestamp>="2025-11-13T00:00:00Z"
```

## 🔍 Distributed Tracing

### Setup Tracing

```python
from weather_outfit_adk.monitoring import setup_tracing, trace_agent_call

# Initialize tracing
tracer = setup_tracing("coach-agent")

# Trace an operation
with trace_agent_call("weather_agent", "get_forecast"):
    result = call_weather_agent(city="Portland")
```

### View Traces

**Google Cloud Console:**
1. Go to **Trace** > **Trace List**
2. Filter by service name
3. Click trace to see detailed timeline

**Trace Example:**
```
coach_agent.call (245ms)
  ├─ weather_agent.get_forecast (89ms)
  ├─ activity_agent.classify (45ms)
  ├─ stylist_agent.plan_outfit (78ms)
  └─ safety_agent.check (23ms)
```

## 📊 Dashboards

### Create Pre-configured Dashboard

```python
from weather_outfit_adk.monitoring.dashboards import create_agent_dashboard

# Create dashboard programmatically
dashboard_name = create_agent_dashboard()
```

Or run the script:
```bash
python -m weather_outfit_adk.monitoring.dashboards
```

### Dashboard Includes

- **Agent Call Latency** - Average response time per agent
- **Agent Call Rate** - Requests per minute by agent
- **Tool Execution Time** - Tool performance breakdown
- **Error Rate** - Failed requests over time

### Access Dashboard

Go to: https://console.cloud.google.com/monitoring/dashboards/custom

## 🔔 Alerting Policies

### Create Alerts

#### High Error Rate Alert

```bash
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="High Agent Error Rate" \
  --condition-display-name="Error rate > 5%" \
  --condition-threshold-value=0.05 \
  --condition-threshold-duration=300s \
  --condition-filter='resource.type="global" AND metric.type="custom.googleapis.com/agent/agent_calls" AND metric.label.status="error"'
```

#### High Latency Alert

```bash
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="High Agent Latency" \
  --condition-display-name="Latency > 2000ms" \
  --condition-threshold-value=2000 \
  --condition-threshold-duration=180s \
  --condition-filter='resource.type="global" AND metric.type="custom.googleapis.com/agent/agent_call_latency"'
```

### Recommended Alerts

| Alert | Condition | Threshold | Duration |
|-------|-----------|-----------|----------|
| High Error Rate | Error rate > 5% | 0.05 | 5 min |
| High Latency | P95 latency > 2s | 2000ms | 3 min |
| Low Availability | Success rate < 95% | 0.95 | 10 min |
| High Tool Latency | Tool time > 5s | 5000ms | 3 min |

## 🔧 Integration with A2A Services

### Add Monitoring to A2A Service

```python
from google.adk.a2a import to_a2a
from weather_outfit_adk.monitoring import setup_logging, setup_tracing, add_monitoring_to_app
from weather_outfit_adk.agents.weather import weather_agent

# Setup monitoring
logger = setup_logging("weather-agent", enable_cloud_logging=True)
tracer = setup_tracing("weather-agent")

# Create A2A app
app = to_a2a(weather_agent)

# Add monitoring middleware
add_monitoring_to_app(app, "weather-agent")

# Run with monitoring enabled
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Example: Weather Service with Monitoring

See `deploy/a2a/weather_service/app.py` for a complete example.

## 📉 Performance Monitoring

### Key Performance Indicators (KPIs)

Monitor these metrics for system health:

**Availability**
- Target: > 99.5%
- Formula: `successful_requests / total_requests`

**Latency (P95)**
- Target: < 2000ms
- Measure: 95th percentile response time

**Error Rate**
- Target: < 1%
- Formula: `error_requests / total_requests`

**Throughput**
- Target: Varies by load
- Measure: Requests per minute

### Query Examples

**Average Latency by Agent:**
```sql
SELECT
  metric.label.agent,
  AVG(value.agent_call_latency) as avg_latency_ms
FROM
  custom.googleapis.com/agent/agent_call_latency
WHERE
  timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
GROUP BY
  metric.label.agent
```

**Error Rate by Service:**
```sql
SELECT
  metric.label.service,
  COUNT(*) as error_count
FROM
  custom.googleapis.com/agent/agent_calls
WHERE
  metric.label.status = "error"
  AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
GROUP BY
  metric.label.service
```

## 🐛 Debugging with Monitoring

### Common Scenarios

**Scenario 1: High Latency**
1. Check **Trace List** for slow traces
2. Identify bottleneck in trace timeline
3. Review **Tool Execution Time** metric
4. Optimize slow tool or add caching

**Scenario 2: Errors**
1. Filter logs by `level="ERROR"`
2. Check error message patterns
3. Review **Error Rate** dashboard
4. Look at trace for failed requests

**Scenario 3: Performance Degradation**
1. Compare current metrics to baseline
2. Check for resource exhaustion (CPU, memory)
3. Review recent deployments
4. Scale up if needed

## 🎯 Best Practices

1. **Always Enable Monitoring in Production**
   - Set `GOOGLE_CLOUD_PROJECT` environment variable
   - Enable Cloud Logging and Cloud Trace

2. **Use Structured Logging**
   - Include context (user_id, session_id)
   - Use appropriate log levels (INFO, WARNING, ERROR)

3. **Add Custom Metrics for Business Logic**
   - Track domain-specific events
   - Monitor user-facing features

4. **Set Up Alerts Before Launch**
   - Error rate alerts
   - Latency alerts
   - Availability alerts

5. **Regular Dashboard Reviews**
   - Daily: Check error rates
   - Weekly: Review performance trends
   - Monthly: Analyze usage patterns

## 📚 Resources

- **Google Cloud Monitoring**: https://cloud.google.com/monitoring/docs
- **Cloud Logging**: https://cloud.google.com/logging/docs
- **Cloud Trace**: https://cloud.google.com/trace/docs
- **OpenTelemetry**: https://opentelemetry.io/docs/

---

**Status**: ✅ Production Ready - Full monitoring suite integrated

**Last Updated**: November 13, 2025

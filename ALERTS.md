# Alert Policies Guide

Complete guide to setting up and managing Google Cloud Monitoring alerts for the Weather Outfit ADK system.

## 📊 Overview

Alert policies automatically notify you when metrics exceed thresholds, enabling proactive incident response.

## 🚨 Pre-configured Alerts

The system includes three essential alert policies:

**Note**: The default alerts track **throughput rates** (errors/minute, successes/minute, latency). For percentage-based alerts (error rate as errors/total), see [Advanced: Ratio-Based Alerts](#advanced-ratio-based-alerts) below.

### 1. High Error Rate Alert

**Triggers when**: Error rate exceeds 5 errors/minute for 5 minutes

**How it works**: Monitors the error rate using ALIGN_RATE. You specify thresholds in errors/minute (e.g., 5 errors/min), which are automatically converted to errors/second (5/60 = 0.083/sec) for comparison against the rate metric. When the rate exceeds the threshold for the specified duration, the alert triggers.

**Important**: This monitors error **rate**, NOT error percentage. It triggers based on the throughput of errors. For percentage-based error rate alerts (errors/total), see the Advanced section below.

**Why it matters**: Indicates issues with agent operations, API failures, or bugs

**Metrics used**: Error rate (ALIGN_RATE) over 60-second windows

**Recommended action**:
- Check error logs for root cause
- Review recent deployments
- Verify external API availability (weather API)

### 2. High Latency Alert

**Triggers when**: P95 latency exceeds 2000ms for 3 minutes

**Why it matters**: Poor user experience, potential resource constraints

**Recommended action**:
- Check Cloud Trace for slow operations
- Review tool execution times
- Scale up resources if needed

### 3. Low Success Rate Alert

**Triggers when**: Success rate drops below 10 successes/minute for 10 minutes

**How it works**: Monitors the success rate using ALIGN_RATE. You specify thresholds in successes/minute (e.g., 10 successes/min), which are automatically converted to successes/second (10/60 = 0.167/sec) for comparison against the rate metric. When the rate drops below the threshold for the specified duration, the alert triggers.

**Important**: This monitors success **rate**, NOT success percentage. It triggers based on low throughput. For percentage-based availability alerts (successes/total), see the Advanced section below.

**Why it matters**: Significant service degradation or low traffic

**Metrics used**: Success rate (ALIGN_RATE) over 60-second windows

**Recommended action**:
- Immediate incident response
- Check all service health endpoints
- Review system dependencies

## 🔧 Setup Instructions

### Step 1: Create Notification Channel

First, create an email notification channel:

```python
from weather_outfit_adk.monitoring.alerts import create_notification_channel_email

# Create email notification channel
channel_id = create_notification_channel_email(
    project_id="your-project-id",
    email="alerts@yourdomain.com",
    display_name="Weather Outfit Alerts"
)

print(f"Notification channel created: {channel_id}")
```

Or use the `gcloud` CLI:

```bash
gcloud alpha monitoring channels create \
  --display-name="Weather Outfit Alerts" \
  --type=email \
  --channel-labels=email_address=alerts@yourdomain.com
```

### Step 2: Create Alert Policies

#### Option A: Create All Alerts (Recommended)

```python
from weather_outfit_adk.monitoring.alerts import AlertPolicyManager

# Initialize with notification channels
manager = AlertPolicyManager(
    project_id="your-project-id",
    notification_channels=["projects/YOUR_PROJECT/notificationChannels/CHANNEL_ID"]
)

# Create all recommended alerts
alerts = manager.create_all_alerts()

print(f"Created {len(alerts)} alert policies:")
for name, policy_id in alerts.items():
    print(f"  - {name}: {policy_id}")
```

#### Option B: Create Individual Alerts

```python
from weather_outfit_adk.monitoring.alerts import AlertPolicyManager

manager = AlertPolicyManager(
    project_id="your-project-id",
    notification_channels=["CHANNEL_ID"]
)

# High error rate (>5 errors/min for 5 minutes) - Rate-based, not percentage
error_alert = manager.create_high_error_rate_alert(
    errors_per_minute=5,  # Triggers when rate > 5/min (0.083/sec)
    duration_seconds=300
)

# High latency (>2000ms for 3 minutes)
latency_alert = manager.create_high_latency_alert(
    threshold_ms=2000,
    duration_seconds=180
)

# Low success rate (<10 successes/min for 10 minutes) - Rate-based, not percentage
success_alert = manager.create_low_success_rate_alert(
    min_successes_per_minute=10,  # Triggers when rate < 10/min (0.167/sec)
    duration_seconds=600
)
```

#### Option C: Command Line

```bash
# Set environment variable
export GOOGLE_CLOUD_PROJECT=your-project-id

# Create all alerts
python -m weather_outfit_adk.monitoring.alerts --create-all
```

### Step 3: Verify Alerts

Check the Google Cloud Console:

```
https://console.cloud.google.com/monitoring/alerting/policies?project=YOUR_PROJECT
```

You should see three alert policies:
- Weather Outfit ADK - High Error Rate
- Weather Outfit ADK - High Agent Latency
- Weather Outfit ADK - Low Success Rate

## 📧 Notification Channels

### Supported Channels

Google Cloud Monitoring supports multiple notification channels:

- **Email** - Send alerts to email addresses
- **SMS** - Text message notifications
- **Slack** - Slack channel integration
- **PagerDuty** - Incident management
- **Webhooks** - Custom integrations
- **Cloud Pub/Sub** - Event-driven workflows

### List Existing Channels

```python
from weather_outfit_adk.monitoring.alerts import AlertPolicyManager

manager = AlertPolicyManager(project_id="your-project-id")
channels = manager.list_notification_channels()

for channel in channels:
    print(f"{channel['display_name']}: {channel['name']}")
```

Or use `gcloud`:

```bash
gcloud alpha monitoring channels list
```

## ⚙️ Customizing Alerts

### Adjust Thresholds

```python
# More sensitive error rate alert (3 errors/min = 0.05/sec)
manager.create_high_error_rate_alert(
    errors_per_minute=3,
    duration_seconds=180  # 3 minutes
)

# Stricter latency requirement (1 second)
manager.create_high_latency_alert(
    threshold_ms=1000,  # 1 second
    duration_seconds=300  # 5 minutes
)

# Higher success rate threshold (50/min = 0.833/sec)
manager.create_low_success_rate_alert(
    min_successes_per_minute=50,
    duration_seconds=600  # 10 minutes
)
```

### Create Custom Alerts

```python
from google.cloud import monitoring_v3

client = monitoring_v3.AlertPolicyServiceClient()

# Custom alert for tool failures
policy = monitoring_v3.AlertPolicy()
policy.display_name = "High Tool Failure Rate"
policy.documentation.content = "Too many tool execution failures"

condition = monitoring_v3.AlertPolicy.Condition()
condition.display_name = "Tool errors > 10%"
condition.condition_threshold.filter = (
    'resource.type="global" '
    'AND metric.type="custom.googleapis.com/agent/tool_calls" '
    'AND metric.label.status="error"'
)
condition.condition_threshold.comparison = monitoring_v3.ComparisonType.COMPARISON_GT
condition.condition_threshold.threshold_value = 0.10
condition.condition_threshold.duration.seconds = 300

policy.conditions.append(condition)
policy.combiner = monitoring_v3.AlertPolicy.ConditionCombinerType.OR

# Create the policy
created = client.create_alert_policy(
    name=f"projects/YOUR_PROJECT",
    alert_policy=policy
)
```

## 🔔 Alert Response Playbook

### High Error Rate Alert

1. **Check logs** for recent errors
   ```bash
   gcloud logging read "severity>=ERROR" --limit=50 --format=json
   ```

2. **Review metrics** to identify affected agents
   ```
   Go to Metrics Explorer → custom.googleapis.com/agent/agent_calls
   Filter by status="error"
   ```

3. **Common causes**:
   - Weather API down or rate limited
   - Network connectivity issues
   - Invalid API keys
   - Code bugs in recent deployment

4. **Mitigation**:
   - Rollback recent changes if applicable
   - Scale down to reduce API calls
   - Check API status pages

### High Latency Alert

1. **View traces** to identify slow operations
   ```
   Go to Cloud Trace → Trace List
   Sort by duration
   ```

2. **Check resource usage**
   - CPU utilization
   - Memory consumption
   - Network latency

3. **Common causes**:
   - Slow external API calls (weather service)
   - Inefficient LLM prompts
   - Resource constraints

4. **Mitigation**:
   - Scale up resources
   - Optimize prompts
   - Add caching layers
   - Review tool implementations

### Low Availability Alert

1. **Immediate assessment**
   - Check all service health endpoints
   - Review infrastructure status

2. **Escalation path**
   - Notify on-call engineer
   - Start incident channel (Slack/etc)
   - Begin incident documentation

3. **Recovery actions**:
   - Restart failed services
   - Scale up replicas
   - Failover to backup systems
   - Roll back recent changes

## 📊 Alert History

### View Alert Incidents

```bash
# List recent alert incidents
gcloud alpha monitoring policies list-incidents \
  --policy=projects/YOUR_PROJECT/alertPolicies/POLICY_ID
```

### Analyze Patterns

```bash
# Export alert data for analysis
bq query --use_legacy_sql=false \
'SELECT
  timestamp,
  jsonPayload.incident.policy_name,
  jsonPayload.incident.state
FROM
  `YOUR_PROJECT.cloud_monitoring.alert_incidents`
WHERE
  DATE(timestamp) >= CURRENT_DATE() - 7
ORDER BY timestamp DESC'
```

## 🎛️ Alert Maintenance

### Disable Alerts During Maintenance

```bash
# Disable alert policy
gcloud alpha monitoring policies update POLICY_ID \
  --no-enabled

# Re-enable after maintenance
gcloud alpha monitoring policies update POLICY_ID \
  --enabled
```

### Delete Alerts

```bash
# Delete specific alert
gcloud alpha monitoring policies delete POLICY_ID

# List all policies first
gcloud alpha monitoring policies list
```

## 🧪 Testing Alerts

### Trigger Test Alerts

```python
from weather_outfit_adk.monitoring import agent_metrics

# Simulate high error rate
for i in range(100):
    agent_metrics.increment_counter(
        "agent_calls",
        labels={"agent": "test", "status": "error"}
    )

# Simulate high latency
agent_metrics.record_latency(
    "agent_call_latency",
    5000,  # 5 seconds
    labels={"agent": "test"}
)
```

**Note**: Wait for the alert duration period to elapse before expecting notifications.

## 📚 Best Practices

1. **Start Conservative**: Begin with higher thresholds and adjust based on actual behavior

2. **Avoid Alert Fatigue**: Don't create too many alerts or set thresholds too sensitive

3. **Document Runbooks**: Include clear response procedures in alert documentation

4. **Test Regularly**: Verify alerts trigger correctly with test scenarios

5. **Review Periodically**: Adjust thresholds as your system evolves

6. **Multi-Channel Notifications**: Use different channels for different severity levels

7. **Silence During Deployments**: Temporarily disable alerts during planned maintenance

## 🔗 Resources

- **Google Cloud Monitoring Alerts**: https://cloud.google.com/monitoring/alerts
- **Notification Channels**: https://cloud.google.com/monitoring/support/notification-options
- **Alert Policies API**: https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.alertPolicies

---

**Status**: ✅ Production-ready alert configurations available

**Last Updated**: November 13, 2025

## 🎯 Advanced: Ratio-Based Alerts

For production systems requiring percentage-based alerting (e.g., trigger when error rate > 5% regardless of traffic volume), use **MQL (Monitoring Query Language)** alerts.

### Creating Ratio-Based Error Rate Alert

This alert computes `errors / (errors + successes)` to get true error percentage.

```bash
# Create alert policy via gcloud CLI
gcloud alpha monitoring policies create \
  --notification-channels="projects/YOUR_PROJECT/notificationChannels/CHANNEL_ID" \
  --display-name="High Error Rate (Percentage)" \
  --condition-display-name="Error rate > 5%" \
  --condition-monitoring-query-language="
    fetch global
    | { metric 'custom.googleapis.com/agent/agent_calls'
      | filter metric.status == 'error'
      | align rate(1m)
      | group_by [], [value_error: sum(value.agent_calls)]
      ; metric 'custom.googleapis.com/agent/agent_calls'
      | filter metric.status == 'success'
      | align rate(1m)
      | group_by [], [value_success: sum(value.agent_calls)]
      }
    | join
    | value [error_rate: cast_double(val(0)) / (cast_double(val(0)) + cast_double(val(1)))]
    | condition error_rate > 0.05
  " \
  --condition-threshold-duration=300s
```

### Creating Ratio-Based Availability Alert

This alert computes `successes / (errors + successes)` for true availability percentage.

```bash
gcloud alpha monitoring policies create \
  --notification-channels="projects/YOUR_PROJECT/notificationChannels/CHANNEL_ID" \
  --display-name="Low Availability (Percentage)" \
  --condition-display-name="Availability < 95%" \
  --condition-monitoring-query-language="
    fetch global
    | { metric 'custom.googleapis.com/agent/agent_calls'
      | filter metric.status == 'success'
      | align rate(1m)
      | group_by [], [value_success: sum(value.agent_calls)]
      ; metric 'custom.googleapis.com/agent/agent_calls'
      | filter metric.status == 'error'
      | align rate(1m)
      | group_by [], [value_error: sum(value.agent_calls)]
      }
    | join
    | value [availability: cast_double(val(0)) / (cast_double(val(0)) + cast_double(val(1)))]
    | condition availability < 0.95
  " \
  --condition-threshold-duration=600s
```

### Why Use Ratio-Based Alerts?

**Rate-Based Alerts** (default):
- ✅ Simple to set up
- ✅ Detect throughput anomalies
- ✅ Work well for consistent traffic patterns
- ❌ Sensitive to traffic volume changes
- **Best for**: Development, testing, monitoring throughput

**Ratio-Based Alerts** (MQL):
- ✅ Accurate percentage calculation
- ✅ Handle traffic variations correctly
- ✅ Production-grade monitoring
- ❌ More complex to configure
- **Best for**: Production systems with variable traffic

### When to Use Each Approach

| Scenario | Recommendation |
|----------|---------------|
| Development/Testing | Rate-based alerts (simpler) |
| Monitoring absolute throughput | Rate-based alerts |
| Production with variable traffic | Ratio-based alerts (MQL) |
| High-stakes production | Ratio-based alerts (MQL) |
| SLA monitoring (99.9% uptime) | Ratio-based alerts (MQL) |


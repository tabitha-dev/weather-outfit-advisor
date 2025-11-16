# Deployment Guide - Google Cloud Agent Engine

Complete guide for deploying the Weather Outfit ADK system to Google Cloud Agent Engine.

## 📋 Prerequisites

Before deploying, ensure you have:

1. **Google Cloud Project**
   - Active GCP project with billing enabled
   - Project ID noted down

2. **APIs Enabled**
   ```bash
   gcloud services enable aiplatform.googleapis.com
   gcloud services enable storage.googleapis.com
   gcloud services enable run.googleapis.com
   ```

3. **Required Tools**
   ```bash
   # Install gcloud CLI
   curl https://sdk.cloud.google.com | bash
   
   # Install Python ADK
   pip install google-cloud-aiplatform[adk,agent_engines]>=1.111
   ```

4. **Authentication**
   ```bash
   gcloud auth login
   gcloud auth application-default login
   gcloud config set project YOUR_PROJECT_ID
   ```

## 🌍 Environment Setup

### 1. Create GCS Bucket

```bash
export PROJECT_ID="your-project-id"
export REGION="us-central1"
export BUCKET_NAME="${PROJECT_ID}-agent-engine"

gsutil mb -p ${PROJECT_ID} -l ${REGION} gs://${BUCKET_NAME}
```

### 2. Set Up Secrets

Store your API keys in Secret Manager:

```bash
# Create secret for Weather API key
echo -n "your_weather_api_key" | \
  gcloud secrets create weather-api-key \
  --data-file=- \
  --replication-policy="automatic"

# Grant access to the secret
gcloud secrets add-iam-policy-binding weather-api-key \
  --member="serviceAccount:YOUR_SERVICE_ACCOUNT" \
  --role="roles/secretmanager.secretAccessor"
```

### 3. Configure Environment Variables

Create `.env` for local testing:

```bash
# ============================================
# CRITICAL SECRETS (Required)
# ============================================
RAPIDAPI_KEY=your_meteostat_rapidapi_key_here
SESSION_SECRET=your_random_32_char_string_here

# ============================================
# A2A SERVICE URLS (Required for Production)
# ============================================
USE_ADK_AGENTS=true
COACH_URL=http://localhost:8000
WEATHER_URL=http://localhost:8001
STYLIST_URL=http://localhost:8002
ACTIVITY_URL=http://localhost:8003
SAFETY_URL=http://localhost:8004

# ============================================
# GOOGLE CLOUD CONFIGURATION (Required for Observability)
# ============================================
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
GCP_REGION=us-central1

# ============================================
# OPTIONAL CONFIGURATION
# ============================================
GEMINI_API_KEY=your_gemini_api_key_here
DEFAULT_CITY=Redmond
LOG_LEVEL=INFO
ENABLE_METRICS=true
ENABLE_TRACING=true
ENABLE_LOGGING=true

# ============================================
# LEGACY (Backward Compatibility)
# ============================================
WEATHER_API_KEY=${RAPIDAPI_KEY}
GOOGLE_CLOUD_LOCATION=${GCP_REGION}
DEFAULT_MODEL=gemini-2.0-flash-exp
ENABLE_CACHING=true
```

**Environment Variable Reference:**

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `RAPIDAPI_KEY` | ✅ Yes | - | Meteostat weather API key from RapidAPI |
| `SESSION_SECRET` | ✅ Yes | - | Flask session encryption (32+ random chars) |
| `USE_ADK_AGENTS` | Production | `true` | Enable A2A agent integration |
| `COACH_URL` | Production | `http://localhost:8000` | Coach Agent A2A endpoint |
| `WEATHER_URL` | Production | `http://localhost:8001` | Weather Agent A2A endpoint |
| `STYLIST_URL` | Production | `http://localhost:8002` | Stylist Agent A2A endpoint |
| `ACTIVITY_URL` | Production | `http://localhost:8003` | Activity Agent A2A endpoint |
| `SAFETY_URL` | Production | `http://localhost:8004` | Safety Agent A2A endpoint |
| `GOOGLE_CLOUD_PROJECT` | Observability | - | GCP project ID for metrics/logs/traces |
| `GOOGLE_APPLICATION_CREDENTIALS` | Observability | - | Path to service account JSON |
| `GCP_REGION` | No | `us-central1` | Deployment region |
| `GEMINI_API_KEY` | No | ADK default | Google Gemini API key override |
| `DEFAULT_CITY` | No | `Redmond` | Default location for weather |
| `LOG_LEVEL` | No | `INFO` | Logging verbosity (DEBUG/INFO/WARNING/ERROR) |
| `ENABLE_METRICS` | No | Auto | Enable Cloud Monitoring metrics export |
| `ENABLE_TRACING` | No | Auto | Enable Cloud Trace distributed tracing |
| `ENABLE_LOGGING` | No | Auto | Enable Cloud Logging structured logs |

**Production URLs:** Replace `localhost` URLs with deployed service URLs:
```bash
# Example production URLs (replace with your actual deployed endpoints)
COACH_URL=https://coach-agent-abc123-uc.a.run.app
WEATHER_URL=https://weather-agent-def456-uc.a.run.app
STYLIST_URL=https://stylist-agent-ghi789-uc.a.run.app
ACTIVITY_URL=https://activity-agent-jkl012-uc.a.run.app
SAFETY_URL=https://safety-agent-mno345-uc.a.run.app
```

## 🚀 Deployment Methods

### Method 1: Deploy All Agents Together (Recommended for MVP)

Deploy the entire system as a single ADK app:

```bash
# From project root
adk deploy agent-engine \
  --project=${PROJECT_ID} \
  --location=${REGION} \
  --bucket=${BUCKET_NAME} \
  --service-account=YOUR_SERVICE_ACCOUNT
```

**Pros:**
- Simplest deployment
- All agents share memory
- Faster development iteration

**Cons:**
- All agents scale together
- No independent versioning

### Method 2: Deploy Agents Separately (A2A Architecture)

Deploy each agent as an independent service for true A2A communication:

#### Step 1: Deploy Weather Agent Service

```bash
# Create separate directory for Weather agent
mkdir -p deploy/weather_service
cp -r weather_outfit_adk/agents/weather.py deploy/weather_service/
cp -r weather_outfit_adk/tools/weather_tools.py deploy/weather_service/

# Create weather_app.py
cat > deploy/weather_service/app.py << 'EOF'
from google.adk.apps import App
from google.adk import Runner
from weather import weather_agent

app = App(
    name="weather_service",
    root_agent=weather_agent
)

if __name__ == "__main__":
    runner = Runner(app=app)
    runner.run()
EOF

# Deploy
cd deploy/weather_service
adk deploy agent-engine \
  --project=${PROJECT_ID} \
  --location=${REGION} \
  --bucket=${BUCKET_NAME} \
  --service-name=weather-agent

# Note the deployed URL
export WEATHER_AGENT_URL="<deployed-url>"
```

#### Step 2: Deploy Stylist Agent Service

```bash
mkdir -p deploy/stylist_service
# Similar process for stylist agent
# Deploy and note the URL
export STYLIST_AGENT_URL="<deployed-url>"
```

#### Step 3: Deploy Coach Agent with A2A Endpoints

Update `coach_agent` to use RemoteAgent:

```python
from google.adk import RemoteAgent

weather_remote = RemoteAgent(
    project_id=PROJECT_ID,
    location=REGION,
    agent_id="weather-agent"
)

stylist_remote = RemoteAgent(
    project_id=PROJECT_ID,
    location=REGION,
    agent_id="stylist-agent"
)

coach_agent = Agent(
    name="coach_agent",
    tools=[weather_remote, stylist_remote, activity_agent, safety_agent]
)
```

Deploy Coach:

```bash
adk deploy agent-engine \
  --project=${PROJECT_ID} \
  --location=${REGION} \
  --bucket=${BUCKET_NAME} \
  --service-name=coach-agent
```

### Method 3: Deploy to Cloud Run

For more control over infrastructure:

```bash
adk deploy cloud_run \
  --region=${REGION} \
  --project=${PROJECT_ID} \
  --allow-unauthenticated \
  --with_ui \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=${PROJECT_ID},GOOGLE_CLOUD_LOCATION=${REGION}"
```

**Pros:**
- Full container control
- Custom scaling policies
- Can deploy alongside other services

**Cons:**
- More infrastructure management
- Need to handle Agent Engine integration manually

## 🔧 Post-Deployment Configuration

### 1. Test the Deployment

```bash
# Get the deployed endpoint
AGENT_ENDPOINT=$(gcloud run services describe coach-agent \
  --region=${REGION} \
  --format='value(status.url)')

# Test with curl
curl -X POST ${AGENT_ENDPOINT}/query \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "session_id": "test_session_1",
    "message": "What should I wear today in Seattle?"
  }'
```

### 2. Set Up Monitoring

Enable Cloud Monitoring:

```bash
# Create log-based metric for agent calls
gcloud logging metrics create agent_call_count \
  --description="Count of agent invocations" \
  --log-filter='resource.type="cloud_run_revision"
    AND labels.agent_name=~".*_agent"'

# Create alerting policy
gcloud alpha monitoring policies create \
  --notification-channels=YOUR_CHANNEL_ID \
  --display-name="Agent Error Rate" \
  --condition-threshold-value=5 \
  --condition-threshold-duration=300s
```

### 3. Enable Tracing

Agent Engine automatically creates traces. View them in:

```
Cloud Console → Vertex AI → Agent Engine → [Your Agent] → Traces
```

## 📊 Monitoring & Observability

### Key Metrics to Monitor

1. **Request Metrics**
   - Requests per minute
   - Average latency
   - Error rate

2. **Agent Metrics**
   - Agent call frequency (which agents are called most)
   - Token usage per agent
   - Cache hit rate (for weather data)

3. **Business Metrics**
   - User sessions
   - Outfit recommendations generated
   - Safety warnings issued

### Access Logs

```bash
# View recent logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=coach-agent" \
  --limit=50 \
  --format=json

# Stream logs in real-time
gcloud logging tail "resource.type=cloud_run_revision" \
  --format="table(timestamp, severity, textPayload)"
```

### Production Observability Setup

**Step 1: Configure Observability in Code**

The system includes production observability configuration in `config/observability.py`. To enable:

```python
# In your service initialization (e.g., frontend/app.py, deploy/a2a/*/app.py)
from config.observability import setup_production_observability, get_structured_logger

# Setup observability
config = setup_production_observability()

# Get structured logger
logger = get_structured_logger(service_name="your_service")
logger.info("Service started", extra={"version": "1.0.0"})
```

**Step 2: Required IAM Roles for Service Account**

```bash
# Add observability permissions to service account
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:weather-agent-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/monitoring.metricWriter"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:weather-agent-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/cloudtrace.agent"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:weather-agent-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/logging.logWriter"
```

**Step 3: Deploy with Observability Enabled**

```bash
# Deploy with environment variables
gcloud run deploy weather-outfit-frontend \
  --source=frontend \
  --region=us-central1 \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=${PROJECT_ID},GCP_REGION=us-central1,ENABLE_METRICS=true,ENABLE_TRACING=true,ENABLE_LOGGING=true" \
  --service-account=weather-agent-sa@${PROJECT_ID}.iam.gserviceaccount.com
```

**Step 4: Verify Observability**

```bash
# Check metrics
gcloud monitoring time-series list \
  --filter='metric.type=starts_with("custom.googleapis.com/weather_outfit/")' \
  --format=json

# Check logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=weather-outfit-frontend" \
  --limit=10 \
  --format="table(timestamp,severity,jsonPayload.message)"

# Check traces
gcloud trace list \
  --format="table(traceId,spans.name,spans.duration)"
```

**Step 5: Create Custom Dashboard**

```bash
# Create monitoring dashboard (optional)
cat > dashboard.json << 'EOF'
{
  "displayName": "Weather Outfit ADK Dashboard",
  "mosaicLayout": {
    "columns": 12,
    "tiles": [
      {
        "width": 6,
        "height": 4,
        "widget": {
          "title": "Request Rate",
          "xyChart": {
            "dataSets": [{
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "resource.type=\"cloud_run_revision\" AND metric.type=\"run.googleapis.com/request_count\"",
                  "aggregation": {
                    "alignmentPeriod": "60s",
                    "perSeriesAligner": "ALIGN_RATE"
                  }
                }
              }
            }]
          }
        }
      }
    ]
  }
}
EOF

gcloud monitoring dashboards create --config-from-file=dashboard.json
```

## 🔐 Security Best Practices

### 1. Service Account Permissions

Create a dedicated service account with minimal permissions:

```bash
# Create service account
gcloud iam service-accounts create weather-agent-sa \
  --display-name="Weather Agent Service Account"

# Grant only necessary permissions
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:weather-agent-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:weather-agent-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### 2. API Key Rotation

```bash
# Rotate Weather API key
gcloud secrets versions add weather-api-key --data-file=new_key.txt

# Disable old version
gcloud secrets versions disable VERSION_ID --secret=weather-api-key
```

### 3. Network Security

```bash
# Restrict ingress to authenticated users
gcloud run services update coach-agent \
  --region=${REGION} \
  --ingress=internal-and-cloud-load-balancing \
  --no-allow-unauthenticated
```

## 💰 Cost Optimization

### 1. Enable Caching

Caching is already implemented in `weather_tools.py`. Verify it's enabled:

```python
# In config/settings.py
ENABLE_CACHING=true
```

### 2. Set Request Limits

```bash
# Set max instances to control costs
gcloud run services update coach-agent \
  --region=${REGION} \
  --max-instances=10 \
  --min-instances=0
```

### 3. Monitor Costs

```bash
# Check current month spending
gcloud billing accounts list
gcloud billing projects describe ${PROJECT_ID}
```

## 🐛 Troubleshooting

### Issue: Agent not responding

```bash
# Check service status
gcloud run services describe coach-agent --region=${REGION}

# Check recent errors
gcloud logging read "resource.type=cloud_run_revision AND severity>=ERROR" --limit=20
```

### Issue: Weather API failing

```bash
# Verify secret is accessible
gcloud secrets versions access latest --secret=weather-api-key

# Check service account permissions
gcloud secrets get-iam-policy weather-api-key
```

### Issue: High latency

1. Check if caching is working (logs should show "from_cache: true")
2. Review agent call traces in Agent Engine dashboard
3. Consider deploying agents closer to weather API region

## 🔄 Continuous Deployment

### GitHub Actions Example

```yaml
name: Deploy to Agent Engine

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v0
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          project_id: ${{ secrets.GCP_PROJECT_ID }}
      
      - name: Deploy to Agent Engine
        run: |
          pip install google-cloud-aiplatform[adk,agent_engines]
          adk deploy agent-engine \
            --project=${{ secrets.GCP_PROJECT_ID }} \
            --location=us-central1 \
            --bucket=${{ secrets.GCS_BUCKET }}
```

## 📈 Scaling

Agent Engine automatically scales based on:
- Request volume
- Response time requirements
- Available quotas

For custom scaling:

```bash
# Set custom scaling parameters
gcloud run services update coach-agent \
  --region=${REGION} \
  --min-instances=1 \
  --max-instances=100 \
  --concurrency=80
```

## 🎓 Next Steps

After successful deployment:

1. ✅ Set up monitoring dashboards
2. ✅ Configure alerting policies
3. ✅ Test with real users
4. ✅ Implement A2A for independent scaling
5. ✅ Add evaluation metrics
6. ✅ Build a frontend interface

---

**Need Help?**
- [Agent Engine Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit)
- [ADK GitHub Issues](https://github.com/google/adk-python/issues)
- [Google Cloud Support](https://cloud.google.com/support)

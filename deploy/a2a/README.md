# A2A Multi-Service Deployment

**Agent-to-Agent (A2A) Protocol Implementation for Independent Scaling**

This directory contains the A2A multi-service architecture for the Weather Outfit ADK system, enabling each specialized agent to run as an independent microservice.

## 🏗️ Architecture Overview

### Service Topology

```
                     ┌─────────────────┐
                     │  Coach Agent    │
                     │  (Port 8000)    │
                     │  Orchestrator   │
                     └────────┬────────┘
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
           ▼                  ▼                  ▼
    ┌──────────┐       ┌──────────┐      ┌──────────┐
    │ Weather  │       │ Stylist  │      │ Activity │
    │  Agent   │       │  Agent   │      │  Agent   │
    │(Port 8001)       │(Port 8002)      │(Port 8003)
    └──────────┘       └──────────┘      └──────────┘
           │
           ▼
    ┌──────────┐
    │  Safety  │
    │  Agent   │
    │(Port 8004)
    └──────────┘
```

### Service Responsibilities

| Service | Port | Role | Tools |
|---------|------|------|-------|
| **Coach** | 8000 | Main orchestrator, user-facing | Memory tools + Remote agents |
| **Weather** | 8001 | Weather forecasts with caching | get_current_weather, get_hourly_forecast, get_weather_smart |
| **Stylist** | 8002 | Outfit recommendations | plan_outfit |
| **Activity** | 8003 | Activity classification | classify_activity |
| **Safety** | 8004 | Weather safety warnings | check_safety |

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

**Prerequisites:**
- Docker and Docker Compose installed
- Ports 8000-8004 available

**Start all services:**
```bash
cd deploy/a2a

# With docker-compose
docker-compose up

# Or in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Option 2: Local Development (No Docker)

**Prerequisites:**
- Python 3.11+
- All dependencies installed (`pip install -r requirements.txt`)
- Ports 8000-8004 available

**Start all services:**
```bash
cd deploy/a2a

# Create logs directory
mkdir -p logs

# Start all services in background
./start-all.sh

# Stop all services
./stop-all.sh
```

### Option 3: Manual Start (Individual Services)

```bash
# Terminal 1: Weather Agent
python deploy/a2a/weather_service/app.py

# Terminal 2: Stylist Agent
python deploy/a2a/stylist_service/app.py

# Terminal 3: Activity Agent
python deploy/a2a/activity_service/app.py

# Terminal 4: Safety Agent
python deploy/a2a/safety_service/app.py

# Terminal 5: Coach Agent (start last)
python deploy/a2a/coach_service/app.py
```

## 🔍 Testing the A2A Setup

### 1. Check Agent Cards

Each service exposes metadata via A2A agent cards:

```bash
# Check all agent cards
curl http://localhost:8000/.well-known/agent.json  # Coach
curl http://localhost:8001/.well-known/agent.json  # Weather
curl http://localhost:8002/.well-known/agent.json  # Stylist
curl http://localhost:8003/.well-known/agent.json  # Activity
curl http://localhost:8004/.well-known/agent.json  # Safety
```

### 2. Test Individual Services

```bash
# Test Weather Agent directly
curl -X POST http://localhost:8001/run \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user",
    "session_id": "test-session",
    "message": "What is the weather in Seattle?"
  }'

# Test Coach Agent (orchestrates all services)
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user",
    "session_id": "test-session",
    "message": "What should I wear in Portland today?"
  }'
```

### 3. Health Checks

```bash
# Check if all services are healthy
for port in 8000 8001 8002 8003 8004; do
  echo "Checking port $port..."
  curl -f http://localhost:$port/.well-known/agent.json && echo "✅" || echo "❌"
done
```

## 🌐 Environment Variables

### Common Variables (All Services)

```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

### Weather Service Specific

```bash
WEATHER_API_KEY=your_openweather_api_key
```

### Coach Service Specific

```bash
# Remote agent URLs (defaults to localhost)
WEATHER_SERVICE_URL=http://localhost:8001
STYLIST_SERVICE_URL=http://localhost:8002
ACTIVITY_SERVICE_URL=http://localhost:8003
SAFETY_SERVICE_URL=http://localhost:8004
```

## 📦 Deployment to Production

### Google Cloud Run (Separate Services)

Deploy each service independently for true A2A architecture:

```bash
# Deploy Weather Agent
gcloud run deploy weather-agent \
  --source deploy/a2a/weather_service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=your-project

# Deploy Stylist Agent
gcloud run deploy stylist-agent \
  --source deploy/a2a/stylist_service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Deploy Activity Agent
gcloud run deploy activity-agent \
  --source deploy/a2a/activity_service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Deploy Safety Agent
gcloud run deploy safety-agent \
  --source deploy/a2a/safety_service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Deploy Coach Agent (with remote URLs)
gcloud run deploy coach-agent \
  --source deploy/a2a/coach_service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars \
    WEATHER_SERVICE_URL=https://weather-agent-xxxx.run.app,\
    STYLIST_SERVICE_URL=https://stylist-agent-xxxx.run.app,\
    ACTIVITY_SERVICE_URL=https://activity-agent-xxxx.run.app,\
    SAFETY_SERVICE_URL=https://safety-agent-xxxx.run.app
```

### Kubernetes (GKE)

Use the provided Kubernetes manifests:

```bash
# Apply all services
kubectl apply -f deploy/a2a/k8s/

# Check deployment status
kubectl get pods -n weather-outfit

# View logs
kubectl logs -f deployment/coach-agent -n weather-outfit
```

## 🔧 Architecture Benefits

### Independent Scaling

Each agent can scale independently based on load:

```yaml
# Example: Scale Weather Agent to handle more requests
docker-compose up --scale weather-agent=3
```

### Fault Isolation

If one agent fails, others continue operating:
- Weather Agent down → Coach falls back or returns partial response
- Safety Agent down → Outfit recommendations still work

### Technology Flexibility

Each service can:
- Use different models (gemini-2.0-flash vs gemini-1.5-pro)
- Run on different infrastructure
- Have separate deployment schedules
- Use different authentication mechanisms

### Development Velocity

Teams can work on separate agents independently:
- Weather team updates forecasting logic
- Stylist team improves outfit algorithms
- No coordination needed for deployments

## 📊 Monitoring & Observability

### Logs

**Docker Compose:**
```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f coach-agent
```

**Local:**
```bash
# Logs in deploy/a2a/logs/
tail -f deploy/a2a/logs/coach.log
tail -f deploy/a2a/logs/weather.log
```

### Metrics

Each service exposes:
- Agent card metadata (capabilities, version)
- Health status endpoint
- A2A protocol compliance

## 🐛 Troubleshooting

### Service Won't Start

```bash
# Check if port is already in use
lsof -i :8000

# Kill process on port
lsof -ti:8000 | xargs kill -9
```

### Remote Agent Connection Failures

```bash
# Verify remote services are running
curl http://localhost:8001/.well-known/agent.json

# Check Coach service logs for connection errors
docker-compose logs coach-agent
```

### Docker Build Issues

```bash
# Clean rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

## 📚 A2A Protocol Resources

- **A2A Protocol Spec**: https://a2aprotocol.ai/
- **Google ADK A2A Docs**: https://google.github.io/adk-docs/a2a/
- **Agent Card Format**: `/.well-known/agent.json` standard

## 🔗 Related Documentation

- `../../README.md` - Main project documentation
- `../../DEPLOYMENT.md` - Single-service deployment guide
- `../../PROJECT_STATUS.md` - Project status and roadmap

---

**Status**: ✅ Production Ready - Tested with Docker Compose and local deployment

**Last Updated**: November 13, 2025

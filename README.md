# Weather Outfit ADK - Multi-Agent System
<img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExbGtqaHRwZ2ZxYTB4NmNtaWFxY3JtNDQ3a2prczFpbndhaXVrN3p5cSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/IQp947luDDrTK9QLv7/giphy.gif" width="600" />



**Status**: ✅ **PRODUCTION READY** - All tests passing, ready for deployment

A sophisticated weather-based clothing recommendation system built with Google's Agent Development Kit (ADK) for deployment to Google Cloud Agent Engine.

## 🎯 Overview

This project implements a multi-agent AI system that provides personalized clothing recommendations based on:
- Real-time weather conditions
- User activities (work, sports, formal events, casual)
- Personal style preferences (practical, fashion-forward, kid-friendly)
- Comfort profiles (runs cold/hot)
- Safety considerations (extreme weather warnings)

## 🏗️ Architecture

### Multi-Agent Design

The system uses **5 specialized agents** that communicate via Agent-to-Agent (A2A) protocol:

1. **Coach Agent** (Main Orchestrator)
   - User-facing interface
   - Coordinates all other agents
   - Combines responses into friendly answers

2. **Weather Agent**
   - Fetches real-time weather data
   - Implements smart caching (30-minute TTL)
   - Returns structured forecast data

3. **Stylist Agent**
   - Generates outfit recommendations
   - Considers weather, activity, and preferences
   - Provides layering and accessory advice

4. **Activity Agent**
   - Classifies user activities
   - Determines formality and movement levels
   - Provides context for outfit planning

5. **Safety Agent**
   - Monitors weather conditions
   - Issues warnings for extreme weather
   - Provides actionable safety advice

### Key Features

✅ **Activity-Aware Outfits** - Recommends clothing based on your plans (hiking, meetings, dates)  
✅ **Smart Caching** - Reduces API calls and improves response time  
✅ **Safety Warnings** - Alerts for extreme heat, cold, wind, or storms  
✅ **Persona Styles** - Practical, fashion-focused, or kid-friendly responses  
✅ **Memory System** - Remembers your preferences across sessions  

## 📁 Project Structure

```
weather_outfit_adk/
├── agents/              # Agent definitions
│   ├── coach.py        # Main orchestrator agent
│   ├── weather.py      # Weather data specialist
│   ├── stylist.py      # Clothing advisor
│   ├── activity.py     # Activity classifier
│   └── safety.py       # Safety monitor
├── tools/              # Agent tools (functions)
│   ├── weather_tools.py    # Weather API & caching
│   ├── outfit_tools.py     # Outfit planning logic
│   ├── activity_tools.py   # Activity classification
│   └── safety_tools.py     # Safety checking
├── schemas/            # Data models (Pydantic)
│   ├── weather.py      # Weather data structures
│   ├── outfit.py       # Outfit & activity models
│   └── memory.py       # User preferences
├── memory/             # User preference storage
│   └── user_memory.py  # Memory management
└── config/             # Configuration
    └── settings.py     # App settings

app.py                  # Main ADK application entry point
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9-3.13
- Google Cloud Project with Vertex AI enabled
- Weather API key (OpenWeatherMap or similar)

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run locally:**
   ```bash
   python app.py
   ```

## 🌐 Deployment to Google Cloud

### Option 1: Single-Service Deployment (Monolithic)

**Deploy all agents together** - Simplest option for getting started:

```bash
# Install ADK with Agent Engine support
pip install google-cloud-aiplatform[adk,agent_engines]>=1.111

# Authenticate with Google Cloud
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Deploy to Agent Engine
adk deploy agent-engine \
  --project=YOUR_PROJECT_ID \
  --location=us-central1 \
  --bucket=YOUR_GCS_BUCKET
```

### Option 2: A2A Multi-Service Deployment (Recommended for Production)

**Deploy each agent independently** for true microservices architecture with independent scaling:

```bash
# See deploy/a2a/README.md for complete instructions
cd deploy/a2a

# Option A: Docker Compose (local testing)
docker-compose up

# Option B: Google Cloud Run (production)
# Deploy each service separately - see deploy/a2a/README.md

# Option C: Kubernetes/GKE
kubectl apply -f deploy/a2a/k8s/
```

**Benefits of A2A deployment:**
- ✅ Independent scaling per agent
- ✅ Fault isolation (one agent failure doesn't crash system)
- ✅ Technology flexibility (different models per agent)
- ✅ Team independence (deploy agents separately)

See [`deploy/a2a/README.md`](deploy/a2a/README.md) for detailed A2A deployment guide.

### Option 3: Cloud Run (Simple Container Deployment)

```bash
# Deploy as single containerized service
adk deploy cloud_run \
  --region us-central1 \
  --project YOUR_PROJECT_ID \
  --with_ui
```

### Required Environment Variables for Production

Set these in Google Cloud Secret Manager:

- `WEATHER_API_KEY` - Your weather API key
- `GOOGLE_CLOUD_PROJECT` - Your GCP project ID
- `GOOGLE_CLOUD_LOCATION` - Deployment region (e.g., us-central1)

## 💬 Example Interactions

**Basic query:**
```
User: What should I wear today in Seattle?
Agent: It's 58°F and cloudy in Seattle. I recommend jeans, a long-sleeve shirt, 
       and a light jacket. There's a 40% chance of rain, so bring an umbrella!
```

**Activity-aware:**
```
User: I'm going hiking this afternoon in Redmond
Agent: Perfect hiking weather at 62°F! Wear athletic leggings, a moisture-wicking 
       shirt, and layers you can remove. Bring a light jacket and windproof cap 
       since winds are 18 mph. Don't forget trail shoes!
```

**With safety warning:**
```
User: What should I wear for my morning run?
Agent: ⚠️ Extreme cold warning at 18°F! Wear thermal layers, a heavy winter coat, 
       warm hat, scarf, and gloves. Protect your ears and hands, and consider 
       limiting outdoor exposure. Maybe hit the treadmill today?
```

## 🔧 Configuration Options

### User Preferences

Users can set preferences that persist across sessions:

- **Persona**: `practical`, `fashion`, `kid_friendly`
- **Comfort Profile**: `runs_cold`, `neutral`, `runs_hot`
- **Default City**: Automatically use preferred location

### Customization

Edit `weather_outfit_adk/config/settings.py` to modify:
- Default model (currently `gemini-2.0-flash-exp`)
- Cache duration
- Temperature thresholds
- Safety warning levels

## 🖥️ Frontend Interface

**Beautiful, modern chat UI** for interacting with the Weather Outfit Assistant:

- **Real-time Chat** - Interactive conversation with Coach agent
- **Quick Prompts** - Pre-filled example questions
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Error Handling** - Graceful error messages
- **Session Management** - Maintains conversation context

### Quick Start

```bash
# Run frontend server
python frontend/app.py
# Open http://localhost:5000
```

**Complete guide**: See [`frontend/README.md`](frontend/README.md)

## 📊 Observability & Monitoring

**Full observability suite integrated** with Google Cloud Monitoring:

### Three Pillars of Observability

- **Metrics** - Performance and usage tracking (Google Cloud Monitoring)
  - Agent call latency, error rates, throughput
  - Tool execution time
  - HTTP request metrics

- **Traces** - Distributed tracing (OpenTelemetry + Cloud Trace)
  - End-to-end request flow across agents
  - Agent-to-agent communication timeline
  - Bottleneck identification

- **Logs** - Structured logging (Google Cloud Logging)
  - JSON-formatted logs with context
  - Service-level log aggregation
  - Error tracking and debugging

### Features

✅ **Pre-configured dashboards** - Agent metrics visualization  
✅ **Custom metrics** - Track business and performance KPIs  
✅ **Distributed tracing** - See complete request flow  
✅ **Structured logging** - JSON logs with full context  
✅ **Alert policies** - Proactive issue detection  

### Quick Start

```python
from weather_outfit_adk.monitoring import setup_logging, setup_tracing, agent_metrics

# Setup monitoring
logger = setup_logging("my-service", enable_cloud_logging=True)
tracer = setup_tracing("my-service")

# Track metrics
with agent_metrics.measure_time("operation_name"):
    result = do_something()
```

**Complete guide**: See [`MONITORING.md`](MONITORING.md) for setup and usage

### 🔔 Alert Policies

**Automated alerting** for proactive incident response:

✅ **High Error Rate** - Alerts when error rate > 5/min (auto-converted to 0.083/sec)  
✅ **High Latency** - Alerts when P95 latency > 2000ms  
✅ **Low Success Rate** - Alerts when success rate < 10/min (auto-converted to 0.167/sec)  

```python
from weather_outfit_adk.monitoring.alerts import AlertPolicyManager

# Create all alert policies (rate-based)
manager = AlertPolicyManager(notification_channels=["CHANNEL_ID"])
alerts = manager.create_all_alerts()
```

**Note**: Default alerts track throughput rates using ALIGN_RATE. Thresholds are specified in per-minute units (e.g., 5 errors/min) and automatically converted to per-second for Google Cloud Monitoring (e.g., 0.083 errors/sec). For percentage-based alerts (error %, availability %), see [`ALERTS.md`](ALERTS.md).

**Complete guide**: See [`ALERTS.md`](ALERTS.md) for alert configuration

## 🧪 Testing

### Automated Test Suite

**Verify ADK Installation**
```bash
# Test ADK package and Agent class imports
python test_adk_imports.py
```

Expected output:
```
✅ Agent class imported from google.adk
✅ Runner class imported from google.adk
✅ App class imported from google.adk.apps
✅ Created test agent successfully
✅ Created test app successfully
✅ ALL ADK IMPORT TESTS PASSED!
```

**Comprehensive System Tests**
```bash
# Run full system test suite
python test_full_system.py
```

Expected output:
```
✅ All 5 agents operational
✅ All tools functioning
✅ Memory system integrated
✅ Schemas validated
✅ Main app ready
✅ ALL TESTS PASSED!
```

### Local Development

```bash
# Run the ADK app locally
python app.py

# The app will use mock weather data if WEATHER_API_KEY is not set
```

### Example Test Queries

1. "What should I wear in Boston?" (Basic query)
2. "I have a business meeting at 3pm in New York" (Activity + time)
3. "Going biking this evening in Portland" (Sports activity)
4. "What should my kid wear to school in Chicago?" (Persona switch)

## 🔒 Security & Privacy

- API keys managed via environment variables or Secret Manager
- User preferences stored with unique user IDs
- No PII logged in traces
- Weather data cached locally (not shared between users)

## 📚 Architecture Principles

This project follows Google's Agent Design patterns:

- **Model as Brain**: Gemini 2.0 Flash for reasoning
- **Tools as Hands**: Python functions for weather, outfit logic
- **Orchestration as Nervous System**: ADK agent framework
- **Runtime as Body**: Agent Engine for production deployment

### A2A Communication

Agents use Agent-to-Agent protocol for:
- Independent deployment and scaling
- Clean separation of concerns
- Separate session histories per agent

## ✅ Production Readiness

**All Systems Verified**
- ✅ Multi-agent architecture implemented (5 specialized agents)
- ✅ All tools and schemas validated
- ✅ Memory system integrated into Coach agent
- ✅ ADK patterns verified (correct imports, function tools)
- ✅ Comprehensive test suite passing (100%)
- ✅ Architect review approved
- ✅ Ready for Google Cloud Agent Engine deployment

**Test Coverage**
- ADK package import tests
- Agent creation tests
- Tool function tests
- Schema validation tests
- Memory system tests
- End-to-end integration tests

## 🛣️ Future Enhancements

Optional features for future iterations:
- [ ] Multi-day forecast planning
- [ ] Packing recommendations for trips
- [ ] Integration with calendar events
- [ ] Weather alert subscriptions
- [ ] Historical outfit tracking
- [ ] Frontend web interface
- [ ] Mobile app integration

## 📖 Documentation

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Agent Engine Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/quickstart)
- [A2A Protocol](https://developers.googleblog.com/en/agents-adk-agent-engine-a2a-enhancements-google-io/)

## 📄 License

This project is provided as-is for educational and demonstration purposes.

## 🙋 Support

For issues or questions:
1. Check Google Cloud Agent Engine documentation
2. Review ADK GitHub issues
3. Consult Vertex AI support

---

Built with ❤️ using Google Agent Development Kit

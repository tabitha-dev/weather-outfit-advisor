# Weather Outfit Advisor

> A Multi-Agent System Leveraging ADK, A2A Protocol, and Vertex AI Agent Engine

An intelligent clothing recommendation system that combines real-time weather data with personalized style preferences to help you dress appropriately for any occasion.

## Overview

The Weather Outfit Advisor is a capstone project demonstrating advanced AI agent architecture through a practical, user-facing application. Built using Google's Agent Development Kit (ADK) and the Agent-to-Agent (A2A) Protocol, this system showcases how specialized AI agents can collaborate to solve complex, multi-faceted problems.

### Key Features

- **Real-Time Weather Integration** - Fetches current conditions and forecasts with intelligent caching
- **Personalized Recommendations** - Adapts to individual style preferences and comfort profiles
- **Activity-Aware Suggestions** - Tailors outfit advice based on your planned activities
- **Safety Monitoring** - Provides alerts for extreme weather conditions
- **Multi-Agent Architecture** - Five specialized agents working together seamlessly
- **Production-Ready Deployment** - Hosted on Google Cloud Run with Vertex AI Agent Engine

## Architecture

### The Five-Agent System

| Agent | Model | Responsibility |
|-------|-------|----------------|
| **Coach Agent** | Gemini 2.0 Flash | User interface, orchestration, memory management |
| **Weather Agent** | Gemini 2.0 Flash | External API calls, weather data caching |
| **Stylist Agent** | Gemini 2.0 Flash | Outfit logic and style recommendations |
| **Activity Agent** | Gemini 2.0 Flash | Intent classification and activity analysis |
| **Safety Agent** | Gemini 2.0 Flash | Extreme weather monitoring and alerts |

### Design Principles

- **Agent-to-Agent (A2A) Protocol** - Decoupled microservices architecture
- **Least Privilege Security** - Each agent has restricted permissions
- **Smart Caching** - 70% reduction in API calls through intelligent data reuse
- **Context Engineering** - Persistent memory for personalized experiences
- **Quality-First** - Built-in safety, monitoring, and evaluation metrics

## Tech Stack

- **AI Framework**: Google Agent Development Kit (ADK)
- **Language Models**: Gemini 2.0 Flash (Experimental)
- **Communication**: Agent-to-Agent (A2A) Protocol
- **Deployment**: Google Cloud Run + Vertex AI Agent Engine
- **Weather API**: [Weather service integration]
- **Session Management**: Vertex AI Agent Engine Sessions
- **Monitoring**: Cloud Logging & Observability

## Project Structure

```
weather-outfit-advisor/
├── agents/
│   ├── coach_agent.py       # Main orchestrator
│   ├── weather_agent.py     # Weather data specialist
│   ├── stylist_agent.py     # Outfit recommendation engine
│   ├── activity_agent.py    # Activity classifier
│   └── safety_agent.py      # Safety monitoring
├── tools/
│   ├── weather_tools.py     # Weather API integration
│   ├── memory_tools.py      # User preferences management
│   └── outfit_tools.py      # Styling logic
├── presentation.html        # 74-page capstone documentation
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.9+
- Google Cloud Project with ADK enabled
- Vertex AI API access
- Weather API credentials

### Installation

```bash
# Clone the repository
git clone https://github.com/tabitha-dev/weather-outfit-advisor.git
cd weather-outfit-advisor

# Install dependencies
pip install google-adk-agents
pip install -r requirements.txt

# Set up environment variables
export GOOGLE_CLOUD_PROJECT="your-project-id"
export WEATHER_API_KEY="your-api-key"
```

### Usage

```python
# Initialize the Coach Agent
from agents.coach_agent import coach_agent

# Start a conversation
response = coach_agent.run("What should I wear for a morning jog today?")
print(response)
```

## Features in Detail

### Smart Weather Caching
The Weather Agent implements an in-memory cache with a 15-minute TTL, reducing external API calls by approximately 70% and dramatically improving response times (125ms vs 800ms+).

### Personalization Engine
Users can set preferences for:
- **Persona**: Practical, Fashion-forward, or Kid-friendly
- **Comfort Profile**: Temperature sensitivity and layering preferences
- **Style Constraints**: Color preferences, clothing restrictions

### Safety Guardrails
The Safety Agent monitors for:
- Extreme cold (<20°F)
- Extreme heat (>95°F)
- Strong winds (>25 mph)
- Heavy precipitation (>70% chance)
- Freezing conditions

## Production Deployment

The application is deployed on Google Cloud Run with Vertex AI Agent Engine, providing:
- **Scalability**: Auto-scaling based on demand
- **Reliability**: 99.9% uptime SLA
- **Security**: IAM-based access control
- **Observability**: Comprehensive logging and monitoring

**Live Demo**: [https://agentengine-689252953158.us-central1.run.app/](https://agentengine-689252953158.us-central1.run.app/)

## Documentation

The full capstone documentation is available in `presentation.html` - a comprehensive 74-page document covering:
- Day 1: Introduction to Agents
- Day 2: Agent Tools & Interoperability
- Day 3: Context Engineering
- Day 4: Agent Quality
- Day 5: Prototype to Production
- Technical Implementation Details
- Results & Conclusions

To view the documentation, simply open `presentation.html` in any browser.

## Learning Outcomes

This project demonstrates mastery of:
- Multi-agent system design and orchestration
- A2A Protocol implementation
- Production-grade AI deployment
- Context engineering and memory management
- Safety and quality assurance in AI systems
- MLOps best practices (caching, monitoring, evaluation)

## References

Built using insights from the Kaggle "5 Days of AI - Agents" course:
- Blount, A., et al. (2025). Introduction to Agents
- Styer, M., et al. (2025). Agent Tools and Interoperability with MCP
- Milam, K., & Gulli, A. (2025). Context Engineering Sessions and Memory
- Subasioglu, M., et al. (2025). Agent Quality
- Kartakis, S., et al. (2025). Prototype to Production

## Author

**Tabitha Khadse**
- GitHub: [@tabitha-dev](https://github.com/tabitha-dev)
- LinkedIn: [tabitha-dev](https://www.linkedin.com/in/tabitha-dev/)

## License

This project is part of a capstone demonstration for educational purposes.

---

Built with Google Agent Development Kit | Powered by Gemini 2.0 Flash

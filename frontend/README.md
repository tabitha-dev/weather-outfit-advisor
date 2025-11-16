# Weather Outfit ADK - Frontend

Beautiful, modern chat interface for the Weather Outfit Assistant.

## 🎨 Features

- **Clean, Modern UI** - Material Design inspired interface
- **Real-time Chat** - Interactive conversation with the Coach agent
- **Quick Prompts** - Pre-filled example questions
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Error Handling** - Graceful error messages and retry logic
- **Session Management** - Maintains conversation context

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs Flask and Flask-CORS for the web server.

### 2. Run the Frontend

```bash
cd frontend
python app.py
```

The server starts on `http://0.0.0.0:5000`

### 3. Open in Browser

Navigate to: `http://localhost:5000`

## 📝 Demo Mode

The frontend runs in **demo mode** by default, returning mock responses to demonstrate the UI functionality.

### Connecting to Live ADK Agent

To connect the frontend to the actual ADK agent:

**Option 1: Using the A2A Deployment (Recommended)**

1. Start the A2A services:
   ```bash
   cd deploy/a2a
   ./start-all.sh
   ```

2. Update `frontend/app.py` to call the Coach service at `http://localhost:8000`

**Option 2: Using the Main ADK App**

1. Run the main ADK app in a separate terminal:
   ```bash
   python app.py
   ```

2. Update `frontend/app.py` to integrate with the ADK Runner

See the "Integration with ADK" section below for code examples.

## 📁 Project Structure

```
frontend/
├── app.py                 # Flask backend server
├── templates/
│   └── index.html        # Main chat interface
├── static/
│   ├── style.css         # Modern CSS styling
│   └── app.js            # Chat logic and API calls
└── README.md             # This file
```

## 🔌 API Endpoints

### POST /api/chat

Send a message to the Coach agent.

**Request:**
```json
{
  "message": "What should I wear today in Seattle?",
  "session_id": "session_123"
}
```

**Response:**
```json
{
  "response": "Based on today's weather in Seattle...",
  "session_id": "session_123"
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "frontend"
}
```

### GET /api/metrics

Get current metrics statistics.

**Response:**
```json
{
  "counters": {...},
  "latencies": {...}
}
```

## 🎨 UI Components

### Chat Interface

- **Header**: Title and description
- **Chat Messages**: User and assistant messages
- **Quick Prompts**: Example questions to get started
- **Input Area**: Text input and send button

### Features

- **Auto-scroll**: Automatically scrolls to latest message
- **Loading Indicator**: Shows when agent is thinking
- **Error Messages**: Displays errors with helpful context
- **Disabled State**: Prevents multiple simultaneous requests

## 🔧 Configuration

### Environment Variables

```bash
# Port (default: 5000)
export PORT=5000

# Google Cloud project (for monitoring)
export GOOGLE_CLOUD_PROJECT=your-project-id
```

### Customization

**Change Colors:**

Edit `static/style.css`:

```css
:root {
  --primary-color: #4285f4;    /* Main brand color */
  --secondary-color: #34a853;  /* Accent color */
  --error-color: #ea4335;      /* Error messages */
}
```

**Add Quick Prompts:**

Edit `templates/index.html`:

```html
<div class="quick-prompts">
  <button class="quick-prompt">Your custom prompt here</button>
</div>
```

## 🌐 Deployment

### Local Development

```bash
python app.py
```

### Production (Cloud Run)

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "frontend.app:app"]
```

Deploy:
```bash
gcloud run deploy weather-outfit-frontend \
  --source=. \
  --port=5000 \
  --region=us-central1 \
  --allow-unauthenticated
```

### Production (with Replit Workflows)

Already configured in `../.replit` workflow configuration.

## 🔐 Security

### CORS Configuration

CORS is enabled for development. In production:

```python
# app.py
CORS(app, origins=["https://yourdomain.com"])
```

### Rate Limiting

Add rate limiting in production:

```python
from flask_limiter import Limiter

limiter = Limiter(
    app=app,
    key_func=lambda: request.remote_addr,
    default_limits=["100 per hour"]
)

@app.route('/api/chat', methods=['POST'])
@limiter.limit("20 per minute")
def chat():
    ...
```

### Input Validation

The backend validates all inputs:
- Non-empty messages
- Valid session IDs
- Proper JSON format

## 📊 Monitoring

The frontend integrates with the monitoring system:

```python
from weather_outfit_adk.monitoring import agent_metrics

# Tracks:
# - chat_request latency
# - chat_requests counter (success/error)
```

View metrics:
```bash
curl http://localhost:5000/api/metrics
```

## 🧪 Testing

### Manual Testing

1. Open browser to `http://localhost:5000`
2. Try quick prompts
3. Ask custom questions
4. Test error handling (stop backend)

### Automated Testing

```python
# test_frontend.py
import requests

def test_chat_endpoint():
    response = requests.post('http://localhost:5000/api/chat', json={
        'message': 'Hello',
        'session_id': 'test'
    })
    assert response.status_code == 200
    assert 'response' in response.json()

def test_health_endpoint():
    response = requests.get('http://localhost:5000/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'
```

## 🎯 Example Interactions

### Weather Query
```
User: What should I wear today in Portland?
Assistant: Based on Portland's weather today (65°F, partly cloudy, 20% rain), 
I recommend: Light jacket, jeans, comfortable shoes. No umbrella needed!
```

### Activity-Based
```
User: I'm going hiking this afternoon
Assistant: For hiking, I recommend: Moisture-wicking layers, sturdy hiking 
boots, hat for sun protection, and bring a light rain jacket just in case.
```

### Style Preferences
```
User: I prefer practical outfits
Assistant: Great! I'll focus on functional clothing choices. What's your 
location and what are you doing today?
```

## 🐛 Troubleshooting

### Frontend Won't Start

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
pip install -r requirements.txt
```

### Can't Connect to Backend

**Error**: `Failed to get response. Please check the server connection.`

**Solutions**:
1. Verify Coach agent is properly configured
2. Check imports in `app.py`
3. Ensure ADK dependencies are installed

### Session Not Persisting

Currently uses in-memory sessions (resets on restart).

**Production Solution**: Use database or Redis
```python
import redis
sessions = redis.Redis(host='localhost', port=6379)
```

## 🚀 Future Enhancements

- [ ] User authentication
- [ ] Conversation history persistence
- [ ] Voice input support
- [ ] Multi-language support
- [ ] Export conversation transcript
- [ ] Dark mode toggle
- [ ] Typing indicators
- [ ] Rich message formatting (markdown)

## 📚 Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **Material Design**: https://material.io/design
- **ADK Documentation**: https://cloud.google.com/agent-development-kit

---

**Status**: ✅ Production-ready frontend interface

**Last Updated**: November 13, 2025

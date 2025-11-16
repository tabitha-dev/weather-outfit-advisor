"""
Simple info server for the Weather Outfit ADK project.
The actual ADK agents run via `python app.py` or are deployed to Google Cloud Agent Engine.
This provides project information and status.
"""

from flask import Flask, jsonify, render_template_string
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Weather Outfit ADK</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            max-width: 900px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .section {
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { margin: 0 0 10px 0; }
        h2 { color: #667eea; margin-top: 0; }
        .status { 
            padding: 10px 15px;
            border-radius: 5px;
            display: inline-block;
            font-weight: bold;
        }
        .status.ready { background: #d4edda; color: #155724; }
        .status.warning { background: #fff3cd; color: #856404; }
        .agent-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .agent-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .agent-card h4 { margin: 0 0 10px 0; color: #667eea; }
        .agent-card p { margin: 5px 0; font-size: 0.9em; color: #666; }
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        .command {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            margin: 10px 0;
        }
        .badge {
            display: inline-block;
            padding: 3px 8px;
            background: #e7f3ff;
            color: #0366d6;
            border-radius: 3px;
            font-size: 0.85em;
            margin-right: 5px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🌤️ Weather Outfit ADK</h1>
        <p>Multi-Agent AI System for Weather-Based Clothing Recommendations</p>
        <p style="opacity: 0.9; margin-top: 15px;">
            Built with Google's Agent Development Kit (ADK) | Ready for Google Cloud Agent Engine
        </p>
    </div>

    <div class="section">
        <h2>📊 Project Status</h2>
        <p><span class="status {{ status_class }}">{{ status_text }}</span></p>
        <p style="margin-top: 15px;">
            {{ weather_status }}
        </p>
    </div>

    <div class="section">
        <h2>🤖 Agent Architecture</h2>
        <p>This system uses 5 specialized AI agents that communicate via Agent-to-Agent (A2A) protocol:</p>
        
        <div class="agent-list">
            <div class="agent-card">
                <h4>👔 Coach Agent</h4>
                <p>Main orchestrator</p>
                <p><span class="badge">User-facing</span></p>
            </div>
            <div class="agent-card">
                <h4>🌦️ Weather Agent</h4>
                <p>Fetches forecasts</p>
                <p><span class="badge">Caching</span></p>
            </div>
            <div class="agent-card">
                <h4>👗 Stylist Agent</h4>
                <p>Outfit planning</p>
                <p><span class="badge">Personalized</span></p>
            </div>
            <div class="agent-card">
                <h4>🏃 Activity Agent</h4>
                <p>Activity classifier</p>
                <p><span class="badge">Context-aware</span></p>
            </div>
            <div class="agent-card">
                <h4>⚠️ Safety Agent</h4>
                <p>Weather warnings</p>
                <p><span class="badge">Safety-first</span></p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>🚀 Quick Start</h2>
        
        <h3>Local Testing</h3>
        <div class="command">$ python run_test.py</div>
        <p>Run quick functionality tests</p>
        
        <div class="command">$ python test_local.py</div>
        <p>Run comprehensive agent tests</p>
        
        <div class="command">$ python app.py</div>
        <p>Start ADK development server</p>
        
        <h3>Deploy to Google Cloud</h3>
        <div class="command">$ adk deploy agent-engine \\<br>
  --project=YOUR_PROJECT_ID \\<br>
  --location=us-central1 \\<br>
  --bucket=YOUR_GCS_BUCKET</div>
        <p>Deploy to Agent Engine (see DEPLOYMENT.md for details)</p>
    </div>

    <div class="section">
        <h2>✨ Key Features</h2>
        <ul>
            <li>🎯 <strong>Activity-Aware:</strong> Recommendations based on your plans (work, hiking, dates)</li>
            <li>💾 <strong>Smart Caching:</strong> Reduces API calls with 30-minute cache</li>
            <li>⚡ <strong>Safety Warnings:</strong> Alerts for extreme weather conditions</li>
            <li>🎨 <strong>Persona Styles:</strong> Practical, fashion-focused, or kid-friendly responses</li>
            <li>🧠 <strong>Memory System:</strong> Remembers your preferences across sessions</li>
        </ul>
    </div>

    <div class="section">
        <h2>📚 Documentation</h2>
        <ul>
            <li><strong>README.md</strong> - Complete project overview</li>
            <li><strong>DEPLOYMENT.md</strong> - Google Cloud deployment guide</li>
            <li><strong>replit.md</strong> - Project state and preferences</li>
        </ul>
    </div>

    <div class="section">
        <h2>🔧 Configuration</h2>
        <p>Set these environment variables for full functionality:</p>
        <ul>
            <li><code>WEATHER_API_KEY</code> - Your weather API key (OpenWeatherMap)</li>
            <li><code>GOOGLE_CLOUD_PROJECT</code> - GCP project ID (for deployment)</li>
            <li><code>GOOGLE_CLOUD_LOCATION</code> - Deployment region (default: us-central1)</li>
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    weather_api_key = os.getenv('WEATHER_API_KEY')
    gcp_project = os.getenv('GOOGLE_CLOUD_PROJECT')
    
    if weather_api_key:
        status_text = "Ready for Deployment"
        status_class = "ready"
        weather_status = "✅ Weather API configured - Real weather data available"
    else:
        status_text = "Development Mode"
        status_class = "warning"
        weather_status = "⚠️ Using mock weather data - Set WEATHER_API_KEY for real data"
    
    return render_template_string(
        HTML_TEMPLATE,
        status_text=status_text,
        status_class=status_class,
        weather_status=weather_status
    )

@app.route('/status')
def status():
    """API endpoint for project status."""
    return jsonify({
        "project": "Weather Outfit ADK",
        "status": "operational",
        "agents": ["coach", "weather", "stylist", "activity", "safety"],
        "deployment_target": "Google Cloud Agent Engine",
        "weather_api_configured": bool(os.getenv('WEATHER_API_KEY')),
        "ready_for_deployment": bool(os.getenv('GOOGLE_CLOUD_PROJECT'))
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

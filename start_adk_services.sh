#!/bin/bash
# Start all A2A agent services

echo "🚀 Starting Weather Outfit ADK A2A Services..."
echo "================================================"

# Create logs directory
mkdir -p logs

# Start Weather Agent (Port 8001)
echo "Starting Weather Agent on port 8001..."
python deploy/a2a/weather_service/app.py > logs/weather.log 2>&1 &
WEATHER_PID=$!
echo "  ✓ Weather Agent PID: $WEATHER_PID"

sleep 2

# Start Stylist Agent (Port 8002)
echo "Starting Stylist Agent on port 8002..."
python deploy/a2a/stylist_service/app.py > logs/stylist.log 2>&1 &
STYLIST_PID=$!
echo "  ✓ Stylist Agent PID: $STYLIST_PID"

sleep 2

# Start Activity Agent (Port 8003)
echo "Starting Activity Agent on port 8003..."
python deploy/a2a/activity_service/app.py > logs/activity.log 2>&1 &
ACTIVITY_PID=$!
echo "  ✓ Activity Agent PID: $ACTIVITY_PID"

sleep 2

# Start Safety Agent (Port 8004)
echo "Starting Safety Agent on port 8004..."
python deploy/a2a/safety_service/app.py > logs/safety.log 2>&1 &
SAFETY_PID=$!
echo "  ✓ Safety Agent PID: $SAFETY_PID"

sleep 2

# Start Coach Agent (Port 8000)
echo "Starting Coach Agent on port 8000..."
python deploy/a2a/coach_service/app.py > logs/coach.log 2>&1 &
COACH_PID=$!
echo "  ✓ Coach Agent PID: $COACH_PID"

echo ""
echo "================================================"
echo "✅ All services started!"
echo "================================================"
echo ""
echo "Service URLs:"
echo "  Coach:    http://localhost:8000"
echo "  Weather:  http://localhost:8001"
echo "  Stylist:  http://localhost:8002"
echo "  Activity: http://localhost:8003"
echo "  Safety:   http://localhost:8004"
echo ""
echo "Agent Cards:"
echo "  curl http://localhost:8000/.well-known/agent.json"
echo ""
echo "PIDs saved to logs/pids.txt"
echo "$WEATHER_PID $STYLIST_PID $ACTIVITY_PID $SAFETY_PID $COACH_PID" > logs/pids.txt
echo ""
echo "To stop all services: ./stop_adk_services.sh"

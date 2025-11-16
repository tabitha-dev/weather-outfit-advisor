#!/bin/bash
# Stop all A2A agent services

echo "🛑 Stopping Weather Outfit ADK A2A Services..."

if [ -f logs/pids.txt ]; then
    PIDS=$(cat logs/pids.txt)
    for PID in $PIDS; do
        if kill -0 $PID 2>/dev/null; then
            echo "  Stopping PID $PID..."
            kill $PID
        fi
    done
    rm logs/pids.txt
    echo "✅ All services stopped!"
else
    echo "⚠️  No PID file found. Killing by port..."
    # Kill by port as fallback
    for port in 8000 8001 8002 8003 8004; do
        PID=$(lsof -ti:$port 2>/dev/null)
        if [ ! -z "$PID" ]; then
            echo "  Stopping process on port $port (PID: $PID)..."
            kill $PID 2>/dev/null || true
        fi
    done
    echo "✅ Cleanup complete!"
fi

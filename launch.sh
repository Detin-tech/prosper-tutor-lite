#!/bin/bash

# Prosper Tutor Lite Launch Script

echo "🚀 Launching Prosper Tutor Lite..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

echo "✅ Virtual environment activated"

echo "🔄 Starting FastAPI backend..."
uvicorn app.main:app --reload &
BACKEND_PID=$!

echo "🔄 Starting Streamlit frontend..."
streamlit run frontend/app.py &
FRONTEND_PID=$!

echo "✅ Backend PID: $BACKEND_PID"
echo "✅ Frontend PID: $FRONTEND_PID"

echo ""
echo "🎯 Access the application:"
echo "   Frontend: http://localhost:8501"
echo "   Backend API: http://localhost:8000"

echo ""
echo "🛑 Press Ctrl+C to stop both services"

# Wait for both processes
wait $BACKEND_PID
wait $FRONTEND_PID

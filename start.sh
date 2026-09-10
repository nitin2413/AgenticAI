#!/bin/bash

# Change directory to where the script is located
cd "$(dirname "$0")"

# Kill background processes on exit
cleanup() {
    echo -e "\nShutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup INT TERM

# Start FastAPI backend
echo "Starting FastAPI Backend on http://localhost:8000..."
./.venv/bin/uvicorn app:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!

# Wait briefly for backend startup
sleep 1

# Start Frontend dev server
echo "Starting Vite Frontend Dev Server..."
npm run dev --prefix frontend &
FRONTEND_PID=$!

# Wait for both processes
wait

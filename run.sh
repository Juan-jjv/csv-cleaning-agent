#!/usr/bin/env bash

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"


# -----------------------------
# Check Python environment
# -----------------------------

if [ ! -x ".venv/bin/python" ]; then
    echo "Error: Python virtual environment was not found."
    echo ""
    echo "Run:"
    echo "  python3 -m venv .venv"
    echo "  source .venv/bin/activate"
    echo "  python -m pip install -r requirements.txt"
    exit 1
fi


# -----------------------------
# Check npm
# -----------------------------

if ! command -v npm > /dev/null 2>&1; then
    echo "Error: npm was not found."
    exit 1
fi


# -----------------------------
# Check frontend dependencies
# -----------------------------

if [ ! -d "frontend/node_modules" ]; then
    echo "Error: Frontend dependencies are not installed."
    echo ""
    echo "Run:"
    echo "  cd frontend"
    echo "  npm install"
    exit 1
fi


# -----------------------------
# Cleanup
# -----------------------------

cleanup() {
    echo ""
    echo "Stopping CSV Cleaning Agent..."

    if [ -n "${BACKEND_PID:-}" ]; then
        kill "$BACKEND_PID" 2>/dev/null || true
        wait "$BACKEND_PID" 2>/dev/null || true
    fi
}

trap cleanup EXIT INT TERM


# -----------------------------
# Start backend
# -----------------------------

echo "Starting CSV Cleaning Agent..."
echo ""
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "Frontend: http://localhost:5173"
echo ""

echo "Starting backend..."

.venv/bin/python -m uvicorn backend.main:app \
    --host 0.0.0.0 \
    --port 8000 &

BACKEND_PID=$!


# -----------------------------
# Wait for backend port
# -----------------------------

echo "Waiting for backend..."

BACKEND_READY=false

for i in {1..30}; do

    # Make sure the backend process is still alive
    if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo "Error: Backend stopped unexpectedly."
        exit 1
    fi

    # Check whether port 8000 is accepting connections
    if .venv/bin/python - <<'PY'
import socket
import sys

try:
    with socket.create_connection(("127.0.0.1", 8000), timeout=0.5):
        sys.exit(0)
except OSError:
    sys.exit(1)
PY
    then
        BACKEND_READY=true
        break
    fi

    sleep 0.5
done


if [ "$BACKEND_READY" = false ]; then
    echo "Error: Backend did not start listening on port 8000."
    exit 1
fi


echo "Backend is ready."
echo ""
echo "Starting frontend..."


# -----------------------------
# Start frontend
# -----------------------------

npm --prefix frontend run dev
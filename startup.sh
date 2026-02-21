#!/bin/bash

# NexusAI Startup Script
# One command to start everything!

set -e

echo "🚀 Starting NexusAI..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys!"
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install Docker Compose first."
    exit 1
fi

# Start services
echo "🐳 Starting Docker services..."
docker-compose up -d

# Wait for services
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check status
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ NexusAI is running!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 Dashboard:    http://localhost:3000"
echo "📍 API Server:   http://localhost:8000"
echo "📍 API Docs:     http://localhost:8000/docs"
echo "📍 Redis:        localhost:6379"
echo "📍 PostgreSQL:   localhost:5432"
echo "📍 Ollama:       localhost:11434"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Open browser (Linux)
if command -v xdg-open &> /dev/null; then
    echo "🌐 Opening dashboard in browser..."
    xdg-open http://localhost:3000
elif command -v gnome-open &> /dev/null; then
    gnome-open http://localhost:3000
fi

# Show logs
echo "📜 Showing logs (Ctrl+C to stop watching)..."
docker-compose logs -f

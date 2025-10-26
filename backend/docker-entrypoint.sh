#!/bin/bash
set -e

echo "═══════════════════════════════════════════════════════════════"
echo "  🚀 Starting Backend Service"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Run database initialization
echo "📦 Initializing database and creating test users..."
python3 init_db.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Database initialized successfully!"
    echo ""
else
    echo ""
    echo "⚠️  Database initialization had issues, but continuing..."
    echo ""
fi

# Start the main application
echo "🚀 Starting FastAPI application..."
echo ""
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


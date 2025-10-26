#!/bin/bash

echo "🚀 Простой запуск приложения (без Docker Compose)"
echo "=================================================="
echo ""

# Kill any existing processes
echo "🛑 Остановка существующих процессов..."
pkill -f "uvicorn" 2>/dev/null
pkill -f "node.*react-scripts" 2>/dev/null
pkill -f "python.*main.py" 2>/dev/null
sudo fuser -k 8001/tcp 2>/dev/null
sudo fuser -k 3000/tcp 2>/dev/null
sudo fuser -k 80/tcp 2>/dev/null
sleep 2
echo "✅ Процессы остановлены"
echo ""

# Navigate to project directory
cd "$(dirname "$0")"
PROJECT_DIR=$(pwd)

# Check Python dependencies
echo "📦 Проверка Python зависимостей..."
cd "$PROJECT_DIR/backend"

# Install pip if needed
if ! command -v pip3 &> /dev/null; then
    echo "⚠️  Установка pip3..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

# Install Python packages
echo "⚠️  Установка Python пакетов..."
pip3 install --user fastapi uvicorn pydantic sqlalchemy alembic python-jose passlib bcrypt python-multipart scikit-learn pandas numpy python-dotenv pillow email-validator psycopg2-binary redis

echo "✅ Python зависимости готовы"
echo ""

# Set up database
echo "💾 Настройка базы данных..."
export DATABASE_URL="sqlite:///./people_search.db"
export PATH="$HOME/.local/bin:$PATH"

# Create database if it doesn't exist
if [ ! -f "people_search.db" ]; then
    echo "Создание базы данных..."
    python3 -c "
from app.database import engine, Base
from app.models import User, Profile, Interest, Skill, Match, Message
Base.metadata.create_all(bind=engine)
print('✅ База данных создана')
" 2>/dev/null || echo "⚠️  База данных может уже существовать"
fi
echo ""

# Start backend
echo "🚀 Запуск backend на порту 8001..."
cd "$PROJECT_DIR/backend"
export DATABASE_URL="sqlite:///./people_search.db"
export PATH="$HOME/.local/bin:$PATH"
nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload > "$PROJECT_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
echo "✅ Backend запущен (PID: $BACKEND_PID)"
echo "   Логи: $PROJECT_DIR/backend.log"
sleep 3
echo ""

# Check if backend is running
if curl -s http://localhost:8001/docs > /dev/null 2>&1; then
    echo "✅ Backend отвечает на http://localhost:8001"
else
    echo "⚠️  Backend всё ещё запускается..."
fi
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js не установлен"
    echo "Установка через nvm..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    nvm install 18
    nvm use 18
fi

# Start frontend
echo "🎨 Запуск frontend на порту 3000..."
cd "$PROJECT_DIR/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Установка frontend зависимостей (это может занять несколько минут)..."
    npm install
fi

# Start React app
nohup npm start > "$PROJECT_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo "✅ Frontend запущен (PID: $FRONTEND_PID)"
echo "   Логи: $PROJECT_DIR/frontend.log"
echo ""

# Wait for services to start
echo "⏳ Ожидание инициализации сервисов..."
sleep 15
echo ""

# Show status
echo "=================================================="
echo "✅ Приложение запущено!"
echo "=================================================="
echo ""
echo "📍 Точки доступа:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8001"
echo "   API Docs: http://localhost:8001/docs"
echo ""
echo "🔍 ID процессов:"
echo "   Backend:  $BACKEND_PID"
echo "   Frontend: $FRONTEND_PID"
echo ""
echo "📝 Логи:"
echo "   Backend:  tail -f $PROJECT_DIR/backend.log"
echo "   Frontend: tail -f $PROJECT_DIR/frontend.log"
echo ""
echo "🧪 Тестовые аккаунты (пароль: password123):"
echo "   john.doe@example.com (Сан-Франциско)"
echo "   jane.smith@example.com (Нью-Йорк)"
echo "   mike.wilson@example.com (Лос-Анджелес)"
echo "   sarah.johnson@example.com (Чикаго)"
echo "   alex.brown@example.com (Сиэтл)"
echo ""
echo "📌 Создать 10 тестовых пользователей:"
echo "   cd backend"
echo "   export DATABASE_URL='sqlite:///./people_search.db'"
echo "   python3 create_10_test_users.py"
echo ""
echo "🛑 Остановить: pkill -f uvicorn && pkill -f react-scripts"
echo "=================================================="


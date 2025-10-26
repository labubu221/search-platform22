#!/bin/bash

echo "🔧 Очистка портов и запуск Docker Compose"
echo "=========================================="
echo ""

# Stop all running containers
echo "🛑 Остановка всех контейнеров..."
docker-compose down 2>/dev/null || docker compose down 2>/dev/null || true
sleep 2

# Kill processes on ports
echo "🔪 Освобождение портов 3000, 8000, 80..."
sudo fuser -k 3000/tcp 2>/dev/null || true
sudo fuser -k 8000/tcp 2>/dev/null || true
sudo fuser -k 80/tcp 2>/dev/null || true
pkill -f "react-scripts" 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true
sleep 3

echo "✅ Порты освобождены"
echo ""

# Check if ports are free
echo "🔍 Проверка портов..."
if sudo lsof -i :3000 >/dev/null 2>&1; then
    echo "⚠️  Порт 3000 всё ещё занят. Пытаемся освободить снова..."
    sudo fuser -k 3000/tcp 2>/dev/null || true
    sleep 2
fi

if sudo lsof -i :8000 >/dev/null 2>&1; then
    echo "⚠️  Порт 8000 всё ещё занят. Пытаемся освободить снова..."
    sudo fuser -k 8000/tcp 2>/dev/null || true
    sleep 2
fi

echo "✅ Порты свободны"
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Check docker-compose version
echo "🐳 Проверка Docker Compose..."
if docker compose version >/dev/null 2>&1; then
    echo "✅ Используется новая версия: docker compose"
    DOCKER_COMPOSE_CMD="docker compose"
elif docker-compose --version >/dev/null 2>&1; then
    echo "⚠️  Используется старая версия: docker-compose"
    echo "   Рекомендуется обновить до 'docker compose'"
    DOCKER_COMPOSE_CMD="docker-compose"
else
    echo "❌ Docker Compose не установлен!"
    exit 1
fi
echo ""

# Start docker compose
echo "🚀 Запуск Docker Compose..."
echo "   • База данных будет инициализирована автоматически"
echo "   • 10 тестовых пользователей будут созданы автоматически"
echo "   • Пароль для всех: password123"
echo ""
$DOCKER_COMPOSE_CMD up --build

# Note: This will run in foreground. Press Ctrl+C to stop.


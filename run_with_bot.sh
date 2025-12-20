#!/bin/bash
# Скрипт для запуска Django сервера с автоматической настройкой Telegram бота

set -e  # Останавливаться при ошибках

PORT=${1:-8000}  # Порт по умолчанию 8000

echo "🚀 Запуск GGame сервера с Telegram ботом..."
echo ""

# Проверяем наличие Python
if ! command -v python &> /dev/null; then
    echo "❌ Python не найден. Установите Python"
    exit 1
fi

PYTHON_VERSION=$(python --version 2>&1)
echo "🐍 $PYTHON_VERSION"

# Проверяем наличие виртуального окружения
if [ -f "venv/bin/activate" ]; then
    echo "🔧 Активация виртуального окружения..."
    source venv/bin/activate
else
    echo "⚠️  Виртуальное окружение не найдено. Запуск без него..."
fi

# Проверяем настройки Django
echo "🔍 Проверка Django настроек..."
if python manage.py check --quiet; then
    echo "✅ Django настройки корректны"
else
    echo "❌ Ошибка в Django настройках"
    exit 1
fi

# Применяем миграции
echo "🗃️  Применение миграций..."
python manage.py migrate --verbosity 0
echo "✅ Миграции применены"

# Проверяем Telegram бота
echo "🤖 Проверка Telegram бота..."
if BOT_INFO=$(python manage.py bot_info 2>&1); then
    if echo "$BOT_INFO" | grep -q "Bot found"; then
        echo "✅ Telegram бот настроен"
        echo "$BOT_INFO"
    else
        echo "⚠️  Telegram бот не настроен или недоступен"
        echo "$BOT_INFO"
    fi
else
    echo "❌ Ошибка проверки бота"
fi

echo ""
echo "🌐 Запуск Django сервера на порту $PORT..."
echo "📱 Доступно по адресу: http://localhost:$PORT"
echo "🤖 Бот будет автоматически настроен при запуске сервера"
echo ""

# Открываем браузер в фоне (если поддерживается)
if command -v xdg-open &> /dev/null; then
    (sleep 3 && xdg-open "http://localhost:$PORT" 2>/dev/null) &
elif command -v open &> /dev/null; then
    (sleep 3 && open "http://localhost:$PORT" 2>/dev/null) &
fi

# Запускаем сервер
python manage.py runserver "0.0.0.0:$PORT"

#!/usr/bin/env python
"""
Скрипт для локального тестирования Telegram бота
Используйте ngrok для создания туннеля: ngrok http 8000
"""

import os
import subprocess
import requests
from django.conf import settings
from django.core.management import execute_from_command_line

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ggame.settings')
import django
django.setup()

def test_bot():
    """Тестирование подключения к боту"""
    print("🤖 Тестирование Telegram бота...")

    bot_token = settings.TELEGRAM_BOT_TOKEN
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN не настроен")
        return False

    try:
        # Проверка токена
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        if data.get('ok'):
            bot_info = data['result']
            print(f"✅ Бот найден: @{bot_info['username']} ({bot_info['first_name']})")
            return True
        else:
            print(f"❌ Ошибка API: {data.get('description')}")
            return False

    except requests.RequestException as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

def setup_webhook(ngrok_url=None):
    """Настройка вебхука"""
    print("\n🔗 Настройка вебхука...")

    if not ngrok_url:
        print("ℹ️  Для локального тестирования:")
        print("   1. Установите ngrok: https://ngrok.com/download")
        print("   2. Запустите: ngrok http 8000")
        print("   3. Скопируйте HTTPS URL")
        print("   4. Запустите: python test_bot_local.py https://your-ngrok-url.ngrok.io")
        return

    webhook_url = f"{ngrok_url.rstrip('/')}/api/telegram/webhook/"
    print(f"📡 Установка вебхука: {webhook_url}")

    # Запуск Django команды
    execute_from_command_line(['manage.py', 'set_webhook', '--url', webhook_url])

def start_server():
    """Запуск сервера"""
    print("\n🚀 Запуск Django сервера...")
    print("ℹ️  Сервер будет доступен на http://localhost:8000")
    print("ℹ️  Для тестирования бота используйте ngrok")

    try:
        execute_from_command_line(['manage.py', 'runserver', '8000'])
    except KeyboardInterrupt:
        print("\n👋 Сервер остановлен")

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        # Передан URL ngrok
        ngrok_url = sys.argv[1]
        if test_bot():
            setup_webhook(ngrok_url)
    else:
        # Локальное тестирование
        if test_bot():
            print("\n📋 Инструкция по тестированию:")
            print("1. Запустите ngrok: ngrok http 8000")
            print("2. Скопируйте HTTPS URL (например: https://abc123.ngrok.io)")
            print("3. Запустите: python test_bot_local.py https://abc123.ngrok.io")
            print("4. Отправьте /start боту @MerzoitCodeBot")
            print("\n❓ Или запустить сервер прямо сейчас? (y/n)")

            if input().lower() == 'y':
                start_server()

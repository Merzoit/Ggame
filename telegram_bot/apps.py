import logging
import os
from django.apps import AppConfig
from django.conf import settings

logger = logging.getLogger(__name__)


class TelegramBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_bot'

    def ready(self):
        """Автоматическая установка webhook при запуске сервера"""
        # Импортируем здесь, чтобы избежать циклических импортов
        import requests

        # Проверяем, что мы не в режиме миграций или тестов
        import sys
        if 'migrate' in sys.argv or 'makemigrations' in sys.argv or 'test' in sys.argv:
            return

        # Проверяем, что все необходимые настройки присутствуют
        bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
        webhook_url = getattr(settings, 'TELEGRAM_WEBHOOK_URL', '')

        if not bot_token:
            logger.warning('Telegram bot token not configured. Skipping webhook setup.')
            return

        if not webhook_url:
            logger.warning('Telegram webhook URL not configured. Skipping webhook setup.')
            return

        # Проверяем, является ли URL локальным (для разработки)
        is_localhost = 'localhost' in webhook_url or '127.0.0.1' in webhook_url
        if is_localhost:
            logger.info('Local webhook URL detected. Skipping automatic webhook setup.')
            logger.info('Use "python manage.py setup_bot --force" for testing or setup ngrok.')
            return

        # Формируем полный URL webhook
        full_webhook_url = f"{webhook_url.rstrip('/')}/api/telegram/webhook/"

        try:
            logger.info(f'Setting up Telegram webhook: {full_webhook_url}')

            # Проверяем, можем ли мы подключиться к Telegram API
            info_url = f"https://api.telegram.org/bot{bot_token}/getMe"
            response = requests.get(info_url, timeout=10)
            response.raise_for_status()

            bot_info = response.json()
            if not bot_info.get('ok'):
                logger.error(f'Bot API error: {bot_info.get("description")}')
                return

            # Устанавливаем webhook
            webhook_api_url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
            payload = {
                'url': full_webhook_url,
                'drop_pending_updates': True  # Игнорируем старые обновления
            }

            response = requests.post(webhook_api_url, json=payload, timeout=30)
            response.raise_for_status()

            result = response.json()
            if result.get('ok'):
                bot_name = bot_info['result'].get('username', 'Unknown')
                logger.info(f'✅ Telegram webhook successfully set for @{bot_name}')
                logger.info(f'Webhook URL: {full_webhook_url}')
            else:
                logger.error(f'❌ Failed to set webhook: {result.get("description")}')

        except requests.RequestException as e:
            logger.error(f'❌ Network error setting webhook: {e}')
        except Exception as e:
            logger.error(f'❌ Unexpected error setting webhook: {e}')

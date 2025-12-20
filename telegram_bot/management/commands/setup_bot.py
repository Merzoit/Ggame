import logging
import os
from django.core.management.base import BaseCommand
from django.conf import settings
import requests

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Настройка Telegram бота и webhook'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Принудительная настройка webhook даже для localhost',
        )
        parser.add_argument(
            '--url',
            type=str,
            help='Принудительно указать URL для webhook',
        )

    def handle(self, *args, **options):
        """Ручная настройка бота и webhook"""

        # Получаем настройки
        bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
        webhook_url = options.get('url') or getattr(settings, 'TELEGRAM_WEBHOOK_URL', '')
        frontend_url = getattr(settings, 'FRONTEND_URL', '')

        if not bot_token:
            self.stderr.write(
                self.style.ERROR('TELEGRAM_BOT_TOKEN не настроен в settings.py')
            )
            return

        self.stdout.write(
            self.style.SUCCESS(f'Bot setup: {bot_token[:10]}...')
        )

        # 1. Проверяем информацию о боте
        try:
            self.stdout.write('Getting bot info...')
            info_url = f"https://api.telegram.org/bot{bot_token}/getMe"
            response = requests.get(info_url, timeout=10)
            response.raise_for_status()

            bot_info = response.json()
            if bot_info.get('ok'):
                bot_data = bot_info['result']
                bot_username = bot_data.get('username', 'Unknown')
                bot_name = bot_data.get('first_name', 'Unknown')
                self.stdout.write(
                    self.style.SUCCESS(f'Bot found: @{bot_username} ({bot_name})')
                )
            else:
                self.stderr.write(
                    self.style.ERROR(f'Bot API error: {bot_info.get("description")}')
                )
                return

        except requests.RequestException as e:
            self.stderr.write(
                self.style.ERROR(f'Telegram API connection error: {e}')
            )
            return

        # 2. Check webhook URL
        if not webhook_url:
            self.stdout.write(
                self.style.WARNING('Webhook URL not specified. Skipping webhook setup.')
            )
            self.stdout.write(
                self.style.WARNING('Set TELEGRAM_WEBHOOK_URL in settings.py for webhook setup')
            )
            return

        # Check if URL is localhost
        is_localhost = 'localhost' in webhook_url or '127.0.0.1' in webhook_url or '0.0.0.0' in webhook_url
        if is_localhost and not options.get('force') and not getattr(settings, 'DEBUG', False):
            self.stdout.write(
                self.style.WARNING('Local webhook URL detected in production mode.')
            )
            self.stdout.write(
                self.style.WARNING('Use --force to setup anyway')
            )
            self.stdout.write(
                self.style.WARNING('Or setup ngrok for testing: ngrok http 8000')
            )
            return

        # 3. Setup webhook
        full_webhook_url = f"{webhook_url.rstrip('/')}/api/telegram/webhook/"

        try:
            self.stdout.write(f'Setting webhook: {full_webhook_url}')

            webhook_api_url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
            payload = {
                'url': full_webhook_url,
                'drop_pending_updates': True
            }

            response = requests.post(webhook_api_url, json=payload, timeout=30)
            response.raise_for_status()

            result = response.json()
            if result.get('ok'):
                self.stdout.write(
                    self.style.SUCCESS('Webhook setup successfully!')
                )
                self.stdout.write(f'URL: {full_webhook_url}')
            else:
                self.stderr.write(
                    self.style.ERROR(f'Webhook setup error: {result.get("description")}')
                )
                return

        except requests.RequestException as e:
            self.stderr.write(
                self.style.ERROR(f'Network error during webhook setup: {e}')
            )
            return

        # 4. Check frontend URL
        if frontend_url:
            self.stdout.write(
                self.style.SUCCESS(f'Frontend URL: {frontend_url}')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Frontend URL not configured')
            )

        # 5. Final message
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS('Telegram bot setup complete!')
        )
        self.stdout.write('')
        self.stdout.write('Testing:')
        self.stdout.write(f'   1. Send /start to @{bot_username}')
        self.stdout.write('   2. Click "Start Game" button')
        if frontend_url:
            self.stdout.write(f'   3. Should open: {frontend_url}/#/profile')
        self.stdout.write('')
        self.stdout.write('Management:')
        self.stdout.write('   Delete webhook: python manage.py delete_webhook')
        self.stdout.write('   Check bot: python manage.py bot_info')

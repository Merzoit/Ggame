import requests
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Установка вебхука для Telegram бота'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            help='URL для вебхука (по умолчанию из settings)',
        )

    def handle(self, *args, **options):
        bot_token = settings.TELEGRAM_BOT_TOKEN
        webhook_url = options.get('url') or f"{settings.TELEGRAM_WEBHOOK_URL}/api/telegram/webhook/"

        if not bot_token:
            self.stderr.write(
                self.style.ERROR('TELEGRAM_BOT_TOKEN не настроен в settings.py')
            )
            return

        if not webhook_url:
            self.stderr.write(
                self.style.ERROR('TELEGRAM_WEBHOOK_URL не настроен в settings.py')
            )
            return

        # Установка вебхука
        url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
        payload = {
            'url': webhook_url
        }

        try:
            self.stdout.write(f'Установка вебхука: {webhook_url}')
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()

            result = response.json()
            if result.get('ok'):
                self.stdout.write(
                    self.style.SUCCESS('Webhook successfully set!')
                )
                self.stdout.write(f'URL: {webhook_url}')
            else:
                self.stderr.write(
                    self.style.ERROR(f'Webhook error: {result.get("description")}')
                )

        except requests.RequestException as e:
            self.stderr.write(
                self.style.ERROR(f'Connection error: {e}')
            )
            return

        # Получение информации о боте
        try:
            info_url = f"https://api.telegram.org/bot{bot_token}/getMe"
            response = requests.get(info_url, timeout=10)
            response.raise_for_status()

            bot_info = response.json()
            if bot_info.get('ok'):
                bot_data = bot_info['result']
                self.stdout.write(
                    self.style.SUCCESS(f'Bot: @{bot_data.get("username")} ({bot_data.get("first_name")})')
                )
            else:
                self.stderr.write(
                    self.style.WARNING('Could not get bot info')
                )

        except requests.RequestException as e:
            self.stderr.write(
                self.style.WARNING(f'Error getting bot info: {e}')
            )

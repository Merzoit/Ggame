import requests
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Удаление вебхука для Telegram бота'

    def handle(self, *args, **options):
        bot_token = settings.TELEGRAM_BOT_TOKEN

        if not bot_token:
            self.stderr.write(
                self.style.ERROR('TELEGRAM_BOT_TOKEN не настроен в settings.py')
            )
            return

        # Удаление вебхука
        url = f"https://api.telegram.org/bot{bot_token}/deleteWebhook"

        try:
            self.stdout.write('Удаление вебхука...')
            response = requests.post(url, timeout=30)
            response.raise_for_status()

            result = response.json()
            if result.get('ok'):
                self.stdout.write(
                    self.style.SUCCESS('Webhook successfully deleted!')
                )
            else:
                self.stderr.write(
                    self.style.ERROR(f'Webhook deletion error: {result.get("description")}')
                )

        except requests.RequestException as e:
            self.stderr.write(
                self.style.ERROR(f'Connection error: {e}')
            )

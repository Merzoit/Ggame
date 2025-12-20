import requests
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Получение информации о Telegram боте'

    def handle(self, *args, **options):
        bot_token = settings.TELEGRAM_BOT_TOKEN

        if not bot_token:
            self.stderr.write(
                self.style.ERROR('TELEGRAM_BOT_TOKEN not configured in settings.py')
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
                    self.style.SUCCESS(f'Bot found: @{bot_data.get("username")} ({bot_data.get("first_name")})')
                )
                self.stdout.write(f'ID: {bot_data.get("id")}')
                self.stdout.write(f'Can join groups: {bot_data.get("can_join_groups")}')
                self.stdout.write(f'Can read messages: {bot_data.get("can_read_all_group_messages")}')
                self.stdout.write(f'Supports inline queries: {bot_data.get("supports_inline_queries")}')
            else:
                self.stderr.write(
                    self.style.ERROR(f'Bot API error: {bot_info.get("description")}')
                )

        except requests.RequestException as e:
            self.stderr.write(
                self.style.ERROR(f'Connection error: {e}')
            )

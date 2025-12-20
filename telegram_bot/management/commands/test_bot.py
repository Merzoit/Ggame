import requests
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Тестирование Telegram бота'

    def add_arguments(self, parser):
        parser.add_argument(
            '--chat-id',
            type=str,
            help='Chat ID для отправки тестового сообщения',
            required=True
        )

    def handle(self, *args, **options):
        bot_token = settings.TELEGRAM_BOT_TOKEN
        chat_id = options['chat_id']

        if not bot_token:
            self.stderr.write(
                self.style.ERROR('TELEGRAM_BOT_TOKEN не настроен в settings.py')
            )
            return

        # Получение информации о боте
        try:
            self.stdout.write('Получение информации о боте...')
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
                    self.style.ERROR('Could not get bot info')
                )
                return

        except requests.RequestException as e:
            self.stderr.write(
                self.style.ERROR(f'Error getting bot info: {e}')
            )
            return

        # Отправка тестового сообщения
        try:
            self.stdout.write(f'Отправка тестового сообщения в чат {chat_id}...')
            message_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': '🧪 Тестовое сообщение от GGame бота!\n\nБот работает корректно! ✅',
                'parse_mode': 'HTML'
            }

            response = requests.post(message_url, json=payload, timeout=10)
            response.raise_for_status()

            result = response.json()
            if result.get('ok'):
                self.stdout.write(
                    self.style.SUCCESS('Тестовое сообщение отправлено успешно!')
                )
            else:
                self.stderr.write(
                    self.style.ERROR(f'Ошибка отправки сообщения: {result.get("description")}')
                )

        except requests.RequestException as e:
            self.stderr.write(
                self.style.ERROR(f'Connection error: {e}')
            )

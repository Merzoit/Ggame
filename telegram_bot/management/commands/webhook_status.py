import requests
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Проверка статуса webhook Telegram бота'

    def handle(self, *args, **options):
        """Проверка статуса webhook"""

        bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
        if not bot_token:
            self.stderr.write(
                self.style.ERROR('TELEGRAM_BOT_TOKEN не настроен')
            )
            return

        try:
            # Получение информации о webhook
            webhook_url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
            response = requests.get(webhook_url, timeout=10)
            response.raise_for_status()

            webhook_info = response.json()
            if webhook_info.get('ok'):
                webhook_data = webhook_info['result']

                self.stdout.write(
                    self.style.SUCCESS('📡 Статус webhook:')
                )
                self.stdout.write(f'  URL: {webhook_data.get("url", "не установлен")}')
                self.stdout.write(f'  Активен: {"✅" if webhook_data.get("url") else "❌"}')
                self.stdout.write(f'  Ожидает обновлений: {webhook_data.get("pending_update_count", 0)}')

                if webhook_data.get('last_error_date'):
                    from datetime import datetime
                    error_time = datetime.fromtimestamp(webhook_data['last_error_date'])
                    self.stdout.write(f'  Последняя ошибка: {error_time}')
                    self.stdout.write(f'  Сообщение ошибки: {webhook_data.get("last_error_message", "неизвестно")}')

                if webhook_data.get('max_connections'):
                    self.stdout.write(f'  Макс. соединений: {webhook_data["max_connections"]}')

                # Проверка доступности URL
                current_url = webhook_data.get('url')
                if current_url:
                    try:
                        test_response = requests.get(f"{current_url.rstrip('/').replace('/webhook/', '/test/')}", timeout=10)
                        if test_response.status_code == 200:
                            self.stdout.write('  ✅ Webhook URL доступен')
                        else:
                            self.stdout.write(f'  ⚠️  Webhook URL вернул статус {test_response.status_code}')
                    except requests.RequestException as e:
                        self.stdout.write(f'  ❌ Ошибка доступа к webhook URL: {e}')

            else:
                self.stderr.write(
                    self.style.ERROR(f'Ошибка API: {webhook_info.get("description")}')
                )

        except requests.RequestException as e:
            self.stderr.write(
                self.style.ERROR(f'Ошибка подключения: {e}')
            )

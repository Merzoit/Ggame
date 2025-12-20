import os
import requests
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Проверка состояния деплоя и диагностика проблем'

    def handle(self, *args, **options):
        """Диагностика состояния деплоя"""

        self.stdout.write(
            self.style.SUCCESS('Deployment diagnostics GGame')
        )
        self.stdout.write('')

        # 1. Проверка переменных окружения
        self.stdout.write('Environment variables:')

        env_vars = [
            'SECRET_KEY',
            'DEBUG',
            'TELEGRAM_BOT_TOKEN',
            'TELEGRAM_WEBHOOK_URL',
            'FRONTEND_URL',
            'ALLOWED_HOSTS',
            'CORS_ALLOWED_ORIGINS',
            'DATABASE_URL'
        ]

        for var in env_vars:
            value = os.getenv(var, 'NOT SET')
            if var in ['SECRET_KEY', 'TELEGRAM_BOT_TOKEN', 'DATABASE_URL']:
                # Скрываем чувствительные данные
                if value != 'NOT SET':
                    value = f'{value[:10]}...'
            status = 'OK' if value != 'NOT SET' else 'MISSING'
            self.stdout.write(f'  {status} {var}: {value}')

        self.stdout.write('')

        # 2. Проверка Django настроек
        self.stdout.write('Django settings:')
        self.stdout.write(f'  DEBUG: {getattr(settings, "DEBUG", "not defined")}')
        self.stdout.write(f'  SECRET_KEY set: {"YES" if hasattr(settings, "SECRET_KEY") and settings.SECRET_KEY else "NO"}')

        allowed_hosts = getattr(settings, 'ALLOWED_HOSTS', [])
        self.stdout.write(f'  ALLOWED_HOSTS: {allowed_hosts}')

        cors_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', [])
        self.stdout.write(f'  CORS_ALLOWED_ORIGINS: {cors_origins}')

        self.stdout.write('')

        # 3. Проверка Telegram бота
        bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
        if bot_token:
            self.stdout.write('Telegram bot check:')

            try:
                # Получение информации о боте
                info_url = f"https://api.telegram.org/bot{bot_token}/getMe"
                response = requests.get(info_url, timeout=10)
                response.raise_for_status()

                bot_info = response.json()
                if bot_info.get('ok'):
                    bot_data = bot_info['result']
                    self.stdout.write(f'  ✅ Бот найден: @{bot_data.get("username")} ({bot_data.get("first_name")})')
                else:
                    self.stdout.write(f'  ❌ Ошибка API бота: {bot_info.get("description")}')
                    return

                # Проверка webhook
                webhook_url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
                response = requests.get(webhook_url, timeout=10)
                response.raise_for_status()

                webhook_info = response.json()
                if webhook_info.get('ok'):
                    webhook_data = webhook_info['result']
                    current_webhook = webhook_data.get('url', '')

                    if current_webhook:
                        self.stdout.write(f'  ✅ Webhook установлен: {current_webhook}')
                        self.stdout.write(f'  ⏰ Последнее обновление: {webhook_data.get("last_error_date", "неизвестно")}')
                        if webhook_data.get('last_error_message'):
                            self.stdout.write(f'  ⚠️  Последняя ошибка: {webhook_data.get("last_error_message")}')
                        else:
                            self.stdout.write('  ✅ Ошибок нет')
                    else:
                        self.stdout.write('  ❌ Webhook не установлен')
                        self.stdout.write('  💡 Рекомендация: запустите "python manage.py setup_bot"')
                else:
                    self.stdout.write(f'  ❌ Ошибка получения webhook: {webhook_info.get("description")}')

            except requests.RequestException as e:
                self.stdout.write(f'  ❌ Ошибка подключения к Telegram API: {e}')
        else:
            self.stdout.write('❌ TELEGRAM_BOT_TOKEN не установлен')

        self.stdout.write('')

        # 4. Проверка базы данных
        self.stdout.write('🗃️  Проверка базы данных:')
        try:
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            self.stdout.write('  ✅ База данных подключена')
        except Exception as e:
            self.stdout.write(f'  ❌ Ошибка базы данных: {e}')

        # 5. Проверка миграций
        try:
            from django.core.management import call_command
            from io import StringIO
            output = StringIO()
            call_command('showmigrations', stdout=output, verbosity=0)

            migrations_output = output.getvalue()
            pending_migrations = [line for line in migrations_output.split('\n') if '[ ]' in line]

            if pending_migrations:
                self.stdout.write(f'  ⚠️  Есть {len(pending_migrations)} непримененных миграций')
                for migration in pending_migrations[:3]:  # Показать первые 3
                    self.stdout.write(f'     {migration.strip()}')
                if len(pending_migrations) > 3:
                    self.stdout.write(f'     ... и еще {len(pending_migrations) - 3}')
            else:
                self.stdout.write('  ✅ Все миграции применены')

        except Exception as e:
            self.stdout.write(f'  ❌ Ошибка проверки миграций: {e}')

        self.stdout.write('')

        # 6. Рекомендации
        self.stdout.write('💡 Рекомендации:')

        debug_mode = getattr(settings, 'DEBUG', True)
        if debug_mode:
            self.stdout.write('  ⚠️  DEBUG=True - установите DEBUG=False для продакшена')

        webhook_url = getattr(settings, 'TELEGRAM_WEBHOOK_URL', '')
        if webhook_url and 'localhost' in webhook_url:
            self.stdout.write('  ⚠️  Webhook URL указывает на localhost - обновите для продакшена')

        frontend_url = getattr(settings, 'FRONTEND_URL', '')
        if not frontend_url:
            self.stdout.write('  ⚠️  FRONTEND_URL не установлен - бот не сможет открывать веб-приложение')

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS('🎯 Для исправления проблем:')
        )
        self.stdout.write('  1. Проверьте переменные окружения в Railway')
        self.stdout.write('  2. Запустите: python manage.py setup_bot')
        self.stdout.write('  3. Проверьте логи Railway в разделе "Deployments"')
        self.stdout.write('  4. Перезапустите сервис в Railway')

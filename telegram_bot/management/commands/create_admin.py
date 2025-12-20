import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import TelegramUser


class Command(BaseCommand):
    help = 'Создание суперпользователя для доступа к Django admin'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Имя пользователя для админа'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@ggame.com',
            help='Email для админа'
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Пароль для админа (если не указан, будет сгенерирован)'
        )

    def handle(self, *args, **options):
        """Создание суперпользователя"""

        username = options['username']
        email = options['email']
        password = options['password']

        # Проверяем, существует ли уже пользователь
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Пользователь {username} уже существует')
            )
            return

        # Создаем суперпользователя
        if not password:
            password = 'admin123'  # Дефолтный пароль
            self.stdout.write(
                self.style.WARNING(f'Пароль не указан. Используется: {password}')
            )

        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )

            self.stdout.write(
                self.style.SUCCESS(f'Суперпользователь {username} создан!')
            )
            self.stdout.write(f'Email: {email}')
            self.stdout.write(f'Пароль: {password}')
            self.stdout.write('')
            self.stdout.write('Доступ к админке:')
            self.stdout.write(f'URL: https://ВАШ_RAILWAY_URL/admin/')
            self.stdout.write(f'Логин: {username}')
            self.stdout.write(f'Пароль: {password}')

        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f'Ошибка создания суперпользователя: {e}')
            )

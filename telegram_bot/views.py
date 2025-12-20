import json
import logging
import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils import timezone
from users.models import TelegramUser

logger = logging.getLogger(__name__)


def send_message(chat_id, text, reply_markup=None):
    """
    Отправка сообщения в Telegram
    """
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }

    if reply_markup:
        payload['reply_markup'] = reply_markup

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Ошибка отправки сообщения: {e}")
        return None


def register_or_get_user(telegram_data):
    """
    Регистрация или получение существующего пользователя
    """
    try:
        telegram_id = telegram_data['id']
        username = telegram_data.get('username')
        first_name = telegram_data.get('first_name')
        last_name = telegram_data.get('last_name')
        language_code = telegram_data.get('language_code', 'ru')

        user, created = TelegramUser.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                'username_telegram': username,
                'first_name_telegram': first_name,
                'last_name_telegram': last_name,
                'language': language_code,
                'last_activity': timezone.now(),
                'is_active': True
            }
        )

        if not created:
            # Обновляем данные пользователя
            user.username_telegram = username
            user.first_name_telegram = first_name
            user.last_name_telegram = last_name
            user.language = language_code
            user.last_activity = timezone.now()
            user.save()

        logger.info(f"Пользователь {'создан' if created else 'обновлен'}: {user}")
        return user, created

    except Exception as e:
        logger.error(f"Ошибка создания/получения пользователя: {e}")
        return None, False


@csrf_exempt
@require_POST
def telegram_webhook(request):
    """
    Обработчик webhook от Telegram Bot API
    """
    try:
        # Получаем данные от Telegram
        data = json.loads(request.body.decode('utf-8'))
        logger.info(f"=== WEBHOOK RECEIVED ===")
        logger.info(f"Data: {data}")
        logger.info(f"Headers: {dict(request.headers)}")

        # Проверяем наличие сообщения
        if 'message' not in data:
            logger.info("No message in webhook data")
            return JsonResponse({'status': 'ok'})

        message = data['message']
        chat_id = message['chat']['id']
        text = message.get('text', '')
        from_user = message.get('from', {})

        logger.info(f"Message from {from_user.get('username', 'unknown')}: {text}")

        # Обрабатываем команду /start
        if text == '/start':
            logger.info("Processing /start command")
            # Регистрируем пользователя
            user, created = register_or_get_user(from_user)

            if user:
                logger.info(f"User registered/updated: {user.username_telegram}")

                # Создаем кнопку для открытия веб-приложения
                # URL фронтенда берем из настроек
                from django.conf import settings
                frontend_url = getattr(settings, 'FRONTEND_URL', 'https://ggame.vercel.app')
                web_app_url = f"{frontend_url}/#/profile?user_id={user.telegram_id}"

                logger.info(f"Frontend URL: {frontend_url}")
                logger.info(f"Web app URL: {web_app_url}")
                logger.info(f"User Telegram ID: {user.telegram_id}")

                reply_markup = {
                    'inline_keyboard': [[{
                        'text': '🎮 Начать игру',
                        'web_app': {
                            'url': web_app_url
                        }
                    }]]
                }

                welcome_text = f"""🎉 Добро пожаловать в GGame, {user.first_name_telegram or user.username_telegram or 'Игрок'}!

🃏 Это карточная боевая игра с коллекционными картами
💰 У вас есть {user.coins} монет и {user.gold} золота
🏆 Набрано {user.total_points} очков

Нажмите кнопку ниже, чтобы начать игру!"""

                logger.info(f"Sending welcome message to chat {chat_id}")
                result = send_message(chat_id, welcome_text, reply_markup)
                logger.info(f"Send result: {result}")

            else:
                logger.error("Failed to register user")
                send_message(chat_id, "❌ Ошибка регистрации. Попробуйте позже.")

        else:
            logger.info(f"Ignoring message: {text}")

        return JsonResponse({'status': 'ok'})

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON: {e}")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    except Exception as e:
        logger.error(f"Ошибка обработки webhook: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

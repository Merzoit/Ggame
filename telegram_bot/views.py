import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def telegram_webhook(request):
    """
    Обработчик webhook от Telegram Bot API
    """
    try:
        # Получаем данные от Telegram
        data = json.loads(request.body.decode('utf-8'))
        logger.info(f"Получены данные от Telegram: {data}")

        # Здесь будет логика обработки сообщений
        # Пока просто логируем и возвращаем OK

        return JsonResponse({'status': 'ok'})

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON: {e}")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    except Exception as e:
        logger.error(f"Ошибка обработки webhook: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

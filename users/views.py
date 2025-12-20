from django.http import JsonResponse
from django.views.decorators.http import require_GET
from users.models import TelegramUser
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_by_telegram_id(request, telegram_id):
    """
    Получить данные пользователя по Telegram ID
    """
    try:
        user = TelegramUser.objects.get(telegram_id=telegram_id)

        # Формируем данные пользователя
        user_data = {
            'id': user.id,
            'telegram_id': user.telegram_id,
            'username_telegram': user.username_telegram,
            'first_name_telegram': user.first_name_telegram,
            'last_name_telegram': user.last_name_telegram,
            'coins': user.coins,
            'gold': user.gold,
            'total_points': user.total_points,
            'date_joined_telegram': user.date_joined.date().isoformat() if user.date_joined else None,
            'last_activity': user.last_activity.isoformat() if user.last_activity else None,
            'is_active': user.is_active,
            'language': user.language,
            'notifications_enabled': user.notifications_enabled,
            # Статистика (добавим поля по умолчанию, если их нет в модели)
            'total_games': getattr(user, 'total_games', 0),
            'games_won': getattr(user, 'games_won', 0),
            'current_streak': getattr(user, 'current_streak', 0),
            'best_streak': getattr(user, 'best_streak', 0),
        }

        return JsonResponse(user_data)

    except TelegramUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

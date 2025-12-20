from django.urls import path
from django.http import JsonResponse
from . import views

def test_webhook(request):
    """Тестовый эндпоинт для проверки работы webhook"""
    return JsonResponse({
        'status': 'ok',
        'message': 'Telegram webhook is working',
        'timestamp': '2025-01-01T00:00:00Z'
    })

def create_admin_endpoint(request):
    """Временный эндпоинт для создания суперпользователя (ТОЛЬКО ДЛЯ НАСТРОЙКИ!)"""
    from django.contrib.auth import get_user_model
    from django.http import JsonResponse

    # Проверяем, что эндпоинт вызывается с правильным ключом
    setup_key = request.GET.get('key')
    if setup_key != 'ggame_setup_2025':
        return JsonResponse({'error': 'Invalid setup key'}, status=403)

    User = get_user_model()

    # Проверяем, существует ли уже админ
    if User.objects.filter(username='admin').exists():
        return JsonResponse({
            'status': 'warning',
            'message': 'Admin user already exists',
            'login': 'admin',
            'password': 'admin123',
            'admin_url': 'https://web-production-051b.up.railway.app/admin/'
        })

    try:
        # Создаем суперпользователя
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@ggame.com',
            password='admin123'
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Admin user created successfully',
            'login': 'admin',
            'password': 'admin123',
            'admin_url': 'https://web-production-051b.up.railway.app/admin/'
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

urlpatterns = [
    path('webhook/', views.telegram_webhook, name='telegram_webhook'),
    path('test/', test_webhook, name='test_webhook'),
    path('create_admin/', create_admin_endpoint, name='create_admin'),
]

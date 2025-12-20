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

urlpatterns = [
    path('webhook/', views.telegram_webhook, name='telegram_webhook'),
    path('test/', test_webhook, name='test_webhook'),
]

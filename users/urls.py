from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Создаем роутер для API пользователей
router = DefaultRouter()
# router.register(r'users', views.UserViewSet)  # Добавим позже

urlpatterns = [
    path('', include(router.urls)),
    path('by_telegram/<int:telegram_id>/', views.get_user_by_telegram_id, name='user_by_telegram'),
]

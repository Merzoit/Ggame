from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Создаем роутер для API пользователей
router = DefaultRouter()
# router.register(r'users', views.UserViewSet)  # Добавим позже

urlpatterns = [
    path('', include(router.urls)),
]

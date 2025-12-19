from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Создаем роутер для API
router = DefaultRouter()
router.register(r'templates', views.CardTemplateViewSet)
router.register(r'instances', views.CardInstanceViewSet, basename='cardinstance')

urlpatterns = [
    path('', include(router.urls)),
]

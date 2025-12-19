from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Создаем роутер для API
router = DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'inventory', views.InventoryItemViewSet, basename='inventory')

urlpatterns = [
    path('', include(router.urls)),
]

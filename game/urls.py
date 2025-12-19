from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Создаем роутер для API
router = DefaultRouter()
router.register(r'games', views.GameSessionViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'rounds', views.GameRoundViewSet)
router.register(r'answers', views.AnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

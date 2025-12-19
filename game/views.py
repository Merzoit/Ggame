from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import GameSession, PlayerInGame, Question, GameRound, Answer
from .serializers import (
    GameSessionSerializer, PlayerInGameSerializer,
    QuestionSerializer, GameRoundSerializer, AnswerSerializer
)


class GameSessionViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления игровыми сессиями
    """
    queryset = GameSession.objects.all()
    serializer_class = GameSessionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Присоединиться к игре"""
        game_session = self.get_object()
        user = request.user

        if game_session.players.count() >= game_session.max_players:
            return Response(
                {'error': 'Игра заполнена'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if game_session.players.filter(id=user.id).exists():
            return Response(
                {'error': 'Вы уже в игре'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Добавляем игрока в игру
        PlayerInGame.objects.create(player=user, game_session=game_session)

        serializer = self.get_serializer(game_session)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Начать игру"""
        game_session = self.get_object()

        if game_session.start_game():
            serializer = self.get_serializer(game_session)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'Невозможно начать игру'},
                status=status.HTTP_400_BAD_REQUEST
            )


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра вопросов
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]


class GameRoundViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра раундов игры
    """
    queryset = GameRound.objects.all()
    serializer_class = GameRoundSerializer
    permission_classes = [IsAuthenticated]


class AnswerViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления ответами
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(player=self.request.user)

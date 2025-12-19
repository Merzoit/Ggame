from rest_framework import serializers
from .models import GameSession, PlayerInGame, Question, GameRound, Answer
from users.models import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя Telegram"""

    class Meta:
        model = TelegramUser
        fields = [
            'id', 'telegram_id', 'username_telegram',
            'first_name_telegram', 'last_name_telegram',
            'total_games', 'games_won', 'total_points',
            'current_streak', 'best_streak'
        ]


class PlayerInGameSerializer(serializers.ModelSerializer):
    """Сериализатор для игрока в игре"""
    player = TelegramUserSerializer(read_only=True)

    class Meta:
        model = PlayerInGame
        fields = ['player', 'joined_at', 'points', 'is_ready']


class GameSessionSerializer(serializers.ModelSerializer):
    """Сериализатор для игровой сессии"""
    players = PlayerInGameSerializer(source='player_in_game', many=True, read_only=True)
    players_count = serializers.SerializerMethodField()

    class Meta:
        model = GameSession
        fields = [
            'id', 'status', 'max_players', 'players_count',
            'players', 'time_limit', 'points_for_win',
            'telegram_chat_id', 'created_at', 'started_at', 'finished_at'
        ]
        read_only_fields = ['id', 'created_at', 'started_at', 'finished_at']

    def get_players_count(self, obj):
        return obj.players.count()


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для вопроса"""

    class Meta:
        model = Question
        fields = [
            'id', 'text', 'difficulty', 'category',
            'times_asked', 'correct_answers'
        ]


class GameRoundSerializer(serializers.ModelSerializer):
    """Сериализатор для раунда игры"""
    question = QuestionSerializer(read_only=True)
    answers = serializers.SerializerMethodField()

    class Meta:
        model = GameRound
        fields = [
            'id', 'game_session', 'question', 'round_number',
            'started_at', 'time_limit_seconds', 'answers'
        ]

    def get_answers(self, obj):
        answers = obj.answers.all()
        return AnswerSerializer(answers, many=True).data


class AnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для ответа"""
    player = TelegramUserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = [
            'id', 'player', 'game_round', 'answer_text',
            'is_correct', 'points_earned', 'answered_at'
        ]
        read_only_fields = ['id', 'is_correct', 'points_earned', 'answered_at']

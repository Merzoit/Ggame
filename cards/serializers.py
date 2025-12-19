from rest_framework import serializers
from .models import AnimeUniverse, Season, CardTemplate, CardInstance


class AnimeUniverseSerializer(serializers.ModelSerializer):
    """Сериализатор для аниме-вселенных"""
    seasons_count = serializers.SerializerMethodField()

    class Meta:
        model = AnimeUniverse
        fields = ['id', 'name', 'description', 'logo_url', 'is_active', 'seasons_count']

    def get_seasons_count(self, obj):
        return obj.seasons.filter(is_active=True).count()


class SeasonSerializer(serializers.ModelSerializer):
    """Сериализатор для сезонов"""
    anime_universe_name = serializers.CharField(
        source='anime_universe.name',
        read_only=True
    )

    class Meta:
        model = Season
        fields = ['id', 'anime_universe', 'anime_universe_name', 'name', 'season_number', 'is_active']


class CardTemplateSerializer(serializers.ModelSerializer):
    """Сериализатор для шаблонов карт"""
    anime_universe_name = serializers.CharField(
        source='anime_universe.name',
        read_only=True
    )
    season_name = serializers.CharField(
        source='season.name',
        read_only=True
    )

    class Meta:
        model = CardTemplate
        fields = [
            'id', 'name', 'description', 'image_url',
            'anime_universe', 'anime_universe_name', 'season', 'season_name',
            'element', 'health_min', 'health_max', 'attack_min', 'attack_max',
            'defense_min', 'defense_max', 'coin_cost', 'gold_cost', 'sell_price'
        ]


class CardInstanceSerializer(serializers.ModelSerializer):
    """Сериализатор для экземпляров карт"""
    template = CardTemplateSerializer(read_only=True)
    owner_username = serializers.CharField(
        source='owner.username_telegram',
        read_only=True
    )
    is_alive = serializers.SerializerMethodField()

    class Meta:
        model = CardInstance
        fields = [
            'id', 'template', 'owner', 'owner_username',
            'health', 'attack', 'defense', 'current_health',
            'is_alive', 'is_in_deck', 'level', 'experience',
            'acquired_at', 'last_used'
        ]
        read_only_fields = [
            'id', 'owner', 'health', 'attack', 'defense',
            'acquired_at', 'last_used'
        ]

    def get_is_alive(self, obj):
        return obj.is_alive()

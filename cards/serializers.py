from rest_framework import serializers
from .models import AnimeUniverse, Season, CardTemplate, CardInstance, Deck, DeckCard


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


class DeckSerializer(serializers.ModelSerializer):
    """Сериализатор для колод"""
    owner_username = serializers.CharField(
        source='owner.username_telegram',
        read_only=True
    )
    cards_count = serializers.SerializerMethodField()
    total_stats = serializers.SerializerMethodField()
    is_valid_deck = serializers.SerializerMethodField()
    cards = serializers.SerializerMethodField()

    class Meta:
        model = Deck
        fields = [
            'id', 'owner', 'owner_username', 'name', 'description',
            'is_active', 'cards_count', 'total_stats', 'is_valid_deck',
            'cards', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']

    def get_cards_count(self, obj):
        return obj.deck_cards.count()

    def get_total_stats(self, obj):
        return obj.get_total_stats()

    def get_is_valid_deck(self, obj):
        valid, message = obj.is_valid()
        return {'valid': valid, 'message': message}

    def get_cards(self, obj):
        deck_cards = obj.deck_cards.select_related('card__template').all()
        return DeckCardSerializer(deck_cards, many=True).data


class DeckCardSerializer(serializers.ModelSerializer):
    """Сериализатор для карт в колоде"""
    card_info = serializers.SerializerMethodField()

    class Meta:
        model = DeckCard
        fields = ['id', 'deck', 'card', 'position', 'card_info']
        read_only_fields = ['id']

    def get_card_info(self, obj):
        return {
            'id': obj.card.id,
            'template_name': obj.card.template.name,
            'health': obj.card.health,
            'attack': obj.card.attack,
            'defense': obj.card.defense,
            'element': obj.card.template.element,
            'anime_universe': obj.card.template.anime_universe.name,
            'season': obj.card.template.season.name
        }

from rest_framework import serializers
from .models import CardTemplate, CardInstance


class CardTemplateSerializer(serializers.ModelSerializer):
    """Сериализатор для шаблонов карт"""

    class Meta:
        model = CardTemplate
        fields = [
            'id', 'name', 'description', 'image_url',
            'anime_universe', 'season', 'rarity', 'element',
            'health_min', 'health_max', 'attack_min', 'attack_max',
            'defense_min', 'defense_max', 'coin_cost', 'gold_cost'
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

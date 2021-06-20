from api.models import Match, Sport, Market, Selection
from rest_framework import serializers


class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ('id', 'name')


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ('id', 'name', 'odds')


class MarketSerializer(serializers.ModelSerializer):
    # Nested serialization
    selections = SelectionSerializer(many=True)

    class Meta:
        model = Market
        fields = ('id', 'name', 'selections',)


# User two match serializers - one for more data, one for less. 
class MatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('id', 'url', 'name', 'start_time',)

class MatchDetailSerializer(serializers.ModelSerializer):
    # Nest serialization
    sport = SportSerializer()
    market = MarketSerializer()

    class Meta:
        model = Match
        fields = ('id', 'url', 'name', 'start_time', 'sport', 'market',)



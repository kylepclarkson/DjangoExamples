from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    """ Out data """
    class Meta:
        model = Room
        fields = ['id', 'code', 'host', 'guest_can_pause', 'votes_to_skip', 'created_at']


class CreateRoomSerializer(serializers.ModelSerializer):
    """ Serialize data from request """
    class Meta:
        model = Room
        # Note user id is stored as session id.
        fields = ('guest_can_pause', 'votes_to_skip')




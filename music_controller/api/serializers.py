from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    """ Out data """
    class Meta:
        model = Room
        fields = ['id', 'code', 'host', 'guest_can_pause', 'votes_to_skip', 'created_at']


class CreateRoomSerializer(serializers.ModelSerializer):
    """ Serialize data from request to create room. """
    class Meta:
        model = Room
        # Note user id is stored as session id.
        fields = ('guest_can_pause', 'votes_to_skip')


class UpdateRoomSerializer(serializers.ModelSerializer):
    """ Serialize data from request to update room. """
    # Note: Need to 'dereference' the code field of the model as it is unique. 
    code = serializers.CharField(validators=[])
    class Meta:
        model = Room
        # Note user id is stored as session id.
        fields = ('guest_can_pause', 'votes_to_skip', 'code')






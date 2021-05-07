from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Room
from .serializers import RoomSerializer, CreateRoomSerializer


class RoomView(generics.ListAPIView):
    """ Get all room objects. """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CreateRoomView(APIView):

    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            # create session
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key

            query_set = Room.objects.filter(host=host)
            if query_set.exists():
                # update room
                room = query_set[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
            else:
                # create room
                room = Room(host=host, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
                room.save()

            # return created/updated room, serialized
            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)



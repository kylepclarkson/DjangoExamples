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


class GetRoom(APIView):
    """ Get Room using code value in request. """

    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            room = Room.objects.filter(code=code)
            if len(room) == 1:
                # send data to frontend
                data = RoomSerializer(room[0]).data
                # check if user of session is host of room
                data['is_host'] = self.request.session.session_key == room[0].host
                return Response(data, status=status.HTTP_200_OK)

            # room dne.
            return Response({'Room Not Found': 'Invalid Room Code.'}, status=status.HTTP_404_NOT_FOUND)
        # bad request
        return Response({'Bad Request': 'Code parameter not found.'}, status=status.HTTP_400_BAD_REQUEST)


class JoinRoom(APIView):
    """ Join room using code stored in user's session object. """
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            # create session
            self.request.session.create()

        # room code
        code = request.data.get('code')

        if code is not None:
            room_result = Room.objects.filter(code=code)
            if len(room_result) == 1:
                room = room_result[0]
                # set room in user's session.
                self.request.session['room_code'] = code
                return Response({"message": 'Room Joined!'}, status=status.HTTP_200_OK)

            return Response({'Bad Request': 'Invalid Room Code'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'Bad Request': 'Invalid post data, did not find a code key'}, status=status.HTTP_400_BAD_REQUEST)


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
                # set room in user's session.
                self.request.session['room_code'] = room.code
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
            else:
                # create room
                room = Room(host=host, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
                room.save()
                # set room in user's session.
                self.request.session['room_code'] = room.code

            # return created/updated room, serialized
            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)



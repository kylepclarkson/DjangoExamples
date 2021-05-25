from django.shortcuts import render, redirect
from requests import Request, post
from rest_framework import response

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .credentials import REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
from .util import *
from api.models import Room

class AuthURL(APIView):
    """ Requests access to a user's Spotify account """
    def get(self, request, format=None):
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'
        
        # prepare request code with the above scopes. Sent from front end. 
        url = Request('GET',
        'https://accounts.spotify.com/authorize',
        params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)


def spotify_callback(request, format=None):
    """ Get response from the above request. """

    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://acounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    # update or create user token
    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(request.session.session_key, access_token, token_type, expires_in, refresh_token)

    return redirect('frontend:') 


class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)


class CurrentSong(APIView):
    """ Get current song of room """
    def get(self, request, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)[0]
        host = room.host
        endpoint = 'player/currently-playing'
        # get request.
        response = execute_spotify_api_request(host, endpoint)

        print(response)

        return Response({}, status=status.HTTP_200_OK)





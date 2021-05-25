from django.utils import timezone
from datetime import timedelta
from requests import post, put, get

from .credentials import CLIENT_ID, CLIENT_SECRET 
from .models import SpotifyToken

BASE_URL = 'https://api.spotify.com/v1/me/'

def get_user_tokens(session_id):
    """ Get model instance if it exists using session id """
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None

def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):

    tokens = get_user_tokens(session_id)
    # update expiry date of tokens.
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens: 
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        # is updated token type needed?
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in',])
    else:
        tokens = SpotifyToken(
            user=session_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
            token_type=token_type,
        )
        tokens.save()


def is_spotify_authenticated(session_id):
    """ Check if user is authenticated """
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry < timezone.now():
            # update token of authenticated user.
            refresh_spotify_token(session_id)
            return True
    return False
    

def refresh_spotify_token(session_id):
    """ Get updated access tokens. """
    
    refresh_token = get_user_tokens(session_id).refresh_token

    response = post('https://accounts.spotify.com/api/token', data={
        'grant-type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    refresh_token = response.get('refresh_token')

    update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token)


def execute_spotify_api_request(session_id, endpoint, post_=False, put_=False):
    """ A single function to handle different interview requests. """
    tokens = get_user_tokens(session_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + tokens.access_token 
    }

    if post_:
        # send post request
        post(BASE_URL + endpoint, headers=headers)

    if put_:
        # send put
        put(BASE_URL + endpoint, headers=headers)

    # else get
    response = get(BASE_URL + endpoint, {}, headers=headers)
    try: 
        return response.json()
    except:
        return {'Error': 'Issue with request.'}

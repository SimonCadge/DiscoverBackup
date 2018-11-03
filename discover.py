import sys
import spotipy
from spotipy import oauth2
import spotipy.util as util
from export import SPOTIPY_USERNAME, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

scope = 'playlist-modify-private'

sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=scope, cache_path='.spotipyoauthcache')

tokenInfo = sp_oauth.get_cached_token()
if not tokenInfo:
    url = sp_oauth.get_authorize_url()
    print(url)
    response = input('Paste the link above into the browser and then paste the redirect url here')
    accessCode = sp_oauth.parse_response_code(response)
    if accessCode:
        tokenInfo = sp_oauth.get_access_token(accessCode)

if tokenInfo:
    if sp_oauth._is_token_expired(tokenInfo):
        tokenInfo = sp_oauth.refresh_access_token(tokenInfo['refresh_token'])
    token = tokenInfo['access_token']
    sp = spotipy.Spotify(token)
    me = sp.current_user()
    DiscoverWeekly = sp.user_playlist(me['id'], playlist_id='37i9dQZEVXcX499rnDI26o')
    print(DiscoverWeekly)
    #playlists = sp.current_user_playlists(limit=0)
    #for playlist in playlists['items']:
    #    print(playlist['name'])

else:
    print('Fail')
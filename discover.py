import sys
import datetime
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
    if sp_oauth.is_token_expired(tokenInfo):
        tokenInfo = sp_oauth.refresh_access_token(tokenInfo['refresh_token'])
    token = tokenInfo['access_token']
    sp = spotipy.Spotify(token)
    me = sp.current_user()
    found = False
    x = 0
    playlistID=''
    while playlistID == '':
        playlists = sp.current_user_playlists(offset=50*x)
        if not playlists['items']:
            print('Error')
            break
        else:
            for playlist in playlists['items']:
                if playlist['name'] == 'Discover Weekly':
                    playlistID = playlist['id']
            x += 1
    if not playlistID == '':
        tracks = []
        discoverWeekly = sp.user_playlist_tracks(me['id'], playlist_id=playlistID, fields='items(track(name, id))')
        for item in discoverWeekly['items']:
            track = item['track']
            tracks.append(track['id'])
        date = datetime.date.today().isoformat()
        backupName = 'Rediscover ' + date
        backup = sp.user_playlist_create(me['id'], backupName, public=False, description='Backup of my Discover Weekly from ' + date)
        sp.user_playlist_add_tracks(me['id'], backup['id'], tracks)
else:
    print('Fail')
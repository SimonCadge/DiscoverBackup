import sys
import spotipy
import spotipy.util as util
from export import SPOTIPY_USERNAME, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

readScope = 'playlist-read-private'
writeScope = 'playlist-modify-private'

readToken = util.prompt_for_user_token(SPOTIPY_USERNAME, readScope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)
writeToken = util.prompt_for_user_token(SPOTIPY_USERNAME, writeScope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

if readToken:
    spRead = spotipy.Spotify(auth=readToken)
    print(spRead.current_user_playlists())
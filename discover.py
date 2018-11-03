import sys
import os
import datetime
import spotipy
from spotipy import oauth2
import spotipy.util as util
from export import SPOTIPY_USERNAME, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

scope = 'playlist-modify-private'

def backup():
    #Get the path to the Discover Weekly folder. Ensures that the cache path is correct no matter where the script is executed from.
    cwd = os.path.dirname(os.path.realpath(__file__))
    cachePath = cwd + '/.spotipyoauthcache'

    sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=scope, cache_path=cachePath)

    #Attempting to get a cached token
    tokenInfo = sp_oauth.get_cached_token()
    if not tokenInfo:
        #Getting the url the user needs to paste into their browser for authorisation.
        url = sp_oauth.get_authorize_url()
        print(url)
        #Getting the response from the user.
        response = input('Paste the link above into the browser and then paste the redirect url here')
        accessCode = sp_oauth.parse_response_code(response)
        if accessCode:
            #Create token from the access code.
            tokenInfo = sp_oauth.get_access_token(accessCode)

    #By this point a token should have been found or created.
    if tokenInfo:
        #The token times out periodically and needs to be refreshed.
        if sp_oauth.is_token_expired(tokenInfo):
            tokenInfo = sp_oauth.refresh_access_token(tokenInfo['refresh_token'])
        token = tokenInfo['access_token']
        #Interface with the spotify api using the authorisation token. Our token allows us to modify playlists.
        sp = spotipy.Spotify(token)
        #Get information about current user, importantly id.
        me = sp.current_user()
        x = 0
        playlistID=''
        while playlistID == '':
            #Get the playlists in sets of 50, searching for the 'Discover Weekly' playlist.
            playlists = sp.current_user_playlists(offset=50*x)
            #If the api call hasn't returned any items we've got to the end of the playlists.
            if not playlists['items']:
                print('Error')
                break
            else:
                #Iterate through the playlists.
                for playlist in playlists['items']:
                    if playlist['name'] == 'Discover Weekly':
                        #We've found the playlist id.
                        playlistID = playlist['id']
                x += 1
        #Assuming we've found the playlist id by now.
        if not playlistID == '':
            tracks = []
            #Get info about the tracks in the playlist.
            discoverWeekly = sp.user_playlist_tracks(me['id'], playlist_id=playlistID, fields='items(track(name, id))')
            for item in discoverWeekly['items']:
                #Add each track id to a list.
                track = item['track']
                tracks.append(track['id'])
            #Use the date to create the name and description of the new playlist.
            date = datetime.date.today().isoformat()
            backupName = 'Rediscover ' + date
            #Create new playlist with the generated name and description.
            backup = sp.user_playlist_create(me['id'], backupName, public=False, description='Backup of my Discover Weekly from ' + date)
            #Add to the playlist the tracks we got from the original Discover Weekly playlist.
            sp.user_playlist_add_tracks(me['id'], backup['id'], tracks)
        print("Success!")
    else:
        print('Fail')
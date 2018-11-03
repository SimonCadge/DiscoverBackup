# DiscoverBackup
Python script to Backup my Discover Weekly each friday.

Using the Spotipy wrapper for the Spotify RESTful Web API
https://github.com/plamere/spotipy

To use it you need to have spotipy installed. pip install spotipy works, but currently it's broken and it will install a version from years ago.

Download the zip from the github page and place the Spotipy folder into the Discover Weekly folder. That works for me.

Furthermore, you need to create your own export.py file. It just needs to define the following:
1. SPOTIPY_CLIENT_ID
2. SPOTIPY_CLIENT_SECRET
3. SPOTIPY_REDIRECT_URI
4. SPOTIFY_USERNAME

The first two you get from here https://developer.spotify.com/my-applications/#!/applications. You need to sign up for an application. When you have done so you need to add a redirect uri to it, and it's ok to just use http://localhost/.

The username is, of course, your username.

I personally have hosted the whole thing on a free account on the website called pythonanywhere. This is why I have the run.py file, since pythonanywhere supports daily tasks but I don't want the backup to be created daily. As such my run.py file will only execute the actual backup functionality on fridays.

With this I can forget about it. Each week it will create a backup.

"""
Creates and adds songs to user's playlists

Needs user_id, playlist_name, public, collaborative, description
"""

import json
import requests
import main

# =================
# Create playlist
# =================

def make_playlist_data(name, description = '', public = True, collaborative = False):
    """
    Creates a data dictionary for a create playlist request.

    name: string, required
    public: boolean, sets if public or not
    collaborative: boolean, sets if others can add or delete songs
    description: string
    """
    
    data = {
        'name': name,
        'public': public,
        'collaborative': collaborative,
        'description': description
    }

    return data

def create_playlist(authorization_header, user_id, data):
    # Creates a playlist in the account of the specified user id. Data should be taken from the return value of make_playlist_data.

    cplaylist_api_endpoint = "{}/users/{}/playlists".format(main.SPOTIFY_API_URL, user_id)
    cplaylist_response = requests.post(cplaylist_api_endpoint, headers=authorization_header, json = data)
    return json.loads(cplaylist_response.text)

# ======================
# Add song to playlist
# ======================

def add_song(authorization_header, playlist_id, song_id):
    # Adds song to the end of the playlist.
    # Song is a string of the song id.

    data = {
        'uris': ["spotify:track:" + song_id]
    }

    song_api_endpoint = "{}/playlists/{}/tracks".format(main.SPOTIFY_API_URL, playlist_id)
    song_response = requests.post(song_api_endpoint, headers=authorization_header, json = data)
    return json.loads(song_response.text)
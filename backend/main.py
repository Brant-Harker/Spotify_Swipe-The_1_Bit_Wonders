"""
Main file for backend. Authentification and all End Nodes.

References:
Authentication with Spotify API:
https://github.com/drshrey/spotify-flask-auth-example/blob/master/main.py
"""

import json
from flask import Flask, request, redirect, g, render_template, jsonify
import requests
from urllib.parse import quote
from flask_cors import CORS
import playlists

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

#  Client Keys
CLIENT_ID = "980aa9bf0ae54f888ba9fb79bf1ba8b9"
CLIENT_SECRET = "57fcc1ddddff4f71b3d3a57494541ec0"

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "ugc-image-upload user-library-modify playlist-modify-private playlist-modify-public streaming"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

# User Parameters
authorization_header = None
profile_data = None
playlist_id = None
playlist_name = None
playlist_description = None
songs_added = []

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

AUTH_URL = 'https://accounts.spotify.com/api/token'

#hardcode seeds
seed_artists = []
seed_genres = []
seed_tracks = ['0c6xIDDpzE81m2q797ordA']


def createplaylist(name, description=""):
    # Get user ID
    user_id = profile_data["id"]

    print("Creating playlist for user {}".format(user_id))
    print("Playlist name: {}".format(name))
    print("Playlist description: {}".format(description))

    # Get user playlist data
    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    playlist_data = json.loads(playlists_response.text)

    # Create Playlist
    created_data = playlists.create_playlist(authorization_header, user_id, playlists.make_playlist_data(name, description))

    global playlist_id
    playlist_id = created_data["id"]

    print("Created playlist with id {}".format(playlist_id))

    # Combine profile and playlist data to display
    display_arr = [profile_data] + [created_data]
    # return render_template("index.html", sorted_array=display_arr)
    return jsonify(display_arr)


@app.route("/", methods=['GET', 'POST'])
def index():
    # Get arguments from url (seed-track, playlist-name, playlist-description)
    if request.method == 'POST':
        global playlist_name
        global playlist_description

        seed_track = request.form['seed-track']
        playlist_name = request.form['playlist-name']
        playlist_description = request.form['playlist-description']

        # Extract track id from url
        # Example url https://open.spotify.com/track/1K39t0GGnHiblUh8XZjNM3?si=7425eb3e5dc348a1
        track_id = seed_track.split('/')[4].split('?')[0]

        # If all arguments are given, redirect to route(/)
        if seed_track and playlist_name:
            return redirect('/auth')

    return render_template('setup.html')


@app.route("/auth")
def auth():
    # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    print(auth_url)
    return redirect(auth_url)


# Create an app route to render the app page
@app.route("/webapp")
def webapp():
    return render_template('app.html')


@app.route("/callback/q")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    # refresh_token = response_data["refresh_token"]
    # token_type = response_data["token_type"]
    # expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    global authorization_header
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    # Get profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    global profile_data
    profile_data = json.loads(profile_response.text)
    # return jsonify(profile_data)
    # redirect to webapp route
    # Create playlist
    createplaylist(playlist_name, playlist_description)

    return redirect('/webapp')


# @app.route("/api/createplaylist")
# def createplaylist():
#     # Get playlist name from url
#     playlist_name = request.args.get('name')

#     # Get user ID
#     user_id = profile_data["id"]

#     # Get user playlist data
#     playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
#     playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
#     playlist_data = json.loads(playlists_response.text)

#     # Create Playlist

#     """
#     data = {
#         'name': 'Test Test',
#         'description': 'Test'
#     }
#     #data = json.dumps(data)

#     cplaylist_api_endpoint = "{}/users/{}/playlists".format(SPOTIFY_API_URL, user_id)
#     cplaylist_response = requests.post(cplaylist_api_endpoint, headers=authorization_header, json = data)
#     created_data = json.loads(cplaylist_response.text)
#     """

#     created_data = playlists.create_playlist(authorization_header, user_id, playlists.make_playlist_data(playlist_name))

#     global playlist_id
#     playlist_id = created_data["id"]

#     # Combine profile and playlist data to display
#     display_arr = [profile_data] + [created_data]
#     # return render_template("index.html", sorted_array=display_arr)
#     return jsonify(display_arr)

@app.route("/api/addsong")
def addsong():
    # Get song id from url
    song_id = request.args.get('id')

    global songs_added
    songs_added.append(song_id)

    global seed_tracks
    seed_tracks.append(song_id)

    api_data = playlists.add_song(authorization_header, playlist_id, song_id)

    display_arr = [api_data] + songs_added
    return jsonify(display_arr)

@app.route("/api/recommendations")
def recommendations():
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']

    headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    artists = "%2C".join(seed_artists)
    genres = "%2C".join(seed_genres)

    tracks = None

    if len(seed_tracks) > 5:
        tracks = seed_tracks[-5:]
    else:
        tracks = seed_tracks

    tracks = "%2C".join(tracks)
    BASE_URL = "https://api.spotify.com/v1/recommendations?limit=10&market=ES&seed_artists={artists}&seed_genres={genres}&seed_tracks={tracks}".format(artists=artists, genres=genres,tracks=tracks)

    data = requests.get(BASE_URL, headers=headers)
    data = data.json()
    # r = r["tracks"][0]
    # return render_template("index.html", sorted_array=r)
    return data


# Get track info
@app.route("/api/trackinfo")
def trackinfo():
    # Get song id from url
    song_id = request.args.get('id')

    # Get track data
    track_api_endpoint = "{}/tracks/{}".format(SPOTIFY_API_URL, song_id)
    track_response = requests.get(track_api_endpoint, headers=authorization_header)
    track_data = json.loads(track_response.text)

    return jsonify(track_data["album"]["images"][0]["url"])


if __name__ == "__main__":
    app.run(debug=True, port=PORT)

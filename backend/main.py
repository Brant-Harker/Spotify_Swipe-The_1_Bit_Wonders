# pip install Flask python-dotenv requests

import json
from flask import Flask, request, redirect, g, render_template, jsonify
import requests
from urllib.parse import quote
import os
from dotenv import load_dotenv

import playlists

load_dotenv()

app = Flask(__name__)

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

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}


@app.route("/")
def index():
    # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    print(auth_url)
    return redirect(auth_url)


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
    return jsonify(profile_data)


@app.route("/api/createplaylist")
def createplaylist():
    # Get user ID
    user_id = profile_data["id"]

    # Get user playlist data
    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    playlist_data = json.loads(playlists_response.text)

    # Create Playlist

    """
    data = {
        'name': 'Test Test',
        'description': 'Test'
    }
    #data = json.dumps(data)

    cplaylist_api_endpoint = "{}/users/{}/playlists".format(SPOTIFY_API_URL, user_id)
    cplaylist_response = requests.post(cplaylist_api_endpoint, headers=authorization_header, json = data)
    created_data = json.loads(cplaylist_response.text)
    """

    created_data = playlists.create_playlist(authorization_header, user_id, playlists.make_playlist_data("Module"))

    # Combine profile and playlist data to display
    display_arr = [profile_data] + [created_data]
    # return render_template("index.html", sorted_array=display_arr)
    return jsonify(display_arr)


if __name__ == "__main__":
    app.run(debug=True, port=PORT)

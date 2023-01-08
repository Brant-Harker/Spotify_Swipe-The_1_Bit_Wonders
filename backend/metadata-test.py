import requests

CLIENT_ID = "980aa9bf0ae54f888ba9fb79bf1ba8b9"
CLIENT_SECRET = "57fcc1ddddff4f71b3d3a57494541ec0"

AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
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

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

# # Dummy data
# track_id = '6y0igZArWVi6Iz0rj35c1Y'
# album_id = '1A2GTWGtFfWp7KSQTwWOyo'

# # actual GET request with proper header
# # r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)
# r = requests.get(BASE_URL + 'albums/' + album_id, headers=headers)

# # convert response to JSON
# # rjson = r.json()
# cover_art_url = r.json()['images'][0]['url']

# # print(rjson)

# print(cover_art_url)

r = requests.get(BASE_URL + 'recommendations?limit=10&market=ES&seed_artists=4NHQUGzhtTLFvgF5SZesLK&seed_genres=classical%2Ccountry&seed_tracks=0c6xIDDpzE81m2q797ordA', headers=headers)

# convert response to JSON
rjson = r.json()

print(rjson["tracks"][0])
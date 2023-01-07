# RESTFUL API
# Tinder-like application for creating spotify playlists based on a user's music taste

import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Endpoint example
@app.route('/api', methods=['GET'])
def api():
    return jsonify({'message': 'Hello, World!'})


# Endpoints required
# Spotify authentication
# Create a playlist
# Add songs to a playlist
# Song recommendations
# Get song/album metadata (including preview)


if __name__ == '__main__':
    app.run(debug=True)
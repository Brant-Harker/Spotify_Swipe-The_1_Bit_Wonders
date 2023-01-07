"""
This module authorizes access to the Spotify API using Authorization Flow + PKCE
"""
from hashlib import sha256

# Parameters
client_id     = "980aa9bf0ae54f888ba9fb79bf1ba8b9"
response_type = "code"
redirect_uri  = "https://localhost"
state         = "secure string"
scope         = "image-upload user-library-modify playlist-modify-private playlist-modify-public streaming"

# PKCE Parameters
code_challenge_method = "S256"

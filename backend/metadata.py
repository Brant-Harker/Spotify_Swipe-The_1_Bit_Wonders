""" 
    This module requests metadata from the Spotify API and returns it to the frontend in JSON format.
"""

from dotenv import load_dotenv


# Spotify Authentication
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

load_dotenv()

# Song metadata class
class Song:
    def __init__(self, name, artist, album, preview_url, image_url):
        self.name = name
        self.artist = artist
        self.album = album
        self.preview_url = preview_url
        self.image_url = image_url

    def __str__(self):
        return f"{self.name} by {self.artist} on {self.album}"

    def __repr__(self):
        return f"{self.name} by {self.artist} on {self.album}"

    def to_json(self):
        return {
            "name": self.name,
            "artist": self.artist,
            "album": self.album,
            "preview_url": self.preview_url,
            "image_url": self.image_url
        }


if __name__ == "__main__":
    song = Song("Song Name", "Artist Name", "Album Name", "Preview URL", "Image URL")
    print(song)
    print(song.to_json())

# Artist
# Artist logo
# Album cover
# Spotify logo
import base64
from datetime import datetime


class Spotify:
    client_id = "88405b10e1704946976efdef33e73f64"
    client_secret = "9f5d2959d24e461a9b64b7a38291c0cf"
    scopes = ["playlist-modify-public", "playlist-modify-private",
              "ugc-image-upload", "user-read-recently-played", "user-read-private", "user-read-email",]
    auth_url = "https://accounts.spotify.com/authorize"
    token_url = "https://accounts.spotify.com/api/token"
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode()).decode()
    response_type = "code"
    scopes = ["playlist-modify-public", "playlist-modify-private",
              "ugc-image-upload", "user-read-recently-played", "user-read-private", "user-read-email",]

    get_user_endpoint = "https://api.spotify.com/v1/me"
    create_playlist_endpoint = "https://api.spotify.com/v1/me/playlists"
    get_recently_played_endpoint = "https://api.spotify.com/v1/me/player/recently-played"

    def to_unix(played_at):
        """converts played_at field given by Spotify API to unix timestamp in ms

        Args:
            played_at (str): played_at field given by Spotify API

        Returns:
            int: unix timestamp in ms
        """

        try:
            time = int(datetime.strptime(
                played_at, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp())
        except:
            time = int(datetime.strptime(
                played_at, "%Y-%m-%dT%H:%M:%SZ").timestamp())

        return time


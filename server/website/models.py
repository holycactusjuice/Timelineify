from mongoengine import Document, EmbeddedDocument, StringField, IntField, ListField, DictField
from flask_login import UserMixin
from flask import jsonify
import requests
import time

from . import users
from .spotify import Spotify


class Track(EmbeddedDocument):
    track_id = StringField(primary_key=True, required=True,
                           unique=True)  # same as spotify id
    title = StringField(required=True)
    artists = ListField(StringField(), required=True)
    album = StringField(required=True)
    album_art_url = StringField(required=True)
    length = IntField(required=True)
    played_at = IntField(required=True)
    plays = IntField(required=True, default=1)
    time_listened = IntField(required=True, default=0)

    def __init__(self, track_id, title, artists, album, album_art_url, length, played_at, plays=1, time_listened=0):
        self.track_id = track_id
        self.title = title
        self.artists = artists
        self.album = album
        self.album_art_url = album_art_url
        self.length = length
        self.played_at = played_at
        self.plays = plays
        self.time_listened = time_listened

    @classmethod
    def from_json(cls, track_json):
        """
        Creates a Track object from a track JSON

        Args:
            track_json (dict): track json received from Spotify API
        Returns:
            track (Track): Track object with track data
        """

        # retrieve track data from track JSON returned by Spotify API

        track_id = track_json['track']['id']
        title = track_json['track']['name']
        artists = [artist["name"]
                   for artist in track_json["track"]["artists"]]
        album = track_json["track"]["album"]["name"]
        album_art_url = track_json["track"]["album"]["images"][0]["url"]
        length = int(track_json['track']['duration_ms'] / 1000)
        played_at = track_json["played_at"]

        # instantiate Track object from these data
        track = Track(track_id, title, artists, album,
                      album_art_url, length, played_at)

        return track

    def to_dict(self):
        """
        Converts Track object to track JSON

        Returns:
            track_json (dict): track json to be sent to frontend
        """

        track_dict = {
            "track_id": self.track_id,
            "title": self.title,
            "artists": self.artists,
            "album": self.album,
            "album_art_url": self.album_art_url,
            "length": self.length,
            "played_at": self.played_at,
            "plays": self.plays,
            "time_listened": self.time_listened
        }

        return track_dict

    def to_json(self):
        return jsonify(self.to_dict())


class User(UserMixin, Document):
    user_id = StringField(required=True, primary_key=True, unique=True)
    email = StringField(required=True, unique=True)
    display_name = StringField(required=True)
    pfp_url = StringField(required=True)
    access_token = StringField(required=True)
    refresh_token = StringField(required=True)
    last_played_at = IntField(required=True, default=0)
    timeline_data = DictField(required=True)

    def __init__(self, user_id, email, display_name, pfp_url, access_token, refresh_token, last_played_at=0, timeline_data={}, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.user_id = user_id
        self.email = email
        self.display_name = display_name
        self.pfp_url = pfp_url
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.last_played_at = last_played_at
        self.timeline_data = timeline_data

    def from_document(user_doc):
        """
        Creates a User object from a user document
        """
        user = User(
            user_id=user_doc["user_id"],
            email=user_doc["email"],
            display_name=user_doc["display_name"],
            pfp_url=user_doc["pfp_url"],
            access_token=user_doc["access_token"],
            refresh_token=user_doc["refresh_token"],
            last_played_at=user_doc["last_played_at"],
            timeline_data=user_doc["timeline_data"]
        )
        return user

    def to_dict(self):
        """
        Converts User object to dictionary
        """
        return {
            "user_id": self.user_id,
            "email": self.email,
            "display_name": self.display_name,
            "pfp_url": self.pfp_url,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "last_played_at": self.last_played_at,
            "timeline_data": self.timeline_data
        }

    def to_json(self):
        return jsonify(self.to_dict())

    @staticmethod
    def id_to_json(user_id):
        user_doc = User.get_user_document(user_id)
        return jsonify(user_doc)

    @staticmethod
    def get_user_document(user_id):
        user_doc = users.find_one({"user_id": user_id})
        return user_doc

    @staticmethod
    def get(user_id):
        user_doc = User.get_user_document(user_id)
        return User.from_document(user_doc) if user_doc else None

    @staticmethod
    def get_account_info(access_token):
        response = requests.get(
            url=Spotify.get_user_endpoint(),
            headers={
                "Authorization": f"Bearer {access_token}",
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        return response.json()

    def update(self):
        """
        Updates the user document in the database
        """
        query = {"user_id": self.user_id}
        new_values = {"$set": self.to_dict()}
        users.update_one(query, new_values)

    def swap_and_update_tokens(self):
        headers = {
            'Authorization': f'Basic {Spotify.client_creds_b64}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }
        response = requests.post(Spotify.token_url, headers=headers, data=data)
        response_data = response.json()
        new_access_token = response_data['access_token']
        self.access_token = new_access_token

        # new refresh token is only given if last one expired
        if 'refresh_token' in response_data:
            new_refresh_token = response_data['refresh_token']
            self.refresh_token = new_refresh_token

        self.update()
        return

    def get_recent_tracks(self):
        response = requests.get(
            url=Spotify.get_recently_played_endpoint(),
            params={
                # current EST time in milliseconds
                "before": ((time.time() + 5 * 60 * 60) * 1000),
                "limit": 50
            },
            headers={
                "Authorization": f"Bearer {self.access_token}"
            }
        )

        # return empty list if access token has expired
        if (response.status_code in range(400, 499)):
            return []

        recent_tracks = response.json()["items"]

        recent_tracks.reverse()

        # Track objects stored here
        tracks = []

        for i, track_json in enumerate(recent_tracks):
            # list is least to most recent

            # listen time is given as the time when the user stopped listening to the track
            # we can't calculate listen time for the first track since there is no track before it
            # so we ignore the last track
            if (i == 0):
                continue

            track = Track.from_json(track_json)
            time_listened = Spotify.to_unix(
                recent_tracks[i-1]["played_at"]) - Spotify.to_unix(track_json["played_at"])
            # time_listened > length if:
            #   - the user took a break before playing the track
            #   - the user paused the track
            #   - this is the first song in the session
            # so if time_listened > track_length, make time_listened = track_length
            track.time_listened = min(time_listened, track.length)
            track.played_at = track_json["played_at"]
            tracks.append(track)

        return tracks

    def update_timeline_data(self):
        """
        Updates the timeline data for the user
        """

        tracks = self.get_recent_tracks(
            access_token=self.access_token)

        # user_doc = users.find_one({"user_id": self.user_id})
        # timeline_data = user_doc["timeline_data"]

        for new_track in tracks:
            month = Spotify.unix_to_month(new_track.played_at)

            # if month does not yet exist in the user's timeline data, create it
            if (month not in self.timeline_data):
                self.timeline_data[month] = []

            exists = False
            for existing_track in self.timeline_data[month]:
                # check if track already exists in the user's timeline data
                if (existing_track.track_id == new_track.track_id):
                    # if the new track is more recent than the existing track, update the existing track
                    if (new_track.played_at > existing_track.played_at):
                        existing_track.played_at = new_track.played_at
                        exists = True
                        existing_track.plays += 1
                        existing_track.time_listened += new_track.time_listened
                    # otherwise, do nothing since this listen has already been recorded
                    else:
                        exists = True
            # if track does not yet exist in the user's timeline data, add it
            if (not exists):
                self.timeline_data[month].append(new_track.to_json())

        self.update()
        return

    def create_playlist(self, playlist_name, description):
        # proactively update access and refresh tokens
        self.swap_and_update_tokens()
        response = requests.post(
            url=Spotify.create_playlist_endpoint(self.user_id),
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            },
            # must send as json, not data
            json={
                "name": playlist_name,
                "description": description,
                "public": False
            }
        )

        playlist_id = response.json()["id"]
        return playlist_id

    def get_top_tracks(self, month, length=-1):
        """
        Returns the top tracks for a given month

        Args:
            month (str): month for which to get top tracks
            length (int): number of tracks to return
        Returns:
            top_tracks (list): list of top tracks for the given month
        """
        tracks = self.timeline_data[month]
        # sort tracks
        # - primary key is play count
        # - secondary key is time listened
        # - descending (greatest first)
        # then slice to get desired number of tracks
        top_tracks = sorted(tracks, key=lambda track: (
            track["plays"], track["time_listened"]), reverse=True)

        if length == -1:
            return top_tracks
        else:
            return top_tracks[:length]

    def add_tracks_to_playlist(self, playlist_id, top_tracks_uris):
        """
        Adds tracks to a playlist

        Args:
            playlist_id (str): id of playlist to add tracks to
            top_tracks_uris (list): list of track uris to add to playlist
        """
        # proactively update access and refresh tokens
        self.swap_and_update_tokens()
        response = requests.post(
            url=Spotify.add_to_playlist_endpoint(playlist_id),
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            },
            # must send as json, not data
            json={
                "uris": top_tracks_uris
            }
        )
        return

    def create_top_tracks_playlist(self, month, length, playlist_name, description):
        """
        Creates a playlist of the user's top tracks for a given month

        Args:
            month (str): month for which to create playlist
            length (int): number of tracks to include in playlist
            playlist_name (str): name of playlist
            description (str): description of playlist
        Returns:
            playlist_id (str): id of created playlist
        """
        # create playlist first and get the playlist id
        playlist_id = self.create_playlist(playlist_name, description)
        # create list of ids of top tracks
        top_tracks_ids = [track["track_id"]
                          for track in self.get_top_tracks(month, length)]
        # turn track ids into track uris
        top_tracks_uris = [
            f"spotify:track:{track_id}" for track_id in top_tracks_ids]
        # add tracks to playlist
        self.add_tracks_to_playlist(playlist_id, top_tracks_uris)

        return playlist_id

    def get_monthview_data(self, month):
        """

        """
        tracks = self.timeline_data[month]
        # calculate total number different of tracks
        tracks_count = len(tracks)
        # calculate total number of plays across all tracks
        total_plays = sum([track["plays"] for track in tracks])
        # calculate time listened across all tracks
        total_time_listened = sum(
            [track["time_listened"] for track in tracks])
        hours_listened = total_time_listened // 3600
        minutes_listened = (total_time_listened % 3600) // 60
        seconds_listened = total_time_listened % 60

        return {
            "tracks_count": tracks_count,
            "total_plays": total_plays,
            "time_listened": {
                "hours": hours_listened,
                "minutes": minutes_listened,
                "seconds": seconds_listened
            },
        }

    @staticmethod
    def month_str_to_full(month):
        """
        Converts month string of form MM-YYYY to Month Year

        Args:
            month (str): month string of form MM-YYYY
        Returns:
            month_full (str): month string of form Month Year
        """
        month_dict = {
            "01": "January",
            "02": "February",
            "03": "March",
            "04": "April",
            "05": "May",
            "06": "June",
            "07": "July",
            "08": "August",
            "09": "September",
            "10": "October",
            "11": "November",
            "12": "December"
        }
        month_parts = month.split("-")
        month_number = month_parts[0]
        year = month_parts[1]
        month_full = month_dict.get(month_number, "") + " " + year
        return month_full

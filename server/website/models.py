from mongoengine import Document, EmbeddedDocument, StringField, IntField, ListField, EmbeddedDocumentField, DictField
from flask_login import UserMixin
import requests
import json
import math
import time

from . import users
from spotify import Spotify


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

    def to_json(self):
        """
        Converts Track object to track JSON

        Returns:
            track_json (dict): track json to be sent to frontend
        """

        track_json = {
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

        return track_json


class User(UserMixin, Document):
    user_id = StringField(required=True, primary_key=True, unique=True)
    email = StringField(required=True, unique=True)
    display_name = StringField(required=True)
    pfp_url = StringField(required=True)
    access_token = StringField(required=True)
    refresh_token = StringField(required=True)
    last_played_at = IntField(required=True, default=0)
    timeline_data = DictField(required=True)

    def __init__(self, user_id, email, display_name, pfp_url, access_token, refresh_token, last_played_at, timeline_data={}, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.user_id = user_id
        self.email = email
        self.display_name = display_name
        self.pfp_url = pfp_url
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.last_played_at = last_played_at
        self.timeline_data = timeline_data

    @staticmethod
    def get_user_document(user_id):
        user_doc = users.find_one({"user_id": user_id})
        return user_doc

    @staticmethod
    def get_access_token(user_id):
        user_doc = users.find_one({"user_id": user_id})
        access_token = user_doc["access_token"]
        return access_token

    @staticmethod
    def get_refresh_token(user_id):
        user_doc = users.find_one({"user_id": user_id})
        refresh_token = user_doc["refresh_token"]
        return refresh_token

    @staticmethod
    def get_timeline_data(user_id):
        user_doc = users.find_one({"user_id": user_id})
        get_timeline_data = user_doc["get_timeline_data"]
        return get_timeline_data

    @staticmethod
    def get_account_info(access_token):
        response = requests.get(
            url=Spotify.get_user_endpoint,
            headers={
                "Authorization": "Bearer " + access_token,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        return response.json()

    @staticmethod
    def update_last_played_at(user_id, last_played_at):
        user_doc = users.find_one({"user_id": user_id})
        new_values = {"$set": {"last_played_at": last_played_at}}
        users.update_one(user_doc, new_values)
        return

    @staticmethod
    def get_recent_tracks(access_token):
        response = requests.get(
            url=Spotify.get_recently_played_endpoint,
            params={
                # current EST time in milliseconds
                "before": ((time.time() + 5 * 60 * 60) * 1000),
                "limit": 50
            },
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )

        # return empty list if access token has expired
        if (response.status_code in (401, 403)):
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

    @staticmethod
    def update_timeline_data(user_id, access_token):
        """
        Updates the timeline data for the user
        """

        tracks = User.get_recent_tracks(
            access_token=access_token)

        user_doc = users.find_one({"user_id": user_id})
        timeline_data = user_doc["timeline_data"]

        for new_track in tracks:
            month = Spotify.unix_to_month(new_track.played_at)

            # if month does not yet exist in the user's timeline data, create it
            if (month not in timeline_data):
                timeline_data[month] = []

            exists = False
            for existing_track in timeline_data[month]:
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
                timeline_data[month].append(new_track.to_json())

        new_values = {"$set": {"timeline_data": timeline_data}}
        users.update_one(user_doc, new_values)

        return

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json


with open("data.json", "r", encoding="utf-8") as f:
    spotify_data = json.load(f)


scope = 'playlist-modify-public playlist-modify-private user-read-currently-playing user-read-playback-state user-modify-playback-state'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=spotify_data["spotify"]["client_id"],
        client_secret=spotify_data["spotify"]["client_secret"],
        redirect_uri=spotify_data["spotify"]["redirect_uri"],
    )
)


def add_queue(url):
    try:
        sp.add_to_queue(uri=url, device_id=sp.devices()["devices"][0]["id"])
        return "Added track to queue"
    except Exception as e:
        return f"Request raised an Error: {e}"


def add_track(playlist_id, track_id: str):
    track = []
    if track_id.startswith("https://open.spotify.com/track/"):
        _track = track_id[31:][:22]
        track.append(_track)
    elif track_id.startswith("spotify:track:"):
        _track = track_id[13:]
        track.append(_track)
    else:
        result = sp.search(track_id, limit=1, offset=0, type='track')
        _track = result['tracks']['items'][0]['external_urls']['spotify'][31:][:22]
        track.append(_track)
    try:
        sp.playlist_add_items(playlist_id=playlist_id, items=track, position=len(sp.playlist_tracks(playlist_id)['items']))
        return "Added track to playlist"
    except Exception as e:
        return f"Request raised an Error: {e}"


def search(query: str):
    if query.startswith("https://open.spotify.com/track/"):
        return query
    else:
        results = sp.search(query, limit=1, offset=0, type='track')
        items = results['tracks']['items'][0]["external_urls"]["spotify"]
        return items


def now_playing():
    info = []
    artist = sp.current_user_playing_track()['item']['name']
    song = sp.current_user_playing_track()['item']['artists'][0]['name']
    info.append(artist)
    info.append(" - ")
    info.append(song)
    return info


def prev_track():
    try:
        sp.previous_track()
        return "Previous track"
    except Exception as e:
        return f"Request raised an Error: {e}"


def skip_track():
    try:
        sp.next_track()
        return "Skipped track"
    except Exception as e:
        return f"Request raised an Error: {e}"


def _volume(volume: int):
    for devices in sp.devices()["devices"]:
        if devices["is_active"]:
            vol = sp.volume(volume, device_id=devices["id"])
            return vol


def pause_track():
    try:
        sp.pause_playback()
        return "Paused track"
    except Exception as e:
        return f"Request raised an Error: {e}"


def resume_track(playlist_id):
    try:
        sp.start_playback(context_uri=playlist_id)
        return "Resumed track"
    except Exception as e:
        return f"Request raised an Error: {e}"

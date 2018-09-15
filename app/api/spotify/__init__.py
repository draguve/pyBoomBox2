import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

from app.api.spotify.models import *

username = 'username'
client_id='clientid'
client_secret='clientsecret'
redirect_uri='redirecturl'

def get_random_playlists(limit=1,offset=-1):
    if(offset==-1):
        offset = random.randint(0,1500)
    return get_playlist('spotify',limit=limit,offset=offset)

def get_token():
    scope = 'playlist-modify-private'
    token = util.prompt_for_user_token(username,scope,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
    return token

def get_playlists(user,limit,offset):
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    playlists_json = sp.user_playlists(user,limit=limit,offset=offset)
    playlists = []
    for playlist_json in playlists_json['items']:
        playlists.append(Playlist(playlist_json))
    return playlists

def get_playlist_content(user,playlistid=None,fields=None):
    sp = spotipy.Spotify(auth=get_token())
    all_tracks_json = []
    results = sp.user_playlist(username, playlistid,fields="tracks,next")
    tracks = results['tracks']
    all_tracks_json.append(results['tracks'])
    while tracks['next']:
        all_tracks_json.append(sp.next(tracks))
    all_tracks_j = all_tracks_json[0]['items']
    all_tracks = []
    for track in all_tracks_j:
        all_tracks.append(Track(track,is_playlist_track=True))
    return all_tracks

def get_track(track_id):
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    track_json = sp.track(track_id)
    return Track(json)

def get_tracks(track_ids):
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    tracks_json = sp.tracks(track_ids)
    tracks = []
    for track_json in tracks_json['tracks']:
        tracks.append(Track(track_json))
    return tracks


from app.api.spotify import *

class Track:
    def __init__(self,json,is_playlist_track=False):
        if(is_playlist_track):
            json = json['track']
        self.id = json['id']
        self.title = json['name']
        self.album = json['album']['name']

        #song might have multiple artist
        self.artist = []
        self.artistids = []
        for artist in json['artists']:
            self.artist.append(artist['name'])
            self.artistids.append(artist['id'])
        
        # images 1 contains 300px X 300px images
        self.albumart = json['album']['images'][1]['height']
        self.explict = json['explicit']
        self.duration = json['duration_ms']
        self.url = json['external_urls']['spotify']
        self.popularity = json['popularity']

class Artist:
    def __init__(self,json,simplified):
        self.simplified = simplified
        self.id = json['id']
        self.name = json['name']
        if(not(simplified)):
            desimplify(self,json)

    def desimplify(self):
        if(self.simplified):
            #get the complete artist
            desimplify(self,json)

    def desimplify(self,json):
        self.genres = json['genres']
        self.popularity = json['popularity']

        self.images = []
        for image in json['images']:
            self.images.append(image['url'])

class Playlist:
    def __init__(self,json):
        self.id = json['id']
        self.name = json['name']
        self.no_of_tracks = json['tracks']['total']
        self.username = json['owner']['display_name']
        self.tracks = None
    
    def get_tracks(self):
        self.tracks = get_playlist_content(user=self.username,playlistid=self.id)
        return self.tracks


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
        self.albumart = json['external_urls']['images'][1]['height']
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



from enum import Enum

class RequestTypes(Enum):
    add_client = 1
    add_vote = 2
    suggest_song = 3
    get_all_songs = 4
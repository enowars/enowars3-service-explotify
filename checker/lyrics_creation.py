
from music_service import MService


m_service = MService()

def create_song_locally(lyrics,address,round,team):
        list_words = list(lyrics)
        path_create = f"{address}_{round}_{team}.mp3"
        lyrics_to_generate = " ".join(list_words)
        m_service.generate_song(lyrics_to_generate,export_path=path_create)
        song_file = open(path_create,"rb")
        return song_file.read()
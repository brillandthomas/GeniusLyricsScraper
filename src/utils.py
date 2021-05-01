import os
import re

def clean_lyrics(lyrics: str) -> str:
    """
        Removes the [] and the newlines from the lyrics. Can be useful to train NLP models.  

        Input  
        lyrics (str): the lyrics as string  

        Returns
        lyrics (str): the cleaned lyrics
    """
    lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
    lyrics = os.linesep.join([line for line in lyrics.splitlines() if line])

    return lyrics

def get_file_name(url: str) -> str:
    """
        Removes the https://genius.com from the url in order to get the filename.

        Input
        url (str): https://genius.com/artist-song-lyrics  

        Returns  
        file_name (str): artist-song-lyrics.txt
    """

    base_url = 'https://genius.com'

    file_name = url[len(base_url)+1:]+'.txt'

    return file_name

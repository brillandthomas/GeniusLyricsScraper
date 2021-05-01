GENIUS_API_TOKEN = 'Your API Token'

#To save the .txt files
import os

#Loading bar
from tqdm import tqdm

#Scraping part
import requests
from bs4 import BeautifulSoup
import json

from utils import clean_lyrics, get_file_name

def request_artist_research(artist_name:str, page_number:int) -> json:
    """
        Research the artist name in the API
        
        Inputs  
        artist_name (str): The name of the artist  
        page_number (int): The page of the request results  

        Returns    
        response (json): The response of the request, as a json  
    """
    api_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + GENIUS_API_TOKEN}
    search_url = api_url + '/search?per_page=10&page=' + str(page_number)
    data = {'q': artist_name}
    response = requests.get(search_url, data=data, headers=headers)
    response = response.json()
    
    return response

def request_songs_url(artist_name: str, song_cap: int) -> list:
    """
        Get the Genius links of the lyrics for song_cap songs of artist_name.

        Inputs  
        artist_name (str): The name of the artist  
        song_cap (int): The number of songs you want to get   

        Returns  
        songs_list (list): The list of the song links  
    """
    page_number = 1
    songs_list = []

    while True:
        
        response_json = request_artist_research(artist_name, page_number)

        songs_per_page = []

        for song in response_json['response']['hits']:
            if song['result']['primary_artist']['name'].lower() == artist_name.lower():
                songs_per_page.append('https://genius.com'+song['result']['path'])
        
        for url in songs_per_page:
            if len(songs_list) < song_cap:
                songs_list.append(url)
        
        if len(songs_list) == song_cap:
            break
        else:
            page_number+= 1
    
    return songs_list

def scrape_song_lyrics(url: str) -> str:
    """
        Get the song lyrics as a string.  

        Input  
        url (str): The genius link for the song lyrics.  

        Returns
        lyrics (str): The song lyrics as a string.  
    """

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    lyrics = soup.find(class_='lyrics')

    try:
        lyrics = lyrics.get_text()
    except AttributeError: #Sometimes Genius changes the tags: need to retry
        return scrape_song_lyrics(url)
    
    return lyrics

def scrape_songs_artist(artist_name: str, song_cap: int, clean: bool=False) -> None:
    """
        Scrape song_cap songs from artist_name.  

        Input  
        artist_name (str): The name of the artist  
        song_cap (int): The number of songs  
        clean (bool): Apply the clean_lyrics function if True.

        Returns  
        None
    """

    if not os.path.exists('lyrics'):
        os.makedirs('lyrics')
    if not os.path.exists(os.path.join('lyrics',artist_name)):
        os.makedirs(os.path.join('lyrics', artist_name))

    path_folder = os.path.join('lyrics', artist_name)
    songs_url = request_songs_url(artist_name, song_cap)

    number_of_lines = 0

    for song in tqdm(songs_url):

        file_name = get_file_name(song)
        file_name = os.path.join(path_folder, file_name)

        lyrics = scrape_song_lyrics(song)

        if clean:
            lyrics = clean_lyrics(lyrics)

        number_of_lines += len(lyrics.splitlines())

        file_song = open(file_name, 'wb')
        file_song.write(lyrics.encode('utf-8'))
        file_song.close()
    
    print('Saved {} lines of song lyrics from {} songs in lyrics/{}.'.format(number_of_lines, artist_name, artist_name))

    return 

if __name__ == '__main__':

    artist = 'Eminem'
    number_of_songs = 10

    scrape_songs_artist(artist,number_of_songs, clean=False)
# Song Lyrics Scraper
Scrape song lyrics from https://genius.com.

This project allows the user to scrape a certain number of songs from a specific artist.  

First you need to create an API on https://genius.com/api-clients.  
You have to replace the GENIUS_API_TOKEN variable at the beginning of lyrics-scraper.py by your own token.  

You can now run the lyrics_scraper.py file after entering the artist name and the number of songs you want to scrape.  
This will save the files as .txt files in the lyrics/artist_name folder.  
You can then merge all the songs from an artist with file-merger.py.  

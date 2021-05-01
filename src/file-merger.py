import os
from tqdm import tqdm

from utils import clean_lyrics

def merge_txt_files(folder_input: str, output_path: str, clean: bool=False) -> None:
    """
        Merge all the songs from a folder.  

        Inputs  
        folder_input (str): The directory that needs to be merged  
        output_path (str): The entire path of the output file (.txt)
        clean (bool): Apply clean_lyrics if True  

        Returns
        None
    """

    list_file_names = [file_name for file_name in os.listdir(folder_input) if '.txt' in file_name]
    merged_file = open(output_path, 'wb')
    line_count = 0

    for file_name in tqdm(list_file_names):

        song = open(os.path.join(folder_input,file_name), 'r', encoding='utf-8')
        lyrics = song.read()
        song.close()

        if clean:
            lyrics = clean_lyrics(lyrics)
        line_count += len(lyrics.splitlines())

        merged_file.write(lyrics.encode('utf-8'))

    merged_file.close()

    print('{} lines of song lyrics from {} songs, saved to {}.'.format(line_count, len(list_file_names), output_path))

    return


if  __name__ == '__main__':

    input_path = 'lyrics/Eminem'
    output_name = 'lyrics/merged.txt'

    merge_txt_files(input_path, output_name, clean=True)

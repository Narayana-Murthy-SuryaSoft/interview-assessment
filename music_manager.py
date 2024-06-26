import os
import argparse
import ntpath
import shutil
import requests
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

MUSICBRAINZ_API_URL = "http://musicbrainz.org/ws/2/recording"

def list_files(directory):
    music_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.mp3'):
                music_files.append(os.path.join(root, file))
    return music_files

def get_metadata(file_path):
    try:
        if file_path.lower().endswith('.mp3'):
            audio = EasyID3(file_path)  # Default to MP3 if not recognized
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    song = audio.get('title', ['Unknown'])[0]
    artist = audio.get('artist', ['Unknown'])[0]
    album = audio.get('album', ['Unknown'])[0]

    return song, artist, album

def show_metadata(file_path, song, artist, album):
    print("____________________")
    print(f"File: {ntpath.basename(file_path)}")
    print(f"Song: {song}")
    print(f"Artist: {artist}")
    print(f"Album: {album}")

def copy_or_show(copy, source_file, dest_dir):
    if copy:
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy2(source_file, os.path.join(dest_dir, os.path.basename(source_file)))
    else:
        print(source_file, '--->', os.path.join(dest_dir, os.path.basename(source_file)))
    

def group_by_artist(files, output_dir, copy=False):
    for file in files:
        song, artist, album = get_metadata(file)
        artist_dir = os.path.join(output_dir, artist)
        copy_or_show(copy, file, artist_dir)

def group_by_album(files, output_dir, copy=False):
    for file in files:
        song, artist, album = get_metadata(file)
        album_dir = os.path.join(output_dir, album)
        copy_or_show(copy, file, album_dir)

def group_by_artist_album(files, output_dir, copy=False):
    for file in files:
        song, artist, album = get_metadata(file)
        artist_album_dir = os.path.join(output_dir, artist, album)
        copy_or_show(copy, file, artist_album_dir)

def suggest_metadata_matches(file):
    song, artist, album = get_metadata(file)
    print(f"File: {file}")
    print("Top 3 matches:")

    params = {
        "query": song,
        "limit": 3,
        "fmt": "json",
    }
    try:
        response = requests.get(MUSICBRAINZ_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            for idx, rec in enumerate(data['recordings']):
                title = rec.get('title', 'Unknown')
                artist = rec.get('artist-credit', [{'artist': {'name': 'Unknown'}}])[0]['artist']['name']
                album = rec.get('release', {}).get('title', 'Unknown')
                print(f"{idx + 1}. Song: {title}")
                print(f"   Album: {album}")
                print(f"   Artist: {artist}")
            return data
        else:
            print(f"Failed to fetch metadata suggestions for {file}")
    except Exception as e:
        print(f"Error fetching metadata suggestions for {file}: {e}")
    print("---")

def update_metadata(file, data, choice):
    TODO


def main():
    parser = argparse.ArgumentParser(description='Music Library Manager')
    parser.add_argument('--input', type=str, required=True, help='Path to music folder')
    parser.add_argument('--list-files', action='store_true', help='List all music files')
    parser.add_argument('--show-metadata', action='store_true', help='Show metadata of music files')
    parser.add_argument('--group-by', type=str, choices=['ARTIST', 'ALBUM', 'ARTIST_ALBUM'], help='Group by ARTIST, ALBUM, or ARTIST_ALBUM')
    parser.add_argument('--reorganize-by', type=str, choices=['ARTIST', 'ALBUM', 'ARTIST_ALBUM'], help='Reorganize by ARTIST, ALBUM, or ARTIST_ALBUM (dry run)')
    parser.add_argument('--suggest-metadata-matches', action='store_true', help='Suggest metadata matches from online sources')
    parser.add_argument('--update-metadata', action='store_true', help='Update metadata suggestions from online sources')

    args = parser.parse_args()

    output = os.path.join(os.getcwd(), 'Music')

    if args.list_files:
        files = list_files(args.input)
        for file in files:
            print(ntpath.basename(file))
    elif args.show_metadata:
        files = list_files(args.input)
        for file in files:
            song, artist, album = get_metadata(file)
            show_metadata(file, song, artist, album)
    elif args.group_by:
        if not os.path.exists(output):
            os.makedirs(output)
        if args.group_by == 'ARTIST':
            group_by_artist(list_files(args.input), output, copy=True)
            print(f"Files grouped by Artist in directory: {output}")
        elif args.group_by == 'ALBUM':
            group_by_album(list_files(args.input), output, copy=True)
            print(f"Files grouped by Album in directory: {output}")
        elif args.group_by == 'ARTIST_ALBUM':
            group_by_artist_album(list_files(args.input), output, copy=True)
            print(f"Files grouped by Artist and Album in directory: {output}")
    elif args.reorganize_by:
        if args.reorganize_by == 'ARTIST':
            group_by_artist(list_files(args.input), output)
        elif args.reorganize_by == 'ALBUM':
            group_by_album(list_files(args.input), output)
        elif args.reorganize_by == 'ARTIST_ALBUM':
            group_by_artist_album(list_files(args.input), output)
    elif args.suggest_metadata_matches:
        files = list_files(args.input)
        for file in files:
            suggest_metadata_matches(file)
    elif args.update_metadata:
        files = list_files(args.input)
        for file in files:
            data = suggest_metadata_matches(file)
            choice = input('Do you wish to update (Y/N)')
            if (choice == 'Y'):
                choice = input('Select correct choice (1, 2, 3):')
                if choice not in (1,2,3):
                    return
                update_metadata(file, data, choice)
                print('Metadata updated')
            
    else:
        print("Please specify a valid command")

if __name__ == "__main__":
    main()

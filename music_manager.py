import os
import argparse
import ntpath
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

def list_files(directory):
    music_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.mp3'):
                music_files.append(os.path.join(root, file))
    return music_files

def show_metadata(file_path):
    try:
        if file_path.lower().endswith('.mp3'):
            audio = EasyID3(file_path)  # Default to MP3 if not recognized
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    song = audio.get('title', ['Unknown'])[0]
    artist = audio.get('artist', ['Unknown'])[0]
    album = audio.get('album', ['Unknown'])[0]

    print("____________________")
    print(f"File: {ntpath.basename(file_path)}")
    print(f"Song: {song}")
    print(f"Artist: {artist}")
    print(f"Album: {album}")

def main():
    parser = argparse.ArgumentParser(description='Music Library Manager')
    parser.add_argument('--input', type=str, required=True, help='Path to music folder')
    parser.add_argument('--list-files', action='store_true', help='List all music files')
    parser.add_argument('--show-metadata', action='store_true', help='Show metadata of music files')

    args = parser.parse_args()

    if args.list_files:
        files = list_files(args.input)
        for file in files:
            print(ntpath.basename(file))
    elif args.show_metadata:
        files = list_files(args.input)
        for file in files:
            show_metadata(file)
    else:
        print("Please specify a valid command")

if __name__ == "__main__":
    main()

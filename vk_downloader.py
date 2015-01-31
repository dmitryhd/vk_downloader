#!/usr/bin/env python3

from bs4 import BeautifulSoup
from urllib.request import urlopen
import os.path

OUT_DIR = 'music'


def get_music_urls(song_list_file):
    with open(song_list_file, encoding="windows-1251", errors="surrogateescape") as song_list_fd:
        song_list_soup = BeautifulSoup(song_list_fd.read())
        songs = {}  # result 
        for song_item in song_list_soup.findAll("input", {"type": "hidden"}):
            song_url = song_item['value']
            author = song_item.findNext('a').string
            track_name = song_item.findNext('a').findNext('a').string
            if not track_name:
                continue
            author.replace('/', '')
            track_name.replace('/', '')
            out_file_name = author + "-" + track_name + ".mp3"
            songs[out_file_name] = song_url
    return songs


def save_song(url, filename):
    try:
        print("Download: ", filename)
        song = urlopen(url)
        if os.path.isfile(filename):
            print("file:", filename, "already exists!")
            return
        with open(filename, 'wb') as out_fd:
            out_fd.write(song.read())
    except FileNotFoundError:
        print('File not found: ', filename)
    except ValueError:
        print('Wrong url:', url)


def download_music(songs):
    for song_name in songs:
        save_song(songs[song_name], OUT_DIR + '/' +  song_name)


if __name__ == '__main__':
    songs = get_music_urls('tmp/xx.html')
    download_music(songs)

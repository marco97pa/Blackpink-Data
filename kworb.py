#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

from utils import convert_num, display_num
from tweet import twitter_post

hashtags= "\n@BLACKPINK #blinks #music #kpop #streams"
module = "Kworb Charts"

def kworb_data(group):
    """Gets Spotify charts data of an artist

    It starts all the tasks needed to get latest data and eventually tweet updates

    Args:
      - group: dictionary that contains all the data about the group

    Returns:
      the same group dictionary with updated data
    """

    fetched = get_artist_charts(group)
    group = check_new_goal(group, fetched)
    return group

def get_artist_charts(artist):
    """Gets charts of an artist

    It scrapes the page https://kworb.net/spotify/artist/xxxxx.html by parsing the table
    containing all the tracks of that artist with the number of streams

    Args:
      - artist: dictionary that contains all the data about the single artist

    Returns:
      a list of dictionaries with track id, name and number of streams
    """

    URL = 'https://kworb.net/spotify/artist/' + artist["spotify"]["id"]+ '.html'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('table')

    results = []
    z = 0
    for row in table.findAll('tr'):
        elem = row.findAll('td')
        if len(elem) > 3:
            track = {
                "id": elem[1].a.get('href')[9:-5],
                "name": elem[1].text,
                "streams": int (elem[3].text.replace(",",""))
            }
            results.append(track)
            z+=1

    print("[{}] ({}) Fetched {} songs".format(module, artist["name"], z))

    return results

def check_new_goal(artist, new):
    """Checks if a track hits a new stream goal (fixed to 10 million)

    It tweets if a track reaches a new goal

    Args:
      - artist: dictionary that contains all the data about the single artist
      - new: a list of dictionaries with track id, name and number of streams

    Returns:
      an artist dictionary with updated data
    """

    if "kworb" in artist:
        old = artist["kworb"]
        for old_song in old:
            for new_song in new:
                if new_song["id"] == old_song["id"]:
                    if convert_num("10M", old_song["streams"]) != convert_num("10M", new_song["streams"]):
                        twitter_post(
                            "{} reached {} streams on #Spotify\n{}\n{}"
                            .format(new_song["name"], display_num(new_song["streams"]), link_song(new_song["id"]), hashtags)
                            )
    
    artist["kworb"] = new
    return artist

def link_song(track_id):
    """Generates a song link on Spotify, given the id
    
    Args:
      - track_id: id of the song

    Returns:
      a link to that song on Spotify
    """

    return "https://open.spotify.com/track/" + track_id

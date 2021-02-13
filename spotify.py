#!/usr/bin/env python3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from utils import display_num, convert_num, download_image
from tweet import twitter_post, twitter_post_image

hashtags= "\n#blackpink #music #song #spotify #newmusic #kpop #lisa #jisoo #jennie #rosé"


def login():
    print("Logging in...")
    # Client credential authorization flow
    # See https://spotipy.readthedocs.io/en/2.16.1/#authorization-code-flow
    auth_manager = SpotifyClientCredentials()
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    return spotify

def get_artist(spotify, artist):
    # Generate URI
    artist["uri"] = 'spotify:artist:' + artist["id"]

    artist_details = spotify.artist(artist["uri"])


    artist["name"] = artist_details["name"]
    print("Getting details of {} ({})".format(artist["name"], artist["id"]))

    artist["popularity"] = artist_details["popularity"]
    artist["genres"] = artist_details["genres"]
    try:
        artist["image"] = artist_details["images"][0]["url"]
    except:
        artist["image"] = None
        print("WARNING: Cannot fetch image of {}".format(artist["name"])) # This fix is needed for artists without a profile image

    if convert_num("100K", artist["followers"]) != convert_num("100K", artist_details["followers"]["total"]):
        artist["followers"] = artist_details["followers"]["total"]
        twitter_post_image(
            "{} reached {} followers on Spotify\n{}\n{}".format(artist["name"], display_num(artist["followers"], decimal=True), link_artist(artist["id"]), hashtags),
            download_image(artist["image"]),
            display_num(artist["followers"], short=True),
            text_size=125
            )

    return artist

def get_discography(spotify, artist):

    print("Fetching discography...")

    # ALBUM DETAILS
    albumResults = spotify.artist_albums(artist["uri"], limit=50)
    albumResults = albumResults['items']
    z = 0


    # Loop over album
    collection = []
    for album in albumResults:

        # TRACK DETAILS
        trackResults = spotify.album_tracks(album['id'])
        trackResults = trackResults['items']
        
        ## Loop over tracks
        tracks = []
        for track in trackResults:
            
            artists_names =[]
            artists_ids = []
            
            for artist_track in track['artists']:
                artists_names.append(artist_track['name'])
                artists_ids.append(artist_track['id'])
            
            ## Extract track data and fill database
            if artist["id"] in artists_ids:
                z+=1
                tracks.append({'name':track['name'],
                                'id': track['id']}
                                )

        if album['album_group'] != 'appears_on':
            collection.append({'name':album['name'],
                                'id': album['id'],
                                'release_date':album['release_date'],
                                'total_tracks':album['total_tracks'],
                                'type':album['album_group'],
                                'image':album['images'][0]['url'],
                                'tracks': tracks}
                                )
        else:
            collection.append({'name':album['name'],
                                'id': album['id'],
                                'release_date':album['release_date'],
                                'total_tracks':album['total_tracks'],
                                'type':album['album_group'],
                                'image':album['images'][0]['url'],
                                'artist_collab':album['artists'][0]['name'],
                                'tracks': tracks}
                                )
    
    print("Fetched {} songs".format(z))

    # Remove duplicates
    print("Removing duplicates")
    seen = set()
    result = []
    z = 0

    for album in collection:
        key = album['name']
        if key in seen:
            continue

        result.append(album)
        z += 1
        seen.add(key)

    print("Now we have {} albums and singles".format(z))

    # Uncomment for debug: it prints all the albums and singles fetched
    #
    # for album in result:
    #     print(album["name"].upper())
    #     for track in album["tracks"]:
    #         print(track["name"])
    #     print()

    return result

def check_new_songs(artist, collection):
    print("Checking new songs...")
    old = artist["discography"]

    for album in collection:
        if album not in old:
            if album["type"] != 'appears_on':
                twitter_post_image(
                    "{} released a new {} on Spotify: {}\n{}\n{}".format(artist["name"], album["type"], album["name"], link_album(album["id"]), hashtags),
                    download_image(album["image"]),
                    None
                    )
            else:
                twitter_post("{} appeared on {} by {} with the song {}\n{}\n{}".format(artist["name"], album["name"], album["artist_collab"], album["tracks"][0]["name"], link_album(album["id"]), hashtags ))
    
    artist["discography"] = collection
    return artist

def link_album(album_id):
    return "https://open.spotify.com/album/" + album_id

def link_artist(artist_id):
    return "https://open.spotify.com/artist/" + artist_id

def spotify_data(group):
    print("Starting Spotify related tasks...")
    spotify = login()

    group["spotify"] = get_artist(spotify, group["spotify"])
    collection = get_discography(spotify, group["spotify"])
    group["spotify"] = check_new_songs(group["spotify"], collection)

    for member in group["members"]:
        if "spotify" in member:
            member["spotify"] = get_artist(spotify, member["spotify"])
            collection = get_discography(spotify, member["spotify"])
            member["spotify"] = check_new_songs(member["spotify"], collection)

    print()

    return group


    
    
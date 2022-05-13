#!/usr/bin/env python3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from utils import display_num, convert_num, download_image
from tweet import twitter_post, twitter_post_image

module = "Spotify"

def login():
    """Logs in to Spotify

    Client credential authorization flow
    The following API keys are needed to be set as environment variables:

      * SPOTIPY_CLIENT_ID
      * SPOTIPY_CLIENT_SECRET
      
    You can request API keys on the `Spotify Developer Dashboard <https://developer.spotify.com/dashboard/>`_

    See https://spotipy.readthedocs.io/en/2.16.1/#authorization-code-flow for more details
    """

    print("[{}] Logging in...".format(module))
    
    auth_manager = SpotifyClientCredentials()
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    return spotify

def get_artist(spotify, artist, hashtags):
    """Gets details about an artist

    It tweets if the artist reaches a new goal of followers on Spotify

    Args:
      - spotify: The Spotify instance
      - artist: dictionary that contains all the data about the single artist
      - hashtags: hashtags to append to the Tweet

    Returns:
      an artist dictionary with updated profile details
    """
    # Generate URI
    artist["uri"] = 'spotify:artist:' + artist["id"]

    artist_details = spotify.artist(artist["uri"])


    artist["name"] = artist_details["name"]
    print("[{}] ({}) Getting details... (ID: {})".format(module, artist["name"], artist["id"]))

    artist["popularity"] = artist_details["popularity"]
    artist["genres"] = artist_details["genres"]
    try:
        artist["image"] = artist_details["images"][0]["url"]
    except:
        artist["image"] = None
        print("WARNING: Cannot fetch image of {}".format(artist["name"])) # This fix is needed for artists without a profile image

    if convert_num("100K", artist_details["followers"]["total"]) > convert_num("100K", artist["followers"]):
        artist["followers"] = artist_details["followers"]["total"]
        twitter_post_image(
            "{} reached {} followers on #Spotify\n{}\n{}".format(artist["name"], display_num(artist["followers"], decimal=True), link_artist(artist["id"]), hashtags),
            download_image(artist["image"]),
            display_num(artist["followers"], short=True, decimal=True),
            text_size=125
            )

    return artist

def get_discography(spotify, artist):
    """Gets all the releases of an artist

    A release is single, EP, mini-album or album: Spotify simply calls them all "albums"

    Example:

      * `DDU-DU-DDU-DU <https://open.spotify.com/album/2811CkGSYR9SUtIoFWWiTk>`_ of BLACKPINK is a **single**
      * `SQUARE UP <https://open.spotify.com/album/0wOiWrujRbxlKEGWRQpKYc>`_ of BLACKPINK is a **mini-album**
      * `THE ALBUM <https://open.spotify.com/album/71O60S5gIJSIAhdnrDIh3N>`_ of BLACKPINK is (really) an **album**
    
    It also gets releases where the artist is **featured**.
    Example:

      * `Sour Candy <https://open.spotify.com/album/6y6lP1WRfqEhv8RLy4ufZB>`_ is a song of Lady Gaga, but BLACKPINK are featured  

    Spotify also makes many "clones" of the same album: there could be extended albums or albums that later added tracks.
    Each one of this makes a duplicate of the same album.
    So this function also tries to clean up the discography by removing duplicates.

    Args:
      - spotify: The Spotify instance
      - artist: dictionary that contains all the data about the single artist

    Returns:
      an dictionary with updated discography details
    """

    print("[{}] ({}) Fetching discography...".format(module, artist["name"]))

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
    
    print("[{}] ({}) Fetched {} songs".format(module, artist["name"], z))

    # Remove duplicates
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

    print("[{}] ({}) After removing duplicates we have {} releases (singles/EPs/albums)".format(module, artist["name"], z))

    # Uncomment for debug: it prints all the albums and singles fetched
    #
    # for album in result:
    #     print(album["name"].upper())
    #     for track in album["tracks"]:
    #         print(track["name"])
    #     print()

    return result

def check_new_songs(artist, collection, hashtags):
    """Checks if there is any new song

    It compares the old discography of the artist with the new (already fetched) discography.
    It tweets if there is a new release or featuring of the artist.

    Args:
      - artist: dictionary that contains all the data about the single artist
      - collection: dictionary that contains all the updated discography of the artist
      - hashtags: hashtags to append to the Tweet

    Returns:
      an artist dictionary with updated discography details
    """
    print("[{}] ({}) Checking new songs...".format(module, artist["name"]))

    # Skip check if discography is empty
    if "discography" in artist:
      old = artist["discography"]

      for album in collection:
          found = False
          for old_album in old:
              if album["name"].lower() == old_album["name"].lower():
                  found = True
                  break
          if not found:
              if album["type"] != 'appears_on':
                  twitter_post_image(
                      "{} released a new {} on #Spotify: {}\n{}\n{}".format(artist["name"], album["type"], album["name"], link_album(album["id"]), hashtags),
                      download_image(album["image"]),
                      None
                      )
              else:
                  try:
                      twitter_post("{} appeared on {} by {} with the song {}\n{}\n{} #spotify".format(artist["name"], album["name"], album["artist_collab"], album["tracks"][0]["name"], link_album(album["id"]), hashtags))
                  except IndexError:
                      print("WARNING: Skipped one 'appeared on' since there was not a valid response from Spotify")
    
    artist["discography"] = collection
    return artist

def link_album(album_id):
    """Generates a link to an album

    Args:
      album_id: ID of the album

    Returns:
      The link to that album on Spotify
    """
    return "https://open.spotify.com/album/" + album_id

def link_artist(artist_id):
    """Generates a link to an artist

    Args:
      artist_id: ID of the artist

    Returns:
      The link to that artist on Spotify
    """
    return "https://open.spotify.com/artist/" + artist_id

def spotify_data(group):
    """Runs all the Spotify related tasks

    It scrapes data from Spotify for the whole group and the single artists

    Args:
      group: dictionary with the data of the group to scrape

    Returns:
      the same group dictionary with updated data
    """
    print("[{}] Starting tasks...".format(module))
    spotify = login()

    group["spotify"] = get_artist(spotify, group["spotify"], group["hashtags"])
    collection = get_discography(spotify, group["spotify"])
    group["spotify"] = check_new_songs(group["spotify"], collection, group["hashtags"])

    for member in group["members"]:
        if "spotify" in member:
            member["spotify"] = get_artist(spotify, member["spotify"], member["hashtags"])
            collection = get_discography(spotify, member["spotify"])
            member["spotify"] = check_new_songs(member["spotify"], collection,  member["hashtags"])

    print()

    return group


    
    

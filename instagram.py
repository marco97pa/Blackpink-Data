#!/usr/bin/env python3
import os
from instagrapi import Client
from PIL import Image
import requests
from utils import display_num, convert_num, download
from tweet import twitter_post, twitter_post_image

module = "Instagram"

# Get Instagram cookies
ACCOUNT_USERNAME = os.environ.get('INSTAGRAM_ACCOUNT_USERNAME')
ACCOUNT_PASSWORD = os.environ.get('INSTAGRAM_ACCOUNT_PASSWORD')

# Init
cl = Client()


def instagram_data(group):
    """Runs all the Instagram related tasks

    It scrapes data from Instagram for the whole group and the single artists

    Args:
      group: dictionary with the data of the group to scrape

    Returns:
      the same group dictionary with updated data
    """

    print("[{}] Starting tasks...".format(module))

    # Login
    cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

    group, user_id = instagram_profile(group)
    group = instagram_last_post(group, user_id)

    for artist in group["members"]:
        artist, user_id = instagram_profile(artist)
        artist = instagram_last_post(artist, user_id)

    print()
    return group

def instagram_last_post(artist, user_id):
    """Gets the last post of a profile

    It tweets if there is a new post: if the timestamp of the latest stored post does not match with the latest fetched posts timestamp

    Args:
      - user_id: a profile ID
      - artist: a dictionary with all the details of the artist

    Returns:
      an dictionary containing all the updated data of the artist
    """

    print("[{}] ({}) Fetching new posts".format(module, artist["instagram"]["url"][26:-1]))

    medias = cl.user_medias(user_id, 5)
    
    for media in medias:
      # If the last post timestamp is greater (post is newest) or the saved post does not exist
      if "last_post" not in artist["instagram"] or media.taken_at.timestamp() > artist["instagram"]["last_post"]["timestamp"]:
        url = "https://www.instagram.com/p/" + media.code
        if len(media.resources) == 0:
            media.resources.append(media)
        if media.resources[0].media_type == 2:
            content_type = "video"
            filename = "temp.mp4"
            source = "{}".format(media.resources[0].video_url)
            download(source, filename)
            twitter_post_image(
              "{} posted a new {} on #Instagram:\n{}\n{}\n{}\n\n{}".format(artist["name"], content_type, clean_caption(media.caption_text), media.taken_at.timestamp(), url, artist["hashtags"]),
              filename,
              None
          )
        else:
          content_type = "photo"
          i = 0
          filenames = []
          for resource in media.resources:
            if resource.media_type == 1:
              i=i+1
              if i >= 5:
                break
              filename = "temp{}.jpg".format(i)
              source = "{}".format(resource.thumbnail_url)
              download(source, filename)
              filenames.append(filename)
          twitter_post_image(
              "{} posted a new {} on #Instagram:\n{}\n{}\n{}\n\n{}".format(artist["name"], content_type, clean_caption(media.caption_text), media.taken_at.timestamp(), url, artist["hashtags"]),
              filenames,
              None
          )
      else:
        break

    last_post = {}
    last_post["url"] = "https://www.instagram.com/p/" + medias[0].code
    last_post["caption"] = medias[0].caption_text
    last_post["timestamp"] = medias[0].taken_at.timestamp()

    artist["instagram"]["last_post"] = last_post
    
    return artist

def instagram_profile(artist):
    """Gets the details of an artist on Instagram

    It tweets if the artist reaches a new followers goal

    Args:
      artist: a dictionary with all the details of the artist

    Returns:
      - an dictionary containing all the updated data of the artist
      - a Profile ID
    """
    username = artist["instagram"]["url"][26:-1]

    print("[{}] ({}) Fetching profile details".format(module, username))

    user_id = cl.user_id_from_username(username)
    info = cl.user_info(user_id)
    artist["instagram"]["posts"] = info.media_count
    # Update profile pic
    artist["instagram"]["image"] = "{}".format(info.profile_pic_url)

    # Add followers if never happened before
    if "followers" not in artist["instagram"]:
      artist["instagram"]["followers"] = info.follower_count

    # Update followers only if there is an increase (fixes https://github.com/marco97pa/Blackpink-Data/issues/11)
    if info.follower_count > artist["instagram"]["followers"]:
        print("[{}] ({}) Followers increased {} --> {}".format(module, artist["instagram"]["url"][26:-1], artist["instagram"]["followers"], info.follower_count))
        if convert_num("M", artist["instagram"]["followers"]) != convert_num("M", info.follower_count):
            twitter_post_image(
                "{} reached {} followers on #Instagram\n{}".format(artist["name"], display_num(info.follower_count), artist["hashtags"]),
                download_profile_pic(artist["instagram"]["image"]),
                display_num(info.follower_count, short=True),
                text_size=50
                )
        artist["instagram"]["followers"] = info.follower_count
    
    return artist, user_id

def clean_caption(caption):
    """Removes unnecessary parts of an Instagram post caption

    It removes all the hashtags and converts tags in plain text (@marco97pa --> marco97pa)

    Args:
      caption: a text

    Returns:
      the same caption without hashtags and tags
    """

    clean = ""

    words = caption.split()
    for word in words:
        if word[0] != "#":
            if word[0] == "@":
                clean += word[1:] + " "
            else:
                clean += word + " "

    return clean[:90]

def download_profile_pic(url):
    """Downloads an image, given an url

    The image is saved in the download.jpg file

    Args:
      url: source from where download the image
    """

    filename = "download.jpg"
    response = requests.get(url)

    file = open(filename, "wb")
    file.write(response.content)
    file.close()

    img = Image.open(filename)
    img = img.resize((400, 400), Image.ANTIALIAS)
    img.save(filename)

    return filename

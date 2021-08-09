#!/usr/bin/env python3
import os
from instascrape import *
from utils import display_num, convert_num, download_image
from tweet import twitter_post, twitter_post_image

# Get Instagram cookies
instagram_sessionid = os.environ.get('INSTAGRAM_SESSION_ID')
headers = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
"cookie": f"sessionid={instagram_sessionid};"}

module = "Instagram"

def instagram_data(group):
    """Runs all the Instagram related tasks

    It scrapes data from Instagram for the whole group and the single artists

    Args:
      group: dictionary with the data of the group to scrape

    Returns:
      the same group dictionary with updated data
    """

    print("[{}] Starting tasks...".format(module))
    group, ig_profile = instagram_profile(group)
    group = instagram_last_post(group, ig_profile)

    for artist in group["members"]:
        artist, ig_profile = instagram_profile(artist)
        artist = instagram_last_post(artist, ig_profile)

    print()
    return group

def instagram_last_post(artist, profile):
    """Gets the last post of a profile

    It tweets if there is a new post: if the timestamp of the latest stored post does not match with the latest fetched posts timestamp

    Args:
      - profile: a Profile instance, already scraped
      - artist: a dictionary with all the details of the artist

    Returns:
      an dictionary containing all the updated data of the artist
    """

    print("[{}] ({}) Fetching new posts".format(module, artist["instagram"]["url"][26:-1]))

    recents = profile.get_recent_posts()
    
    for recent in recents:
      recent.scrape(headers=headers)
      # If the last post timestamp is greater (post is newest) or the saved post does not exist
      if "last_post" not in artist["instagram"] or recent.timestamp > artist["instagram"]["last_post"]["timestamp"]:
        url = "https://www.instagram.com/p/" + recent.shortcode
        if recent.is_video:
            content_type = "video"
            filename = "temp.mp4"
        else:
            content_type = "photo"
            filename = "temp.jpg"
        recent.download(filename)
        twitter_post_image(
            "{} posted a new {} on #Instagram:\n{}\n{}\n{}\n\n{}".format(artist["name"], content_type, clean_caption(recent.caption), recent.timestamp, url, artist["hashtags"]),
            filename,
            None
        )
      else:
        break

    last_post = {}
    last_post["url"] = "https://www.instagram.com/p/" + recents[0].shortcode
    last_post["caption"] = recents[0].caption
    last_post["timestamp"] = recents[0].timestamp

    artist["instagram"]["last_post"] = last_post
    
    return artist

def instagram_profile(artist):
    """Gets the details of an artist on Instagram

    It tweets if the artist reaches a new followers goal

    Args:
      artist: a dictionary with all the details of the artist

    Returns:
      - an dictionary containing all the updated data of the artist
      - a Profile instance
    """

    print("[{}] ({}) Fetching profile details".format(module, artist["instagram"]["url"][26:-1]))

    profile = Profile(artist["instagram"]["url"])
    profile = profile.scrape(headers=headers, inplace=False)
    artist["instagram"]["posts"] = profile.posts
    # Update profile pic
    artist["instagram"]["image"] = profile.profile_pic_url_hd

    # Add followers if never happened before
    if "followers" not in artist["instagram"]:
      artist["instagram"]["followers"] = profile.followers

    # Update followers only if there is an increase (fixes https://github.com/marco97pa/Blackpink-Data/issues/11)
    if profile.followers > artist["instagram"]["followers"]:
        print("[{}] ({}) Followers increased {} --> {}".format(module, artist["instagram"]["url"][26:-1], artist["instagram"]["followers"], profile.followers))
        if convert_num("M", artist["instagram"]["followers"]) != convert_num("M", profile.followers):
            twitter_post_image(
                "{} reached {} followers on #Instagram\n{}".format(artist["name"], display_num(profile.followers), artist["hashtags"]),
                download_image(artist["instagram"]["image"]),
                display_num(profile.followers, short=True),
                text_size=50
                )
        artist["instagram"]["followers"] = profile.followers
    
    return artist, profile

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

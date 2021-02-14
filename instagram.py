#!/usr/bin/env python3
import os
from instascrape import *
from utils import display_num, convert_num, download_image
from tweet import twitter_post, twitter_post_image

# Get Instagram cookies
instagram_sessionid = os.environ.get('INSTAGRAM_SESSION_ID')
headers = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
"cookie": f"sessionid={instagram_sessionid};"}

hashtags = "\n@BLACKPINK #blinks #photo #pic"

def instagram_data(group):
    """ Starts the Instagram tasks (uses the insta-scrape module https://pypi.org/project/insta-scrape/)

    Args:
    - group (dict): a dictionary containing all the group data
    """
    print("Starting Instagram related tasks...")
    group, ig_profile = instagram_profile(group)
    group = instagram_last_post(group, ig_profile)

    for artist in group["members"]:
        artist, ig_profile = instagram_profile(artist)
        artist = instagram_last_post(artist, ig_profile)

    print()
    return group

def instagram_last_post(artist, profile):
    print("Fetching new posts for {}".format(artist["instagram"]["url"]))

    recents = profile.get_recent_posts()
    recents[0].scrape(headers=headers)
    if artist["instagram"]["last_post"]["timestamp"] != recents[0].timestamp:
        artist["instagram"]["last_post"]["url"] = "https://www.instagram.com/p/" + recents[0].shortcode
        artist["instagram"]["last_post"]["caption"] = recents[0].caption
        artist["instagram"]["last_post"]["timestamp"] = recents[0].timestamp
        if recents[0].is_video:
            content_type = "video"
            filename = "temp.mp4"
        else:
            content_type = "photo"
            filename = "temp.jpg"
        recents[0].download(filename)
        twitter_post_image(
            "#{} posted a new {} on #Instagram:\n{}\n{}\n\n{}".format(artist["name"].upper(), content_type, clean_caption(artist["instagram"]["last_post"]["caption"]), artist["instagram"]["last_post"]["url"], hashtags),
            filename,
            None
        )
    return artist

def instagram_profile(artist):
    print("Fetching profile details for {}".format(artist["instagram"]["url"]))

    profile = Profile(artist["instagram"]["url"])
    profile.scrape(headers=headers)
    artist["instagram"]["posts"] = profile.posts
    # Temporary fix to https://github.com/marco97pa/Blackpink-Data/issues/4
    # Keep this line commented until this issue of instascrape is fixed:
    # https://github.com/chris-greening/instascrape/issues/90
    #
    # artist["instagram"]["image"] = profile.profile_pic_url_hd

    if convert_num("M", artist["instagram"]["followers"]) != convert_num("M", profile.followers):
        twitter_post_image(
            "#{} reached {} followers on #Instagram\n{}".format(artist["name"].upper(), display_num(profile.followers), hashtags),
            download_image(artist["instagram"]["image"]),
            display_num(profile.followers, short=True),
            text_size=50
            )
    artist["instagram"]["followers"] = profile.followers
    
    return artist, profile

def clean_caption(caption):
    clean = ""

    words = caption.split()
    for word in words:
        if word[0] != "#":
            if word[0] == "@":
                clean += word[1:] + " "
            else:
                clean += word + " "

    return clean[:100]
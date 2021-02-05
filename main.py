#!/usr/bin/env python3
import sys
import yaml
import requests
import json
import datetime
import tweepy
from instascrape import *
from youtube_api import YoutubeDataApi
from PIL import Image, ImageFont, ImageDraw 
import os

#Change to True for testing purposes: it won't Tweet anything
test_mode = False

# Get Twitter API keys
consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
access_token = os.environ.get('TWITTER_ACCESS_KEY')
access_token_secret = os.environ.get('TWITTER_ACCESS_SECRET')

# Get API key for YouTube
youtube_api_key = os.environ.get('YOUTUBE_API_KEY')

# Constants
url_youtube_video = "https://youtu.be/"
hashtags_youtube = "@BLACKPINK #stats #charts #blinks #youtubemusic #music #lisa #jisoo #jennie #rosè #blackpink"
hashtags_instagram = "@BLACKPINK #post #photo #blinks #lisa #jisoo #jennie #rosè #pic #blackpink"

def load_group():
    print("Loading data from YAML file...")

    with open('data.yaml', encoding="utf-8") as file:
        group = yaml.load(file, Loader=yaml.FullLoader)

        out = "{} consist of ".format(group["name"])
        for artist in group["members"]:
            out += artist["name"]
            out += " "
        print(out + "\n")

        return group

def write_group(group):
    print("Writing data to YAML file...")
    with open('data.yaml', 'w', encoding="utf-8") as file:
        yaml.dump(group, file, sort_keys=False, allow_unicode=True)

def youtube_data(yt, group):
    print("Starting Youtube related tasks...")

    # Getting channel data and stats
    channel_data = youtube_get_channel(yt, group["youtube"]["url"])
    group["youtube"] = youtube_check_channel_change(group["youtube"], channel_data)

    # Getting video data and stats
    videos = youtube_get_videos(yt, group["youtube"]["playlist"])
    group["youtube"]["videos"] = youtube_check_videos_change(group["name"], group["youtube"]["videos_scale"], group["youtube"]["videos"], videos)

    # Getting Youtube data for each member
    for member in group["members"]:
        if "youtube" in member:
            channel_data = youtube_get_channel(yt, member["youtube"]["url"])
            member["youtube"] = youtube_check_channel_change(member["youtube"], channel_data)

            videos = youtube_get_videos(yt, member["youtube"]["playlist"])
            member["youtube"]["videos"] = youtube_check_videos_change(member["name"], member["youtube"]["videos_scale"], member["youtube"]["videos"], videos)
    
    print()
    return group

def youtube_get_channel(yt, channel_id):
    data = yt.get_channel_metadata(channel_id, snippet="statistics, snippet")

    channel_data = {
       "name": data["title"],
       "subs": data["subscription_count"],
       "views": data["view_count"],
       "playlist": data["playlist_id_uploads"],
       "image": youtube_get_profile_image(channel_id)
       }

    print("Fetched {} Youtube channel".format(channel_data["name"]))

    return channel_data

def youtube_get_videos(yt, playlist_id):
    playlist = yt.get_videos_from_playlist_id(playlist_id)
    
    video_ids = []
    for video in playlist:
        video_ids.append(video["video_id"])
    
    videos = []
    videos_data = yt.get_video_metadata(video_ids)
    videos_data
    for video in videos_data:
        videos.append({"name": video["video_title"], "url": video["video_id"], "views": video["video_view_count"], "image": video["video_thumbnail"]})
    
    print("Fetched {} videos".format(len(videos)))
    
    return videos

def youtube_get_profile_image(channel_id):
    page = requests.get("https://www.googleapis.com/youtube/v3/channels?part=snippet&id=" + channel_id + "&fields=items(id%2Csnippet%2Fthumbnails)&key=" + youtube_api_key)
    response = json.loads(page.content)
    return response["items"][0]["snippet"]["thumbnails"]["high"]["url"]

def youtube_check_channel_change(old_channel, new_channel):
    
    # Tweet if subs reach a new 100 thousands
    if convert_num("100K", new_channel["subs"]) != convert_num("100K", old_channel["subs"]):
        twitter_post_image(
            "{} reached {} subscribers on #YouTube\n{}".format(new_channel["name"], display_num(new_channel["subs"], decimal=True), hashtags_youtube),
            download_image(new_channel["image"]),
            display_num(new_channel["subs"], short=True, decimal=True),
            text_size=150,
            test=test_mode
        )
    old_channel["subs"] = new_channel["subs"]

    # Tweet if total views reach a new mark (based on the views_scale)
    if convert_num(old_channel["views_scale"], new_channel["views"]) != convert_num(old_channel["views_scale"], old_channel["total_views"]):
        twitter_post_image(
            "{} reached {} total views on #YouTube\n{}".format(new_channel["name"], display_num(new_channel["views"]), hashtags_youtube),
            download_image(new_channel["image"]),
            display_num(new_channel["views"], short=True),
            test=test_mode
        )
    old_channel["total_views"] = new_channel["views"]

    old_channel["playlist"] = new_channel["playlist"]
    old_channel["name"] = new_channel["name"]
    old_channel["image"] = new_channel["image"]

    return old_channel

def youtube_check_videos_change(name, scale, old_videos, new_videos):
    if old_videos is not None:
        for new_video in new_videos:
            found = False
            for old_video in old_videos:
                if new_video["url"] == old_video["url"]:
                    found = True
                    # Tweet if a video reaches a new record (based on the scale parameter)
                    if convert_num(scale, new_video["views"]) != convert_num(scale, old_video["views"]):
                        twitter_post_image(
                            "{} reached {} views on #YouTube\n{}\n{}".format(new_video["name"], display_num(new_video["views"]), url_youtube_video + new_video["url"], hashtags_youtube),
                            download_image(new_video["image"]),
                            display_num(new_video["views"], short=True),
                            text_size=100,
                            crop=True,
                            test=test_mode
                        )
            if not found:
                twitter_post_image(
                    "{} uploaded a new #video on #YouTube: {}\n{}\n{}".format(name, new_video["name"], url_youtube_video + new_video["url"], hashtags_youtube),
                    download_image(new_video["image"]),
                    "NEW",
                    text_size=100,
                    crop=True,
                    test=test_mode
                    )
    return new_videos

def check_birthdays(group):
    now = datetime.datetime.today()
    print("Today is {}".format(now.date()))

    print("Checking birthdays...")
    for member in group["members"]:
        birthday = datetime.datetime.strptime(member["birthday"], '%d/%m/%Y')
        difference = round((now - birthday).days / 365.25)
        birthday = birthday.replace(year=now.year)
        if birthday.date() == now.date():
            twitter_post(
                "Today is {}'s birthday! She did {} years\n#{} #{}bday #blackpink @BLACKPINK".format(member["name"], difference, member["name"], member["name"]),
                test=test_mode
                )
    print()


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
    recents[0].scrape()
    if artist["instagram"]["last_post"]["timestamp"] != recents[0].timestamp:
        artist["instagram"]["last_post"]["url"] = "https://www.instagram.com/p/" + recents[0].shortcode
        artist["instagram"]["last_post"]["caption"] = recents[0].caption
        artist["instagram"]["last_post"]["timestamp"] = recents[0].timestamp
        recents[0].download("temp.jpg")
        twitter_post_image(
            "{} posted a new photo on #Instagram\n{}\n{}\n{}".format(artist["name"], artist["instagram"]["last_post"]["url"], artist["instagram"]["last_post"]["caption"][:100], hashtags_instagram),
            "temp.jpg",
            None,
            test=test_mode
        )
    return artist

def instagram_profile(artist):
    print("Fetching profile details for {}".format(artist["instagram"]["url"]))

    profile = Profile(artist["instagram"]["url"])
    profile.scrape()
    if artist["instagram"]["followers"] != profile.followers:
        if convert_num("M", artist["instagram"]["followers"]) != convert_num("M", profile.followers):
            twitter_post(
                "{} reached {} followers on #Instagram\n{}".format(artist["name"], display_num(profile.followers), hashtags_instagram),
                test=test_mode)
        artist["instagram"]["followers"] = profile.followers
    artist["instagram"]["posts"] = profile.posts
    artist["instagram"]["image"] = profile.profile_pic_url_hd
    return artist, profile

def twitter_repost(twitter, test=False):
    print("Starting Twitter repost task...")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    print("Fetching tweets for {}".format(twitter["url"]))

    if twitter["last_tweet_id"] is not None:
        tweets = api.user_timeline(screen_name = twitter["url"], 
                                since_id = twitter["last_tweet_id"],
                                include_rts = False,
                                # extended mode to get full text
                                tweet_mode = "extended"
                                )
    else:
        tweets = api.user_timeline(screen_name = twitter["url"], 
                                # Take only the last tweet
                                count = 1,
                                include_rts = False,
                                # extended mode to get full text
                                tweet_mode = "extended"
                                )

    for tweet in tweets:
        print("Retwitting this tweet from @{}".format(twitter["url"]))
        print("Tweet ID: {}".format(tweet.id))
        print("Datetime: {}".format(tweet.created_at))
        print(tweet.full_text[:20])
        if test is False:
            api.retweet(tweet.id)

    if len(tweets) > 0:
        twitter["last_tweet_id"] = tweets[0].id
        
    print()
    return twitter

def twitter_post(message, test=False):
    """ Post a message on Twitter (uses the Tweepy module)
    
    Args:
        message (str): a string containing the message to be posted
    """
    message = message[:270]
    print(message+"\n")

    if test is False:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        try:
            api.update_status(message)
        except tweepy.TweepError as error:
            print("WARNING: Tweet NOT posted because " + str(error.reason))

def twitter_post_image(message, filename, text, text_size=200, crop=False, test=False):
    """ Post a photo with message on Twitter (uses the Tweepy module)
    
    Args:
        message (str): a string containing the message to be posted
        url (str): filename of the image to be posted
    """

    if text is not None:
        edit_image(filename, text, text_size=text_size, crop=crop)
    
    message = message[:270]
    print(message)
    print("Image: " + filename + "\n")

    if test is False:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        api.update_with_media(filename, status=message)
        os.remove(filename)

def edit_image(filename, text, text_size=200, crop=False):
    """ Edit an image by adding a text (uses the Pillow module)
    
    Args:
        filename (str): filename of the image to be modified
        text (str): text to be added
    """
    #Open image
    my_image = Image.open(filename)
    # Crop
    if crop:
        # Size of the image in pixels (size of orginal image) 
        width, height = my_image.size 
        
        # Setting the points for cropped image 
        left = 0
        right = width
        top = height / 8
        bottom = height - (height / 8)
        
        # Cropped image of above dimension 
        my_image = my_image.crop((left, top, right, bottom)) 
    
    # Open font
    title_font = ImageFont.truetype('Montserrat-Bold.ttf', text_size)
    # Edit image
    image_editable = ImageDraw.Draw(my_image)
    # Add text
    image_editable.text((50,15), text, (237, 230, 211), font=title_font)
    # Save image
    my_image.save(filename)

def convert_num(mode, num):
    num = int(num)

    if mode == "100K":
        num = int(num / 100000)
    elif mode == "M":
        num = int(num / 1000000)
    elif mode == "10M":
        num = int(num / 10000000)
    elif mode == "100M":
        num = int(num / 100000000)
    elif mode == "B":
        num = int(num / 1000000000)
    return num

def display_num(num, short=False, decimal=False):
    num = int(num)
    digits = len(str(abs(num)))

    if digits <= 6:
        num = int(num / 1000)
        if not short:
            out = "{} thousand".format(num)
        else:
            out = "{}.000".format(num)
    elif digits > 6 and digits <= 9:
        if not decimal:
            num = int(num / 1000000)
            if not short:
                out = "{} million".format(num)
            else:
                out = "{} Mln".format(num)
        else:
            num = num / 1000000
            if not short:
                out = "{:0.1f} million".format(num)
            else:
                out = "{:0.1f} Mln".format(num)
    elif digits > 9:
        num = num / 1000000000
        if not short:
            out = "{:0.1f} billion".format(num)
        else:
            out = "{:0.1f} Bln".format(num)
    return out

def download_image(url):
    filename = "download.jpg"
    response = requests.get(url)

    file = open(filename, "wb")
    file.write(response.content)
    file.close()

    return filename


if __name__ == '__main__':
    
    group = load_group()

    check_birthdays(group)

    youtube = YoutubeDataApi(youtube_api_key)
    group = youtube_data(youtube, group)

    group["twitter"] = twitter_repost(group["twitter"], test=test_mode)

    #group = instagram_data(group)

    write_group(group)

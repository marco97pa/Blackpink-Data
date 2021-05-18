#!/usr/bin/env python3
import os
import requests
import json
from youtube_api import YoutubeDataApi
from utils import display_num, convert_num, download_image
from tweet import twitter_post, twitter_post_image

# Get API key for YouTube
youtube_api_key = os.environ.get('YOUTUBE_API_KEY')

url_video = "https://youtu.be/"

module = "YouTube"

def youtube_data(group):
    """Runs all the YouTube related tasks

    It scrapes data from YouTube for the whole group and the single artists

    Args:
      group: dictionary with the data of the group to scrape

    Returns:
      the same group dictionary with updated data
    """

    print("[{}] Starting tasks...".format(module))
    yt = YoutubeDataApi(youtube_api_key)

    # Getting channel data and stats
    channel_data = youtube_get_channel(yt, group["youtube"]["url"])
    group["youtube"] = youtube_check_channel_change(group["youtube"], channel_data, group["hashtags"])

    # Getting video data and stats
    videos = youtube_get_videos(yt, group["youtube"]["playlist"], group["youtube"]["name"])
    group["youtube"]["videos"] = youtube_check_videos_change(group["name"], group["youtube"]["videos_scale"], group["youtube"]["videos"], videos, group["hashtags"])

    # Getting Youtube data for each member
    for member in group["members"]:
        if "youtube" in member:
            channel_data = youtube_get_channel(yt, member["youtube"]["url"])
            member["youtube"] = youtube_check_channel_change(member["youtube"], channel_data, member["hashtags"])

            videos = youtube_get_videos(yt, member["youtube"]["playlist"], member["youtube"]["name"])
            member["youtube"]["videos"] = youtube_check_videos_change(member["name"], member["youtube"]["videos_scale"], member["youtube"]["videos"], videos, member["hashtags"])
    
    print()
    return group

def youtube_get_channel(yt, channel_id):
    """Gets details about a channel

    Args:
      - yt: The YouTube instance
      - channel_id: the ID of that channel on YouTube

    Returns:
      an dictionary containing all the scraped data of that channel
    """

    data = yt.get_channel_metadata(channel_id, snippet="statistics, snippet")

    channel_data = {
       "name": data["title"],
       "subs": data["subscription_count"],
       "views": data["view_count"],
       "playlist": data["playlist_id_uploads"],
       "image": youtube_get_profile_image(channel_id)
       }

    print("[{}] ({}) Fetched channel".format(module, channel_data["name"]))

    return channel_data

def youtube_get_videos(yt, playlist_id, name):
    """Gets videos from a playlist

    Args:
      - yt: The YouTube instance
      - playlist_id: the ID of the playlist on YouTube
      - name: name of the channel owner of the playlist

    Returns:
      a list of videos
    """

    playlist = yt.get_videos_from_playlist_id(playlist_id)
    
    video_ids = []
    for video in playlist:
        video_ids.append(video["video_id"])
    
    videos = []
    videos_data = yt.get_video_metadata(video_ids)
    videos_data
    for video in videos_data:
        videos.append({"name": video["video_title"], "url": video["video_id"], "views": video["video_view_count"], "image": video["video_thumbnail"]})
    
    print("[{}] ({}) Fetched {} videos".format(module, name, len(videos)))
    
    return videos

def youtube_get_profile_image(channel_id):
    """Gets profile image of a channel

    Args:
      channel_id: the ID of the channel on YouTube

    Returns:
      an url to an high quality thumbanail of that channel
    """

    page = requests.get("https://www.googleapis.com/youtube/v3/channels?part=snippet&id=" + channel_id + "&fields=items(id%2Csnippet%2Fthumbnails)&key=" + youtube_api_key)
    response = json.loads(page.content)
    return response["items"][0]["snippet"]["thumbnails"]["high"]["url"]

def youtube_check_channel_change(old_channel, new_channel, hashtags):
    """Checks if there is any change in the number of subscribers or total views of the channel

    It compares the old channel data with the new (already fetched) data.
    It tweets if the channel reaches a new goal of subscribers or total views on YouTube

    Args:
      - old_channel: dictionary that contains all the old data of the channel
      - new_channel: dictionary that contains all the updated data of the channel
      - hashtags: hashtags to add to the Tweet

    Returns:
      a dictionary with updated data of the channel
    """
    
    # Tweet if subs reach a new 100 thousands
    if convert_num("100K", new_channel["subs"]) != convert_num("100K", old_channel["subs"]):
        twitter_post_image(
            "{} reached {} subscribers on #YouTube\n{}".format(new_channel["name"], display_num(new_channel["subs"], decimal=True), hashtags),
            download_image(new_channel["image"]),
            display_num(new_channel["subs"], short=True, decimal=True),
            text_size=150
        )
    old_channel["subs"] = new_channel["subs"]

    # Tweet if total views increase and reach a new mark (based on the views_scale)
    if new_channel["views"] > old_channel["total_views"]:
      if convert_num(old_channel["views_scale"], new_channel["views"]) != convert_num(old_channel["views_scale"], old_channel["total_views"]):
          twitter_post_image(
              "{} reached {} total views on #YouTube\n{}".format(new_channel["name"], display_num(new_channel["views"]), hashtags),
              download_image(new_channel["image"]),
              display_num(new_channel["views"], short=True)
          )
      old_channel["total_views"] = new_channel["views"]

    old_channel["playlist"] = new_channel["playlist"]
    old_channel["name"] = new_channel["name"]
    old_channel["image"] = new_channel["image"]

    return old_channel

def youtube_check_videos_change(name, scale, old_videos, new_videos, hashtags):
    """Checks if there is any new video

    It compares the old videos list of the artist with the new (already fetched) videos list.
    It tweets if there is a new release or if a video reaches a new views goal.

    Args:
      - name: name of the channel
      - scale: number scale that triggers a new views goal (example: reaches a new million, a new billion...)
      - old_videos: list that contains all the old videos
      - new_videos: list that contains all the updated videos
      - hashtags: hashtags to append to the Tweet

    Returns:
      new_videos
    """
    
    if old_videos is not None:
        for new_video in new_videos:
            found = False
            for old_video in old_videos:
                if new_video["url"] == old_video["url"]:
                    found = True
                    # Tweet if a video reaches a new record (based on the scale parameter)
                    if convert_num(scale, new_video["views"]) != convert_num(scale, old_video["views"]):
                        twitter_post_image(
                            "{} reached {} views on #YouTube\n{}\n{} #{}".format(new_video["name"], display_num(new_video["views"]), url_video + new_video["url"], hashtags, name),
                            download_image(new_video["image"]),
                            display_num(new_video["views"], short=True),
                            text_size=100,
                            crop=True
                        )
            if not found:
                twitter_post_image(
                    "{} uploaded a new #video on #YouTube: {}\n{}\n{}".format(name, new_video["name"], url_video + new_video["url"], hashtags),
                    download_image(new_video["image"]),
                    "NEW",
                    text_size=100,
                    crop=True
                    )
    return new_videos
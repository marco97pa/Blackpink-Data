#!/usr/bin/env papihon3
import os
import requests
import json
from pyyoutube import Api
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
    api = Api(api_key=youtube_api_key)

    # Getting channel data and stats
    channel_data = youtube_get_channel(api, group["youtube"]["url"])
    group["youtube"] = youtube_check_channel_change(group["youtube"], channel_data, group["hashtags"])

    # Getting video data and stats
    videos = youtube_get_videos(api, group["youtube"]["playlist"], group["youtube"]["name"])
    group["youtube"]["videos"] = youtube_check_videos_change(group["name"], group["youtube"]["videos_scale"], group["youtube"]["videos"], videos, group["hashtags"])

    # Getting Youtube data for each member
    for member in group["members"]:
        if "youtube" in member:
            channel_data = youtube_get_channel(api, member["youtube"]["url"])
            member["youtube"] = youtube_check_channel_change(member["youtube"], channel_data, member["hashtags"])

            videos = youtube_get_videos(api, member["youtube"]["playlist"], member["youtube"]["name"])
            member["youtube"]["videos"] = youtube_check_videos_change(member["name"], member["youtube"]["videos_scale"], member["youtube"]["videos"], videos, member["hashtags"])
    
    print()
    return group

def youtube_get_channel(api, channel_id):
    """Gets details about a channel

    Args:
      - api: The YouTube instance
      - channel_id: the ID of that channel on YouTube

    Returns:
      an dictionary containing all the scraped data of that channel
    """

    data = api.get_channel_info(channel_id=channel_id)
    channel = data.items[0]

    channel_data = {
       "name": channel.snippet.title,
       "subs": channel.statistics.subscriberCount,
       "views": channel.statistics.viewCount,
       "playlist": channel.contentDetails.relatedPlaylists.uploads,
       "image": channel.snippet.thumbnails.high.url
       }

    print("[{}] ({}) Fetched channel".format(module, channel_data["name"]))

    return channel_data

def youtube_get_videos(api, playlist_id, name):
    """Gets videos from a playlist

    Args:
      - api: The YouTube instance
      - playlist_id: the ID of the playlist on YouTube
      - name: name of the channel owner of the playlist

    Returns:
      a list of videos
    """
    videos = []

    playlist = api.get_playlist_items(playlist_id=playlist_id, count=None)
    
    for video in playlist.items:
      # Try to get the highest quality thumbnail
      if video.snippet.thumbnails.maxres is None:
        thumbnail = video.snippet.thumbnails.standard.url
      else:
        thumbnail = video.snippet.thumbnails.maxres.url

        videos.append(
         {"name": video.snippet.title,
         "url": video.snippet.resourceId.videoId,
         "image": thumbnail}
        )
    
    print("[{}] ({}) Fetched {} videos".format(module, name, len(videos)))
    
    return videos


def youtube_check_channel_change(old_channel, new_channel, hashtags):
    """Checks if there is any change in the number of subscribers or total views of the channel

    It compares the old channel data with the new (already fetched) data.

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
            if not found:
                twitter_post_image(
                    "{} uploaded a new #video on #YouTube: {}\n{}\n{}".format(name, new_video["name"], url_video + new_video["url"], hashtags),
                    download_image(new_video["image"]),
                    "NEW",
                    text_size=100,
                    crop=True
                    )
    return new_videos
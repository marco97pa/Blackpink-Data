#!/usr/bin/env python3
import os
import tweepy
import sys
import time

import json
import requests
from requests_oauthlib import OAuth1
from PIL import Image, ImageFont, ImageDraw 

# Get Twitter API keys
consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
access_token = os.environ.get('TWITTER_ACCESS_KEY')
access_token_secret = os.environ.get('TWITTER_ACCESS_SECRET')

module = "Twitter"

MEDIA_ENDPOINT_URL = 'https://upload.twitter.com/1.1/media/upload.json'

oauth = OAuth1(consumer_key,
  client_secret=consumer_secret,
  resource_owner_key=access_token,
  resource_owner_secret=access_token_secret)

test = False

def set_test_mode():
    """Enables the test mode

    Prevents tweets from being posted. They are still printed in the console.
    This is really useful for debugging purposes
    """

    global test 
    test = True

def retrieve_own_tweets(num=3):
    """Retrieves recent tweets made by the bot.

    Args:
      num: an integer with the number of tweets to retrieve.

    Returns:
      a list of tweet objects
    """

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    latest_tweets = api.user_timeline(screen_name="data_blackpink", count=num, tweet_mode="extended")
    return latest_tweets

def check_duplicates(message):
    """Checks tweet message against 3 latest user tweets to ensure no duplicative posts

    Args:
      message: a string containing the message to be posted

    Returns:
      Boolean which signals True if a duplicate is found
    """
    last_three = retrieve_own_tweets()
    last_three_messages = [tweet.full_text for tweet in last_three]  # list of tweet message strings to check against

    return message in last_three_messages

def twitter_repost(artist):
    """Retweets latest tweets of a given account

    Args:
      artist: a dictionary with all the details of the artist

    Returns:
      an dictionary containing all the updated data of the artist
    """
    print("[{}] Starting repost task...".format(module))
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    print("[{}] ({}) Fetching tweets".format(module, artist["twitter"]["url"]))

    if "last_tweet_id" in artist["twitter"] and artist["twitter"]["last_tweet_id"] is not None:
        tweets = api.user_timeline(screen_name = artist["twitter"]["url"], 
                                since_id = artist["twitter"]["last_tweet_id"],
                                include_rts = False,
                                # extended mode to get full text
                                tweet_mode = "extended"
                                )
    else:
        tweets = api.user_timeline(screen_name = artist["twitter"]["url"], 
                                # Take only the last tweet
                                count = 1,
                                include_rts = False,
                                # extended mode to get full text
                                tweet_mode = "extended"
                                )

    for tweet in tweets:
        print("Retwitting this tweet from @{}".format(artist["twitter"]["url"]))
        print("Tweet ID: {}".format(tweet.id))
        print("Datetime: {}".format(tweet.created_at))
        print(tweet.full_text[:20])
        if test is False:
            api.retweet(tweet.id)

    if len(tweets) > 0:
        artist["twitter"]["last_tweet_id"] = tweets[0].id
        
    print()
    return artist

def twitter_post(message):
    """ Post a message on Twitter (uses the Tweepy module)
    
    Args:
        message: a string containing the message to be posted
    """
    message = message[:270]
    print(message+"\n")

    if not check_duplicates(message):
        if test is False:
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth)
            
            try:
                api.update_status(message)
            except tweepy.TweepError as error:
                print("WARNING: Tweet NOT posted because " + str(error.reason))
    else:
        print("WARNING: Tweet NOT posted because it was a duplicate.")
          
def twitter_post_image(message, filename, text, text_size=200, crop=False):
    """ Post a photo with message on Twitter (uses the Tweepy module)
    
    Args:
        - message: a string containing the message to be posted
        - url: filename of the image to be posted
    """

    if text is not None:
        edit_image(filename, text, text_size=text_size, crop=crop)
    
    message = message[:270]
    print(message)
    print("Media: " + filename + "\n")


    if not check_duplicates(message):
        if test is False:
            # Check if the file is a video
            if filename[-3:] == "mp4":
                print("[{}] File is a video".format(module))
                # If it is a video, start a chunk upload
                videoTweet = VideoTweet(filename)
                videoTweet.upload_init()
                videoTweet.upload_append()
                videoTweet.upload_finalize()
                videoTweet.media_id

                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_token_secret)
                api = tweepy.API(auth)
                api.update_status(message, media_ids=[videoTweet.media_id])
                os.remove(filename)

            else:
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_token_secret)
                api = tweepy.API(auth)

                uploaded = api.media_upload(filename)
                api.update_status(message, media_ids=[uploaded.media_id])
                os.remove(filename)
    else:
        print("WARNING: Tweet NOT posted because it was a duplicate.")

def edit_image(filename, text, text_size=200, crop=False):
    """ Edit an image by adding a text (uses the Pillow module)
    
    Args:
        - filename: filename of the image to be modified
        - text: text to be added
        - text_size (optional): size of the text (default: 200)
        - crop (optional): if enabled removes black bars from a video thumbnail (16:9 over 4:3)
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


class VideoTweet(object):

  def __init__(self, file_name):
    '''
    Defines video tweet properties
    '''
    self.video_filename = file_name
    self.total_bytes = os.path.getsize(self.video_filename)
    self.media_id = None
    self.processing_info = None


  def upload_init(self):
    '''
    Initializes Upload
    '''
    print("[{}] (video) Initializing...".format(module))

    request_data = {
      'command': 'INIT',
      'media_type': 'video/mp4',
      'total_bytes': self.total_bytes,
      'media_category': 'tweet_video'
    }

    req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, auth=oauth)
    media_id = req.json()['media_id']

    self.media_id = media_id


  def upload_append(self):
    '''
    Uploads media in chunks and appends to chunks uploaded
    '''

    print("[{}] (video) Appending...".format(module))

    segment_id = 0
    bytes_sent = 0
    file = open(self.video_filename, 'rb')

    while bytes_sent < self.total_bytes:
      chunk = file.read(4*1024*1024)

      request_data = {
        'command': 'APPEND',
        'media_id': self.media_id,
        'segment_index': segment_id
      }

      files = {
        'media':chunk
      }

      req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, files=files, auth=oauth)

      if req.status_code < 200 or req.status_code > 299:
        print(req.status_code)
        print(req.text)
        sys.exit(0)

      segment_id = segment_id + 1
      bytes_sent = file.tell()

      print("[{}] (video) {}%".format(module, int((bytes_sent / self.total_bytes) * 100)))

    print("[{}] (video) Upload complete".format(module))


  def upload_finalize(self):
    '''
    Finalizes uploads and starts video processing
    '''
    print("[{}] (video) Finalizing...".format(module))

    request_data = {
      'command': 'FINALIZE',
      'media_id': self.media_id
    }

    req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, auth=oauth)

    self.processing_info = req.json().get('processing_info', None)
    self.check_status()


  def check_status(self):
    '''
    Checks video processing status
    '''
    if self.processing_info is None:
      return

    state = self.processing_info['state']

    print("[{}] (video) Media processing status is {}".format(module, state))

    if state == u'succeeded':
      print("[{}] (video) Posted successfully!".format(module))
      return

    if state == u'failed':
      sys.exit(0)

    check_after_secs = self.processing_info['check_after_secs']
    
    time.sleep(check_after_secs)

    request_params = {
      'command': 'STATUS',
      'media_id': self.media_id
    }

    req = requests.get(url=MEDIA_ENDPOINT_URL, params=request_params, auth=oauth)
    
    self.processing_info = req.json().get('processing_info', None)
    self.check_status()

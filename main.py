#!/usr/bin/env python3
import sys
import yaml
import os

from utils import convert_num, display_num, download_image
from tweet import twitter_post, twitter_post_image, twitter_repost, set_test_mode
from bithdays import check_birthdays
from instagram import instagram_data
from youtube import youtube_data
from spotify import spotify_data

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


def check_args():
    source = {"instagram": True, "youtube": True, "spotify": True, "birthday": True, "twitter": True}

    if len(sys.argv) > 1:
        for arg in sys.argv:
            if arg == "-no-tweet":
                print("-no-tweet parameter passed!\nTest mode enabled: the bot won't tweet anything")
                set_test_mode()
                
            if arg == "-no-instagram":
                print("-no-instagram parameter passed!")
                source["instagram"] = False
                
            if arg == "-no-spotify":
                print("-no-spotify parameter passed!")
                source["spotify"] = False
                
            if arg == "-no-youtube":
                print("-no-youtube parameter passed!")
                source["youtube"] = False
                
            if arg == "-no-birthday":
                print("-no-birthday parameter passed!")
                source["birthday"] = False
                
            if arg == "-no-twitter":
                print("-no-twitter parameter passed!")
                source["twitter"] = False
                
    print()
    return source


if __name__ == '__main__':

    source = check_args()
    
    group = load_group()

    if source["birthday"]:
        check_birthdays(group)
    
    if source["youtube"]: 
        group = youtube_data(group)
        
    if source["twitter"]:
        group["twitter"] = twitter_repost(group["twitter"])
    
    if source["instagram"]:
        group = instagram_data(group)
    
    if source["spotify"]:
        group = spotify_data(group)

    write_group(group)

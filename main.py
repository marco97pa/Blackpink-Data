#!/usr/bin/env python3
import sys
import yaml
import os

from utils import convert_num, display_num, download_image
from tweet import twitter_post, twitter_post_image, twitter_repost, set_test_mode
from bithdays import check_birthdays
from instagram import instagram_data
from youtube import youtube_data


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
    if len(sys.argv) > 1:
        if sys.argv[1] == "-no-tweet":
            print("-no-tweet parameter passed!\nTest mode enabled: the bot won't tweet anything\n")
            set_test_mode()


if __name__ == '__main__':

    check_args()
    
    group = load_group()

    check_birthdays(group)

    group = youtube_data(group)

    group["twitter"] = twitter_repost(group["twitter"])

    group = instagram_data(group)

    

    write_group(group)

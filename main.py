#!/usr/bin/env python3
import sys
import yaml
import os

from utils import convert_num, display_num, download_image
from tweet import twitter_post, twitter_post_image, twitter_repost, set_test_mode
from birthdays import check_birthdays
# from instagram import instagram_data
from youtube import youtube_data
from spotify import spotify_data
from billboard_charts import billboard_data
from radio import radio_data

def load_group():
    """Reads the data.yaml YAML file

    Data about a group is stored inside the data.yaml file in the same directory as the script

    Returns:
      A dictionary that contains all the informations about the group
    """

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
    """Writes the data.yaml YAML file

    Data about a group is stored inside the data.yaml file in the same directory as the script

    Args:
      group: dictionary that contains all the informations about the group
    """

    print("Writing data to YAML file...")
    with open('data.yaml', 'w', encoding="utf-8") as file:
        yaml.dump(group, file, sort_keys=False, allow_unicode=True)


def check_args():
    """Checks the arguments passed by the command line
    
    By passing one or more parameters, you can disable a single module source.

    Actual parameters allowed are:

    * `-no-instagram`: disables Instagram source  
    * `-no-youtube`: disables YouTube source  
    * `-no-spotify`: disables Spotify source  
    * `-no-birthday`: disables birthdays events source  
    * `-no-twitter`: disables Twitter source (used for reposting)  

    Remember that `-no-twitter` is different than `-no-tweet`:  
    
    `-no-tweet` actually prevents the bot from tweeting any update from the enabled sources. The output will still be visible on the console. This is really useful for **testing**.
    
    Returns:
      A dictionary that contains all the sources and their state (enabled or disabled, True or False)
    """

    source = {"instagram": True, "radio": True, "youtube": True, "spotify": True, "birthday": True, "twitter": True, "billboard": True}
    write = True

    if len(sys.argv) > 1:
        for arg in sys.argv:
            if arg == "-no-tweet":
                print("-no-tweet parameter passed!\nTest mode enabled: the bot won't tweet anything")
                set_test_mode()
                
            if arg == "-no-instagram":
                print("-no-instagram parameter passed!")
                source["instagram"] = False
            
            if arg == "-no-radio":
                print("-no-radio parameter passed!")
                source["radio"] = False
                
            if arg == "-no-spotify":
                print("-no-spotify parameter passed!")
                source["spotify"] = False
                
            if arg == "-no-youtube":
                print("-no-youtube parameter passed!")
                source["youtube"] = False
                
            if arg == "-no-birthday":
                print("-no-birthday parameter passed!")
                source["birthday"] = False

            if arg == "-no-billboard":
                print("-no-billboard parameter passed!")
                source["billboard"] = False
                
            if arg == "-no-twitter":
                print("-no-twitter parameter passed!")
                source["twitter"] = False
            
            if arg == "-no-write":
                print("-no-write parameter passed!")
                write = False

                
    print()
    return source, write


if __name__ == '__main__':

    source, write = check_args()
    
    group = load_group()

    if source["birthday"]:
        group = check_birthdays(group)
    
    if source["youtube"]: 
        group = youtube_data(group)
        
    if source["twitter"]:
        group = twitter_repost(group)
    
    if source["instagram"]:
        # group = instagram_data(group)
        print() 
    
    if source["spotify"]:
        group = spotify_data(group)

    if source["billboard"]:
        group = billboard_data(group)
    
    if source["radio"]:
        radio_data()

    if write:
        write_group(group)

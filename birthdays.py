#!/usr/bin/env python3
import datetime
from utils import download_image
from tweet import twitter_post_image, twitter_post

def check_birthdays(group):
    now = datetime.datetime.today()
    print("Today is {}".format(now.date()))
    
    print("Checking birthdays...")
    for member in group["members"]:
        birthday = datetime.datetime.strptime(member["birthday"], '%d/%m/%Y')
        difference = round((now - birthday).days / 365.25)
        birthday = birthday.replace(year=now.year)
        if birthday.date() == now.date():
            if member["years"] != difference:
                member["years"] = difference
                twitter_post_image(
                    "Today is #{}'s birthday! She did {} years\n#{}bday #blackpink @BLACKPINK".format(member["name"].upper(), difference, member["name"].lower()),
                    download_image(member["instagram"]["image"]),
                    str(difference)
                    )
    print()
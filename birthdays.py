#!/usr/bin/env python3
import datetime
from utils import download_image
from tweet import twitter_post_image, twitter_post

module = "Birthdays"

def check_birthdays(group):
    """Checks if today is the birthday of a member of the group

    It tweets if it is the birthday of someone

    Args:
      group: a dictionary with all the details of the group

    Returns:
      an dictionary containing all the updated data of the group
    """
    print("::group::" + module)

    now = datetime.datetime.today()
    print("[{}] Today is {}".format(module, now.date()))
    
    print("[{}] Checking...".format(module))
    for member in group["members"]:
        birthday = datetime.datetime.strptime(member["birthday"], '%d/%m/%Y')
        difference = round((now - birthday).days / 365.25)
        birthday = birthday.replace(year=now.year)
        if birthday.date() == now.date():
            print("[{}] ({}) Birthday: {} years!".format(module, member["name"], difference))
            if member["years"] != difference:
                member["years"] = difference
                twitter_post_image(
                    "Today is #{}'s birthday! She did {} years\n{}".format(member["name"].upper(), difference, member["hashtags"]),
                    download_image(member["instagram"]["image"]),
                    str(difference)
                    )
    print()
    print("::endgroup::")
    return group

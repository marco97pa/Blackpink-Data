#!/usr/bin/env python3
import billboard
from datetime import date
from tweet import twitter_post

hashtags= "\n@BLACKPINK #blinks #music #kpop"
module = "Billboard"

def billboard_data(group):
	"""Gets Billboard charts of a group

    It starts all the tasks needed to get latest data and eventually tweet updates
	Data is updated once a day

    Args:
      - group: dictionary that contains all the data about the group

    Returns:
      the same group dictionary with updated data
    """
	
	print("[{}] Starting...".format(module))

	report = ""

	# If the check didn't run today, start it
	if "billboard_check" not in group or group["billboard_check"] != date.today().strftime("%d-%m-%Y"):

		chart = billboard.ChartData('hot-100')
		print("[{}] Fetched the Hot 100 chart".format(module))
		report += get_artist_rank(group, chart)

		for artist in group["members"]:
			report += get_artist_rank(artist, chart)

		group["billboard_check"] = date.today().strftime("%d-%m-%Y")

		if len(report) > 0:
			report = "Today on #Billboard #Hot100:\n" + report + hashtags
			twitter_post(report)
		else:
			print("[{}] No songs found for the provided artist(s)".format(module))

	else:
		print("[{}] Check already run today, skipping.".format(module))
		
	return group

def get_artist_rank(artist, chart):
	"""Gets the Billboard Hot 100 chart and tries to find an artist

    Args:
      - artist: the artist to look for

    Returns:
      a string containing the list of songs found in the chart (it can be empty)
    """
	report = ""

	for song in chart:
		if artist["name"].lower() in song.artist.lower():
			report += "#{} {} by {}\n".format(song.rank, song.title, song.artist)
	
	return report

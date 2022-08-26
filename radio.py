#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from tweet import twitter_post

module = "Radio"

def radio_data():
	"""Gets appearences of BLACKPINK on italian radios
    """
    
    print("[{}] Starting...".format(module))
    URL = "https://radioairplay.fm/artista/175127/blackpink/airplay/pink-venom/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find("table", class_="table-striped")
    rows = table.find("tbody").find_all("tr")
    radio = []
    for row in rows:
        radio.append(row.text.strip().replace('\n', ' on ').replace(' (Italia)',' (Italy)'))


    f = open("last_radio.txt", "r")
    for appearence in radio:
    if f.readline() == appearence:
        break
    else:
        twitter_post("#PinkVenom aired on radio at " + appearence)
    f.close()

    f = open("last_radio.txt", "w")
    f.write(radio[0])
    f.close()
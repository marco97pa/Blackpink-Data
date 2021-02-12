#!/usr/bin/env python3
import requests

def convert_num(mode, num):
    num = int(num)

    if mode == "100K":
        num = int(num / 100000)
    elif mode == "M":
        num = int(num / 1000000)
    elif mode == "10M":
        num = int(num / 10000000)
    elif mode == "100M":
        num = int(num / 100000000)
    elif mode == "B":
        num = int(num / 1000000000)
    return num

def display_num(num, short=False, decimal=False):
    num = int(num)
    digits = len(str(abs(num)))

    if digits <= 6:
        num = int(num / 1000)
        if not short:
            out = "{} thousand".format(num)
        else:
            out = "{}.000".format(num)
    elif digits > 6 and digits <= 9:
        if not decimal:
            num = int(num / 1000000)
            if not short:
                out = "{} million".format(num)
            else:
                out = "{} Mln".format(num)
        else:
            num = num / 1000000
            if not short:
                out = "{:0.1f} million".format(num)
            else:
                out = "{:0.1f} Mln".format(num)
    elif digits > 9:
        num = num / 1000000000
        if not short:
            out = "{:0.1f} billion".format(num)
        else:
            out = "{:0.1f} Bln".format(num)
    return out

def download_image(url):
    filename = "download.jpg"
    response = requests.get(url)

    file = open(filename, "wb")
    file.write(response.content)
    file.close()

    return filename
#!/usr/bin/env python3
import requests

def convert_num(mode, num):
    """Converts a number in any given number scale

    Example:
    `convert_num("100K", 600000) returns 6`

    Args:
      - mode: (string) the scale for the conversion ("100K", "M", "10M", "100M", "B")
      - num: the number to be converted

    Returns:
      the converted number
    """

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
    """Converts a number in a readable format

    Args:
      - num: the number to be converted
      - short (optional): flag to get a long or short literal ("Mln" vs "million")
      - decimal (optional): flag to print also the first decimal digit (19.1 vs 19)

    Returns:
      a string with a number in a readable format
    """

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
    """Downloads an image, given an url

    The image is saved in the download.jpg file

    Args:
      url: source from where download the image
    """

    filename = "download.jpg"
    response = requests.get(url)

    file = open(filename, "wb")
    file.write(response.content)
    file.close()

    return filename

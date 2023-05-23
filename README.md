
[![Action][action-shield]][action-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Twitter][twitter-shield]][twitter-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/marco97pa/Blackpink-Data">
    <img src="https://raw.githubusercontent.com/marco97pa/Blackpink-Data/master/icon.jpg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">BLACKPINK Data</h3>

  <p align="center">
    A Twitter bot that tweets the latest updates, pictures, stats and news about the korean girl group BLACKPINK.
    <br />
    <a href="https://twitter.com/data_blackpink"><strong>Follow the Bot on Twitter</strong></a>
    <br />
    <br />
    <a href="https://blackpink-data.rtfd.io">Explore the docs »</a>
    ·
    <a href="https://github.com/marco97pa/Blackpink-Data/issues">Report Bug</a>
    ·
    <a href="https://github.com/marco97pa/Blackpink-Data/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Screen Shot](https://pbs.twimg.com/profile_banners/1320467294317928448/1613083325/1500x500)](https://twitter.com/data_blackpink)

A Twitter bot powered by AI that tweets the latest updates, pictures, stats and news about the korean girl group [BLACKPINK](https://en.wikipedia.org/wiki/Blackpink).

The bot runs 24/7 on the **Cloud** thanks to **GitHub Actions**.

It uses a lot of sources to fetch the latest update about the group: Spotify, YouTube, Instagram, Twitter and more. Based on the data scraped from the web and the data already known (stored in a **YAML** file), the bot makes decisions and tweets updates. 

The project is really modular and by editing the YAML file you can easily fork this repo and make a bot of another group or artist, with zero to minimal code changes.

#### Development suspended
Thanks to the latest updates of Twitter API pricing, the development and execution is suspended.  
 See https://github.com/marco97pa/Blackpink-Data/issues/31 for further details


### Built With

* Python 3
* [Tweepy](https://pypi.org/project/tweepy/)
* [pillow](https://pypi.org/project/Pillow/)
* [instagrapi](https://github.com/adw0rd/instagrapi)
* [python-youtube](https://pypi.org/project/python-youtube/)
* [spotipy](https://github.com/plamere/spotipy)
* [billboard.py](https://github.com/guoguo12/billboard-charts)




<!-- GETTING STARTED -->
## Getting Started

To get a copy up and running follow these simple steps.

### Prerequisites

Make sure you have installed:
* Python **3.8**
* pip  

_While not necessary, this project supports **pyenv**:  
in that case all the python command will be 'python' instead of 'python3' and 'pip' instead of 'pip3'_

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/marco97pa/Blackpink-Data.git
   ```
2. Install requirements
   ```sh
   pip3 install -r requirements.txt
   ```
3. Add the API KEYs
   ```sh
    export TWITTER_CONSUMER_KEY='xxxx'
    export TWITTER_CONSUMER_SECRET='xxxx'
    export TWITTER_ACCESS_KEY='xxxx'
    export TWITTER_ACCESS_SECRET='xxxx'

    export YOUTUBE_API_KEY='xxxx'

    export INSTAGRAM_ACCOUNT_USERNAME='xxxxxx'
    export INSTAGRAM_ACCOUNT_PASSWORD='xxxxxx'

    export SPOTIPY_CLIENT_ID='xxxx'
    export SPOTIPY_CLIENT_SECRET='xxxx'
   ```

For detailed instructions see the [related page of the Documentation](https://blackpink-data.readthedocs.io/en/latest/#how-to-build)


<!-- USAGE EXAMPLES -->
## Usage

You can launch the bot by running:   
`python3 main.py`  

_For more details, please refer to the [Run section of the Documentation](https://blackpink-data.readthedocs.io/en/latest/#run)_



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/marco97pa/Blackpink-Data/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

If you are adding a new **module**, please check the documentation and follow the style of other modules.


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Marco Fantauzzo - [@data_blackpink](https://twitter.com/@data_blackpink) - marco97pa@live.it

Project Link: [https://github.com/marco97pa/Blackpink-Data](https://github.com/marco97pa/Blackpink-Data)






<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[action-shield]: https://github.com/marco97pa/Blackpink-Data/actions/workflows/main.yml/badge.svg
[action-url]: https://github.com/marco97pa/Blackpink-Data/actions/workflows/main.yml
[action2-shield]: https://github.com/marco97pa/Blackpink-Data/actions/workflows/instagram.yml/badge.svg
[action2-url]: https://github.com/marco97pa/Blackpink-Data/actions/workflows/instagram.yml
[forks-shield]: https://img.shields.io/github/forks/marco97pa/Blackpink-Data?style=for-the-badge
[forks-url]: https://github.com/marco97pa/Blackpink-Data/network/members
[stars-shield]: https://img.shields.io/github/stars/marco97pa/Blackpink-Data?color=f0a500&style=for-the-badge
[stars-url]: https://github.com/marco97pa/Blackpink-Data/stargazers
[issues-shield]: https://img.shields.io/github/issues/marco97pa/Blackpink-Data?style=for-the-badge
[issues-url]: https://github.com/marco97pa/Blackpink-Data/issues
[twitter-shield]: https://img.shields.io/twitter/follow/data_blackpink?label=%40data_blackpink&style=social
[twitter-url]: https://twitter.com/data_blackpink

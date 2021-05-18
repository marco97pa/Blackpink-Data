.. Blackpink Data documentation master file, created by
   sphinx-quickstart on Fri Feb 19 23:55:38 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Blackpink Data's documentation!
==========================================

.. toctree::
   :maxdepth: 4
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

How to Build
===================

Set up your machine
--------------------

Python
~~~~~~~~~~~~~~~

Make sure you have installed:

-  Python **3.8**
-  pip

Please note that the ``spotify.py`` module, which is based on the
library `spotipy`_, seems to not work well with Windows, so I suggest to
use Linux or WSL on Windows. All the following commands assume that you
are in a Linux-like environment.

Clone the repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run: ``git clone https://github.com/marco97pa/Blackpink-Data.git``

For more info see `this guide`_

Then ``cd`` to the new directory

Install dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run ``pip3 install -r requirements.txt`` to install all `the required
libraries`_

Set API keys as environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The project is componed by different modules such as ``instagram.py``,
``youtube.py`` and more. Each module is used to get data from a
different source. To get this data you need the corresponding API keys.

Twitter API keys
~~~~~~~~~~~~~~~~

| Go to `the Twitter Developers page`_, log in, go to Dashboard and
  create a new app with read and write permissions.
| Then copy the generated keys and set them as environment variables, by
  running these lines (change them with your actual key values):

``export TWITTER_CONSUMER_KEY='xxxx'``
``export TWITTER_CONSUMER_SECRET='xxxx'``
``export TWITTER_ACCESS_KEY='xxxx'``
``export TWITTER_ACCESS_SECRET='xxxx'``

YouTube API key
~~~~~~~~~~~~~~~

| Go to `Google Developers`_ and follow their istructions on how to get
  an API key for YouTube
| Then copy the generated key and set it as environment variable, by
  running this line (change with your actual key value):

``export YOUTUBE_API_KEY='xxxx'``

Spotify API key
~~~~~~~~~~~~~~~

Go to `Spotify Developer Dashboard`_, create a new app and get the API
keys. Then set them as environment variables, by running these lines:

``export SPOTIPY_CLIENT_ID='xxxx'``
``export SPOTIPY_CLIENT_SECRET='xxxx'``

Instagram SESSION_ID cookie
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can get your Instagram **Session ID** if you are logged in to
Instagram using any browser. This guide uses Google Chrome.

1. Open Google Chrome
2. Go to `Instagram`_ and log in to your account
3. Right click somewhere on the webpage and select **Inspect** on the
   dropdown menu to open Chrome Developer tools
4. Click the **Application** tab under the Chrome Developer Tools window
5. Under the **storage** header on the left-hand menu, expand
   **Cookies** and click on the entry for ``https://www.instagram.com/``
6. Find the row with the **Name** equal to ``sessionid``: this is your
   **Session ID**

| Then set it as environment variable by running:
| ``export INSTAGRAM_SESSION_ID='xxxxx'``

Fork
--------------------
By editing the data.yaml file you can make the script work with a different artist group.

For example, you could make a BTS Data Bot by editing the provided **sample_data.yaml** file and saving it as data.yaml

Edit the data.yaml accordingly with all the data you know. Leave empty fields or write fake data if you don't know some details: they will be overwritten with the real ones at the first launch of the script.

With minimal or no code edits, the script could work even for single artists and not only groups.

Run
----

First run
~~~~~~~~~~~~~~~

| Assumed that you have a valid ``data.yaml`` file in the same directory
  as the script, run:
| ``python3 main.py -no-tweet``

For the first run it is important that you use the ``-no-tweet`` option
to prevent an overload of tweets in your timeline. You should also check
that everything is fine by looking at the command line output and the
``data.yaml`` file

Standard run
~~~~~~~~~~~~~~~

| From the next time, you can just run: ``python3 main.py``
| It will tweet eventually changes on the dataset.

Parameters
~~~~~~~~~~~~~~~

By passing one or more parameters, you can disable a single module
source. Actual parameters allowed are:

-  ``-no-instagram``: disables Instagram source
-  ``-no-youtube``: disables YouTube source
-  ``-no-spotify``: disables Spotify source
-  ``-no-birthday``: disables birthdays events source
-  ``-no-twitter``: disables Twitter source (used for reposting)

| Remember that ``-no-twitter`` is different from ``-no-tweet``:
| ``-no-tweet`` actually prevents the bot from tweeting any update from
  the enabled sources. The output will still be visible on the console.
  This is really useful for **testing**.

Schedule the bot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want the bot to run 24/7, you should set the script to run (for
example) every 5 minutes to check for updates. Look at `How to schedule
tasks on Linux using crontab`_ to get an idea on how to do it.

.. _How to schedule tasks on Linux using crontab: https://www.howtogeek.com/101288/how-to-schedule-tasks-on-linux-an-introduction-to-crontab-files/

.. _spotipy: https://github.com/plamere/spotipy
.. _this guide: https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository
.. _the required libraries: https://github.com/marco97pa/Blackpink-Data/blob/master/requirements.txt
.. _the Twitter Developers page: https://developer.twitter.com/en/products/twitter-api
.. _Google Developers: https://developers.google.com/youtube/v3/getting-started
.. _Spotify Developer Dashboard: https://developer.spotify.com/dashboard/
.. _Instagram: https://www.instagram.com/

Modules
==================

Main script
-----------

.. automodule:: main
   :members:

Tweet
------------

.. automodule:: tweet
   :members:

Utils
------------

.. automodule:: utils
   :members:

Birthdays
-----------------

.. automodule:: birthdays
   :members:

YouTube
-----------------

.. automodule:: youtube
   :members:

Instagram
-----------------
.. automodule:: instagram
   :members:

Spotify
-----------------
.. automodule:: spotify
   :members:

Billboard Charts
------------------------
.. automodule:: billboard_charts
   :members:
   

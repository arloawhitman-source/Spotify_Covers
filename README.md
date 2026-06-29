# Spotify Album Art Matrix Display

I made a cool thing that shows the album art of the music you are listening to on Spotify. It is a 64×64 RGB LED matrix display that is powered by the Adafruit Matrix Portal S3. This thing connects to your WiFi network. Uses the Spotify Web API to get the album art of the song that is currently playing. And it does this in real time.

## How It Works

When you turn it on the Matrix Portal S3 connects to your WiFi. Then it talks to Spotify using a special token that it saved earlier. Every 5 seconds it checks with Spotify to see what song is playing now. When the song changes it gets the album art. Shows it on the 64×64 matrix. It even spins the album art like a record while the music is playing. When nothing is playing it shows an animation.

## Hardware Required

* Adafruit Matrix Portal S3

* 64×64 RGB LED Matrix. This is the thing that shows the pictures

* USB-C power supply. You need this to make it work it needs 5V 3A or more

## Software & Libraries

This project uses CircuitPython. You need to copy some libraries to the /lib folder on your board. These are:

* adafruit_matrixportal

* adafruit_requests

* adafruit_display_text

* adafruit_display_shapes

* adafruit_imageload

## Setup

### 1. Spotify Developer App

You need to go to the Spotify Developer Dashboard and make an app. Then you set the redirect URI to http://127.0.0.1:8888/callback. You should write down your Client ID and Client Secret.

### 2. Get a Refresh Token

You need to do this on your computer. You run some code to authorize your account and get a refresh token. Here is the code:

```python

import spotipy

from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(

client_id="YOUR_CLIENT_ID"

client_secret="YOUR_CLIENT_SECRET"

redirect_uri="http://127.0.0.1:8888/callback"

scope="user-read-playing"

))

print(sp.current_user())

```

After you log in you get a.cache file. You need to open it and copy the refresh_token value.

### 3. Configure code.py

You need to fill in your credentials at the top of code.py:

```python

WIFI_SSID = "your_wifi_name"

WIFI_PASSWORD = "

SPOTIFY_CLIENT_ID = "your_client_id"

SPOTIFY_CLIENT_SECRET = "your_client_secret"

SPOTIFY_REFRESH_TOKEN = "your_refresh_token"

```

### 4. Deploy

You copy code.py to the root of your Matrix Portal S3. It will start working when you turn it on.

## Configuration

Here are some variables you can change:

* POLL_SECONDS. This is how often it checks Spotify for a song it is 5 seconds by default

* FPS. This is how many times it updates the display per second it is 20 by default

* RPM. This is how fast the album art spins it is 20.0 by default

* BRIGHTNESS. This is how bright the display is, it is 0.6, by default

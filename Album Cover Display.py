import gc
import time
import ssl
import wifi
import socketpool
import adafruit_requests
import displayio
from adafruit_matrixportal.matrix import Matrix
from io import BytesIO
import adafruit_imageload
import neopixel
import board

#I Will Change All "MY_" to the actual data once I physically have the Pico 2W

WIFI_SSID = "MY_WIFI_SSID"
WIFI_PASSWORD = "MY_WIFI_PASSWORD"

SPOTIFY_CLIENT_ID = "MY_CLIENT_ID"
SPOTIFY_CLIENT_SECRET = "MY_CLIENT_SECRET"

SPOTIFY_REFRESH_TOKEN = "MY_REFRESH_TOKEN"

MATRIX_WIDTH = 16
MATRIX_HEIGHT = 16
NUM_PIXELS = MATRIX_WIDTH * MATRIX_HEIGHT
DATA_PIN = board.GP0
POLL_SECONDS = 5
BRIGHTNESS = 0.6

TOKEN_URL = "https://accounts.spotify.com/api/token"
CURRENTLY_PLAYING_URL = "https://api.spotify.com/v1/me/player/currently-playing"

# Wifi Connection
print("Connecting to WiFi...")
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
print(f"Connected: {wifi.radio.ipv4_address}")

pool = socketpool.SocketPool(wifi.radio)
ssl_ctx = ssl.create_default_context()
requests = adafruit_requests.Session(pool, ssl_ctx)

# Neo Pixel
pixels = neopixel.NeoPixel(
    DATA_PIN,
    NUM_PIXELS,
    brightness=BRIGHTNESS,
    auto_write=False,
    pixel_order=neopixel.GRB
)

# Spotify Token
access_token = None
token_expiry = 0

def refresh_access_token():
    global access_token, token_expiry
    import binascii
    credentials = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    encoded = binascii.b2a_base64(credentials.encode()).decode().strip()
    response = requests.post(
        TOKEN_URL,
        headers={
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data=f"grant_type=refresh_token&refresh_token={SPOTIFY_REFRESH_TOKEN}",
    )
    data = response.json()
    response.close()
    access_token = data["access_token"]
    token_expiry = time.monotonic() + int(data.get("expires_in", 3600)) - 60
    print("Token refreshed.")


def get_valid_token():
    if access_token is None or time.monotonic() >= token_expiry:
        refresh_access_token()
    return access_token


# Spotify API
def get_currently_playing():
    try:
        token = get_valid_token()
        response = requests.get(
            CURRENTLY_PLAYING_URL,
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code == 204:
            response.close()
            return None
        if response.status_code == 401:
            response.close()
            refresh_access_token()
            return get_currently_playing()
        if response.status_code != 200:
            response.close()
            return None
        data = response.json()
        response.close()
        return data
    except Exception as e:
        print(f"Spotify error: {e}")
        return None


def extract_art_url(playback):
    if not playback:
        return None, False
    item = playback.get("item")
    if not item:
        return None, False
    item_type = item.get("type")
    if item_type == "track":
        images = item.get("album", {}).get("images", [])
    else:
        images = item.get("images", [])
    if not images:
        return None, False
    image = min(images, key=lambda img: img.get("width") or 9999)
    return image["url"], bool(playback.get("is_playing"))


# Display
def show_idle():
    """Turn all pixels off when nothing is playing."""
    pixels.fill((0, 0, 0))
    pixels.show()


def xy_to_index(x, y):
    """Convert x,y coordinate to pixel index accounting for serpentine wiring."""
    if y % 2 == 0:
        return y * MATRIX_WIDTH + x
    else:
        return y * MATRIX_WIDTH + (MATRIX_WIDTH - 1 - x)


def download_and_show_art(url):
    """Download album art, scale it to 16x16 and display on the matrix."""
    print(f"Downloading art: {url}")
    try:
        response = requests.get(url)
        data = response.content
        response.close()
        gc.collect()

        bitmap, palette = adafruit_imageload.load(
            BytesIO(data),
            bitmap=displayio.Bitmap,
            palette=displayio.Palette,
        )
        gc.collect()

        # Scale image down to 16x16 by sampling evenly
        src_w = bitmap.width
        src_h = bitmap.height

        for y in range(MATRIX_HEIGHT):
            for x in range(MATRIX_WIDTH):
                src_x = int(x * src_w / MATRIX_WIDTH)
                src_y = int(y * src_h / MATRIX_HEIGHT)
                color_index = bitmap[src_x, src_y]
                color = palette[color_index]
                r = (color >> 16) & 0xFF
                g = (color >> 8) & 0xFF
                b = color & 0xFF
                pixels[xy_to_index(x, y)] = (r, g, b)

        pixels.show()
        gc.collect()
        return True
    except Exception as e:
        print(f"Art download failed: {e}")
        return False


# Display Loop
current_art_url = None
last_poll = -POLL_SECONDS

show_idle()

print("Starting main loop...")
while True:
    now = time.monotonic()

    if now - last_poll >= POLL_SECONDS:
        last_poll = now
        playback = get_currently_playing()
        art_url, is_playing = extract_art_url(playback)

        if art_url and art_url != current_art_url:
            current_art_url = art_url
            download_and_show_art(art_url)
        elif not art_url:
            current_art_url = None
            show_idle()

        gc.collect()

    time.sleep(1)

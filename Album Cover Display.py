import gc
import time
import math
import ssl
import wifi
import socketpool
import adafruit_requests
import board
import displayio
import terminalio
from adafruit_matrixportal.matrix import Matrix
from adafruit_display_shapes.circle import Circle
from adafruit_display_text import label
from io import BytesIO

WIFI_SSID = "MY_WIFI_SSID"
WIFI_PASSWORD = "My_WIFI_PASSWORD"


SPOTIFY_CLIENT_ID = "MY_CLIENT_ID"
SPOTIFY_CLIENT_SECRET = "MY_CLIENT_SECRET"


SPOTIFY_REFRESH_TOKEN = "MY_REFRESH_TOKEN"

MATRIX_WIDTH = 64
MATRIX_HEIGHT = 64
POLL_SECONDS = 5
FPS = 20
RPM = 20.0
BRIGHTNESS = 0.6

TOKEN_URL = "https://accounts.spotify.com/api/token"
CURRENTLY_PLAYING_URL = "https://api.spotify.com/v1/me/player/currently-playing"


print("Connecting to WiFi...")
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
print(f"Connected: {wifi.radio.ipv4_address}")

pool = socketpool.SocketPool(wifi.radio)
ssl_ctx = ssl.create_default_context()
requests = adafruit_requests.Session(pool, ssl_ctx)


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


matrix = Matrix(width=MATRIX_WIDTH, height=MATRIX_HEIGHT, bit_depth=4, serpentine=False)
display = matrix.display
display.brightness = BRIGHTNESS

main_group = displayio.Group()
display.root_group = main_group


def show_idle():
    """Show a simple dark circle when nothing is playing."""
    main_group.remove(main_group[0]) if len(main_group) > 0 else None
    bitmap = displayio.Bitmap(MATRIX_WIDTH, MATRIX_HEIGHT, 2)
    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = 0x333333
    cx = MATRIX_WIDTH // 2
    cy = MATRIX_HEIGHT // 2
    r = MATRIX_WIDTH // 2 - 2
    for angle_deg in range(360):
        rad = math.radians(angle_deg)
        x = int(cx + r * math.cos(rad))
        y = int(cy + r * math.sin(rad))
        if 0 <= x < MATRIX_WIDTH and 0 <= y < MATRIX_HEIGHT:
            bitmap[x, y] = 1
    tile = displayio.TileGrid(bitmap, pixel_shader=palette)
    group = displayio.Group()
    group.append(tile)
    while len(main_group) > 0:
        main_group.pop()
    main_group.append(group)


def download_and_show_art(url, angle_deg):
    """Download album art and display it rotated as a spinning record."""
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

        tile = displayio.TileGrid(bitmap, pixel_shader=palette)
        group = displayio.Group(scale=1)
        group.append(tile)

        while len(main_group) > 0:
            main_group.pop()
        main_group.append(group)
        return bitmap, palette
    except Exception as e:
        print(f"Art download failed: {e}")
        return None, None


def show_art(bitmap, palette):
    tile = displayio.TileGrid(bitmap, pixel_shader=palette)
    group = displayio.Group()
    group.append(tile)
    while len(main_group) > 0:
        main_group.pop()
    main_group.append(group)


import adafruit_imageload

current_art_url = None
current_bitmap = None
current_palette = None
is_playing = False
angle = 0.0
last_poll = -POLL_SECONDS  # Poll immediately on startup
last_frame = time.monotonic()

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
            current_bitmap, current_palette = download_and_show_art(art_url, angle)
        elif not art_url:
            current_art_url = None
            current_bitmap = None
            current_palette = None
            show_idle()

        gc.collect()

    # Update rotation angle if playing
    delta = time.monotonic() - last_frame
    last_frame = time.monotonic()

    if is_playing and current_bitmap is not None:
        angle = (angle + 360.0 * (RPM / 60.0) * delta) % 360.0

        show_art(current_bitmap, current_palette)

    time.sleep(1.0 / FPS)

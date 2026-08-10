# Spotify Album Art Matrix Display

I made a matrix that shows the album art of the music you are listening to on Spotify. It is a 16x16 RGB LED matrix display that is powered by the Raspberry Pi Pico 2 W. This connects to your WiFi network,and uses the Spotify Web API to get the album art of the song that is currently playing. The RGB matrix display is custom made and all the needed files are attached.

## How It Works

When turned on the Pico connects to your WiFi. Then it talks to Spotify using a special token that it saved earlier. Every 5 seconds it checks with Spotify to see what song is playing now. When the song changes it gets the album art and shows it on the 16x16 matrix. It even spins the album art like a record while the music is playing. 

## Hardware Required

* 256x WS2815 LEDs (60LEDs/m strips)
* Polypropylene Sheet 0.5mm (clear)
* 5mm-2mm aluminum base plate
* Level shifter 74HCT125 convert 3.3V logic up to 5V
* 26AWG Wire (Black, Red, Green)
* Heatsink (300x140x20)
* F0.5a Fuses
* 16 AWG Wire (Red, Black)
* LM2596 Voltage Regulator
* Raspberry pi pico 2w
* Power Supply Unit 12v/8.5A
* c1 100nF
* 10A ATC Blade Fuse
* 16 AWG Terminal Connector
* 16 AWG ATC Fuse Holder
* 3.5ft or longer two by four of wood
* M2x10 screw (x9)
* M3x6 screw (x4)

## Bill of Materials

| Component | Qty | Price | Link |
|---|---|---|---|
| 256x WS2815 LEDs (60 LEDs/m strips) | 1 | $41.99 | [Buy](https://www.btf-lighting.com/products/ws2815-rgb-addressable-led-strip-dc12v?variant=47607344726242) |
| Polypropylene Sheet 0.5mm (132.4mm × 14.5mm) | 32 | $19.70 | [Buy](https://www.ebay.com/itm/406446159505) |
| 5mm Aluminum Base Plate | 1 | Depends On Thickness | Depends On Thickness And Location |
| Level Shifter 74HCT125 (3.3V → 5V) | 1 | $0.92 | [Buy](https://www.digikey.com/en/products/detail/texas-instruments/SN74HCT125N/13483078) |
| 26 AWG Wire (Black, Red, Green) | 3 | $13.95 | [Buy](https://www.adafruit.com/product/2513) |
| Heatsink (300×140×20mm) | 1 | $28.09 | [Buy](https://www.walmart.com/ip/Aluminum-Large-Heatsink-300x140x20mm-Heat-Sink-Cooling-Radiators-for-Computer-LED/19318660156) |
| F0.5A Fuse | 16 | $14.77 | [Buy](https://www.ebay.com/itm/358421553078) |
| Wire Shrink Wrap Kit | 1 | $9.95 | [Buy](https://www.adafruit.com/product/4559) |
| 16 AWG Wire (Red, Black) | 1 | $12.18 | [Buy](https://www.remingtonindustries.com/hook-up-wire/hook-up-wire-16-awg-stranded-solid-10-colors-7-sizes-available/?sku=16UL1007SLDBLA25) |
| LM2596 Voltage Regulator | 1 | $0.71 | [Buy](https://www.pcb-hero.com/products/141892) |
| Raspberry Pi Pico 2W | 1 | $7.70 | [Buy](https://www.sparkfun.com/raspberry-pi-pico-2-w.html?src=raspberrypi) |
| Power Supply Unit (Mean Well LRS-100-12) | 1 | $16.50 | [Buy](https://www.walmart.com/ip/Mean-Well-LRS-100-12-Power-Supply-100W-12V/5585345774) |
| C1 100nF Capacitor | 1 | $1.06 | [Buy](https://www.digikey.com/en/products/detail/tdk/FK20C0G1H104JN000/2050105) |
| 10A Blade Fuse | 1 | $4.86 | [Buy](https://www.walmart.com/ip/Cooper-Bussman-ATC-10A-Blade-Fuses-5-Count/20971317) |
| 16 AWG Terminal Connector | 2 | $4.98 | [Buy](https://www.lowes.com/pd/Utilitech-22-16-Ring-Red-20-Count/5017987455) |
| 16 AWG Fuse Holder (Waterproof, ATC/ATO) | 1 | $9.99 | [Buy](https://www.lowes.com/pd/Unique-Bargains-Fuse-Holder-In-line-16AWG-Waterproof-Fuse-Holder-Black-for-ATC-ATO-Fuse/9307036) |

**Estimated Total: ~$187.35**

## How To Build

### Step 1
Print four of the attached 3d model, this will seperate each of the leds and have a place for a strip of the Polypropylene to act as a diffuser. Flip the prints over and drill 1.8mm hole through the provided gap in the back of the board in the following pattern. Once you have the 1.8mm pilot holes thread them with an M2 countersink bit. <img width="453" height="456" alt="image" src="https://github.com/user-attachments/assets/1e5e5834-5be2-438e-8ffe-2467ece1b5fc" /> 

### Step 2
Cut the polypropylene sheet into 132.4mm x 14.5mm strips, you will need a total of 32 strips. Then insert these into the prints. Next glue all four grids to make one large 16x16 grid.

### Step 3
Cut your aluminum sheet to 266.5mm x 266.5mm then drill 2.5mm holes in the same position as the holes in the printed boards. Then countersink the back of the plate to ensure it will lay flat when screwed together.

### Step 4
Cut your wood beam into strips at least 20mm tall 20mm wide and exactly 266.5mm long. These will act as a frame on the back side of the aluminum to protect the componenents and heat sink. Then 30mm from each end drill a 3.5 hole then drill a 2.5mm hole in the same position on the back of the aluminum, then in the aluminum and wood cut M3 threads into the holes you just made.

### Step 5
With a straight edge and a fine tip sharpie mark out the location of the led strips, the distance between each row of leds is 16.66mm. Then on the vertical side of the plate place down a stip of tape to insulate the edges of the lights.

### Step 6
Cut your LEDs into 16 strips of 16 LEDs each. Trim them to ensure they don't stick of the edge of the aluminum plate. Then stick them down following the guide you drew in the last step ensuring that each strip is 16.66mm away from the last, and the stips zig zag going down the board. This means that the data will flow to the right on one row and then to the left on the next (THIS IS VERY IMPORTANT).

### Step 7 
You are now going to daisy chain the data pins, this will be done with 0.14mm^2 wires or 26AWG. place these wire as close to the end as possible to ensure it doesn't get in the way of the printed grid. The data pins will be daisy chained as follows: BO -> BI, DO -> DI <img width="750" height="686" alt="image" src="https://github.com/user-attachments/assets/7171a431-fb05-4bc7-9e64-9958fe9dc473" />

### Step 8
Cut your heasink into a 140mm x 193mm rectangle. Drill 4mm holes in each corner of the heat sink, before marking these holes place the heatsink in the middle of the LED matrix and place the holes in the space between the rows of lights. Then drill 2.5mm holes for the heatsink in the Aluminum plate. Finally thread them with a M3 bit. <img width="742" height="696" alt="image" src="https://github.com/user-attachments/assets/68373852-ea23-4a08-9eab-b7f14f42e42a" />

### Step 9
The power to the lines are injected every row. Drill a 2.5mm hole for each row, this will allow us to run power to each row from behind the board. Solder 26AWG or 0.14mm^2 wires to each +12v and each GND pad (One for each row) Make sure these arent in the middle or on the very edge. Basically you want to avoid the heat sink and the frame that will be placed on the back.

### Step 10 
Solder a 0.5a fuse to each row on the +12v wire. This should be done on the back side of the board after it has passed through the aluminum via the 2.5mm holes. Next solder more 26AWG wire on the other side of each fuse and place heat shrink tube over each fuse.<img width="944" height="700" alt="image" src="https://github.com/user-attachments/assets/5e20e6da-6fcd-47db-8b72-0c1dc8326de0" />

### Step 11
Solder the +12v wires into four groups of four, do the same with the ground wires. Next with 16AWG or 1.5mm^2 stranded wire cut two pieces each about half the length of the board. On the first piece strip the end and in a position fairly close to the same end. On the other wire stip both ends and then twice more spliting the cable into three sections that are still covered. Solder one end of the second wire to the inner spot of the first wire. Finaly solder one group of four +12v ontothe end of the first wire, and one to each of the remain positions on the second wire. cover with heat shrink tubing. Repeat this with the same guage wire for ground.

### Step 12
Drill a 2.5mm hole near the start of the first line but at least 20mm from each side. Then an untrimmed data wire (26AWG), and a untrimmed ground wire (26AWG) through the hole to the LED. Solder these to the DI and gnd pad before the first LED.

### Step 13
Take the Level Shifter and solder pins 4-7 together as well as 8-13 connect pin 7 and 8 with 26AWG wire, also connect pin 1 to pin 4 using wire. Next solder the 100nF capacitor to pins 14 and 1. After, solder the data wire from the last step to pin 3 and the ground wire to pin 8. Solder a 26AWG wire to pin 2 and label it 1A, next solder a 26AWG wire to pin 14 and label it +5V, finally solder a 26AWG wire to pin 13 and label it GND. Put heat shrink wrap over the entire chip. <img width="1674" height="1186" alt="SCH_Main Schematic_1-P1_2026-07-12" src="https://github.com/user-attachments/assets/20d9ac44-c04e-4f52-8128-bda70e4c94a0" />

### Step 14
Still following the wiring diagram above solder the 1A wire from the last step to pin pin 20 on the raspberry pi pico and solder the GND wire from the last step to pin 38.

### Step 15
adjust the voltage regulator to 5v and solder the GND out to pin 38 of the Pico, then solder a a 26AWG wire to pin 39 of the pico, finally solder this wire, one connecting the VOUT out of the voltage regulator and the remaining wire from the Level shifter.

### Step 16
From your power supply solder the ATC Fuse holder and insert the 10A ATC fuse. Then connect the positive +12V from the powersupply and going through the fuse to the end of the unstripped wire from step 11 using 16AWG wire, also solder this to the +12V of the Voltage Regulator with 16AWG wire. Then do the same with the ground from the power supply and connect it to the wire from step 11, and the GND in on the Voltage regulator.

### Step 17
Mont the aluminum plate to the 3d printed grid using nine M2x10mm screws (If you are using 5mm aluminum) Then on the back use doublesided sticky tape to secure all electronic componenets. Mount the heat sink using M3x6 screws (If using 5mm aluminum) on the pre drilled holes. Finally mount the wood frame using M3x25 screws (If using 5mm aluminum).

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

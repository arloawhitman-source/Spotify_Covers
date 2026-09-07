# Total Time: 39.4h

## Initial Research - Jun 26, 2026, 2:22 PM - 1h

<img width="553" height="488" alt="image" src="https://github.com/user-attachments/assets/890de1ac-e780-4340-982e-453ff7ecb252" />

This first hour was spent determining just what materials I would need to do the job. First, I decided to look into RGB LED matrix panels and settled on the resolution I needed, 64 x 64 RGB matrix, as it appeared to me to be just about the right resolution to allow me to render album covers without making them look pixelated. After researching several beginner tutorials on RGB matrixes, I understood enough about their addressing (number of rows, data lines, refresh rate) to make the purchase of hardware. Since the focus of this project was always going to be the hardware part (wiring, actual matrix and enclosure), not on writing everything from scratch, I decided to look for some pre-existing code that I can work with, rather than write another image to matrix converter myself. I found a GitHub repository with pre-existing matrix driving code which I thought will be quite suitable for the software part, thus allowing me to spend more time on the physical construction.**Total time spent: 1 hour**

## Project Redesign - Jun 27, 2026, 3:13 PM - 3h

<img width="698" height="254" alt="image" src="https://github.com/user-attachments/assets/d250f90b-e8e5-4dab-b731-4536374f9443" />

After giving my original idea a day to simmer, I realized that it was time to rethink the brains of the project. While I initially started out designing everything around using a Raspberry Pi Zero, I ended up switching to an ESP32-S3 once I had compared it with the previous. The ESP32-S3 reduced the amount of different parts I would need – I didn’t have to use the full SD card / OS solution anymore, nor did I need the whole power management chain necessary for the full Linux board, not to mention that ESP32-S3 is a lot cheaper than Pi Zero and that helped a lot in keeping the overall budget lower given that there are still a lot of other things to buy (LEDs, aluminum, wires). Having the controller sorted out, it was time to take a look at the software side of things and figure out how to communicate with Spotify.
**Total time spent: 3 hour**

## Library Research - Jun 27, 2026, 4:55 PM - 1h

<img width="1291" height="547" alt="image" src="https://github.com/user-attachments/assets/02f59d96-758f-410f-aebe-350f5ef8dfd7" />

Once I had determined the hardware path, it was time to figure out how to do the software part. Instead of writing the firmware straight up in MicroPython or bare C, I decided to use CircuitPython – mainly because of the availability of displays and networking libraries for it. I started doing research on what particular CircuitPython libraries I would need for such a project – from matrix driving library to an HTTP request library for connecting to Spotify, as well as for loading and decoding images to be displayed. In addition, I installed Mu as a code editor since it is designed explicitly for CircuitPython development, and it features a built-in serial console – greatly simplifying the process of debugging on-device code. Having done all that, I wrote some very basic scripts (blinking pins, printing messages to a serial port) that I would later be able to run the second I got my hands on the ESP32-S3 microcontroller.
**Total time spent: 1 hour**

## Block out programming - Jun 28, 2026, 5:09 PM - 5h

<img width="1673" height="591" alt="image" src="https://github.com/user-attachments/assets/e2778a1a-7ad5-4668-8cfa-a6202f4cdbea" />

It is in this session that I began to write the code for interaction with Spotify itself. I watched additional tutorials on how to construct the request to the endpoint of Spotify's API to receive currently playing track and parse received JSON to get the song's name and its album art URL. However, before any of these could be done, I needed to register a Spotify Developer application on the Spotify for Developers' website and obtain the Client ID and Client Secret and set the OAuth redirect URI. The reason behind this step lies in the fact that Spotify's API will not provide playback data to the anonymous request – access token associated with registered application with appropriate scope is required. As I did not want to write down my actual authentication credentials into the code I was still debugging and providing screenshots from, I left placeholders for Client ID, Client Secret, and access token in the script and planned to fill in the real values at a later point. By the end of the session, I already had functioning code for obtaining the current song and album art URL, even though no real authentication values were used yet.**Total time spent: 5 hour**

## Finished Display Code - Jun 29, 2026, 12:41 PM - 4.5h

<img width="1776" height="973" alt="image" src="https://github.com/user-attachments/assets/2f4387aa-436d-4205-8b28-e234e3222d3a" />

This lesson was all about closing the gap between "I can get the song and album art" and "I can see it on the matrix." I took the code that downloads the album art in last week's lesson and wrote some new code that displays the downloaded image on the matrix by pushing it through. In order to do this, I had to import a new library to drive the matrix, providing pixel/row addressing for the panel, as well as an image library to decode the downloaded image into a format that the matrix library would understand. Writing the actual code to glue the two together was relatively simple, a handful of lines of code. The problem was finding libraries that supported each other and the resolution/color depth I wanted, and then getting the colors and orientation right when rendering it.**Total time spent: 4.5 hour**

## Researching Custom Matrix - Jul 11, 2026, 1:02 PM - 1.8h

<img width="331" height="280" alt="image" src="https://github.com/user-attachments/assets/ded44f9e-6e39-4825-b161-0ba0600ec1e8" />

After working with the display code, I decided that buying a premade matrix panel wasn't going to get me the size, spacing, or physical mounting flexibility I wanted, so I committed to building the LED matrix myself from individual LED strips instead. This meant a pretty significant scope change, since I'd now be responsible for the physical layout, wiring, and power delivery of over a thousand individually addressable LEDs rather than just plugging in a finished panel. I spent this time researching how other people have tackled DIY matrices of this scale and landed on a plan to use 16 separate LED strips of 16 LEDs each (rather than one continuous 256-LED run) specifically to cut down on how much physical wiring and soldering I'd have to do to lay out a full 16x16 grid — shorter, pre-cut strip segments are much easier to route, especially with the zig-zag ("boustrophedon") data-line pattern this kind of matrix typically needs.
**Total time spent: 1.8 hour**

## Custom Matrix Parts - Jul 11, 2026, 2:36 PM - 1h

<img width="545" height="308" alt="image" src="https://github.com/user-attachments/assets/1b75bd7b-31ab-441b-a7d7-0407748c1fa6" />

However, after analyzing the display code I came to the conclusion that purchasing the ready-made matrix panel would not give me the desired dimensions, the distance between the elements and the flexibility in terms of mounting, which is why I have decided to create my own matrix using the individual LED strips. It is important to admit that such approach entailed a substantial change in the scope of work since I was expected to make a proper arrangement of more than a thousand individually addressable LEDs instead of installing the finished panel. In order to find out what are the methods used by others in creating the DIY matrix I did some research and made the decision to use 16 individual LED strips each of 16 LEDs. My decision was made in order to minimize the number of wires and soldering required for the creation of a 16x16 matrix since such strips are easier to arrange using the boustrophedon (zag-zag) pattern of the data line.**Total time spent: 1 hour**

## Wiring Diagram - Jul 12, 2026, 2:24 PM - 2.5h

<img width="1674" height="1186" alt="image" src="https://github.com/user-attachments/assets/73f3e662-ecfb-4634-a53f-b76cf2f7e867" />

This was the session where the electrical design actually came together. I finished a full wiring diagram in KiCad covering every electronic component in the system: the level shifter converting the Pico's 3.3V data signal up to 5V logic, an LM2596 buck voltage regulator to step the 12V supply down to 5V for the logic-side components, and the fusing needed to protect both the low-voltage logic and the high-current LED rails. I picked a Mean Well 12V/8.5A power supply to run the matrix, since 256 WS2815 LEDs pulling current at full brightness needs a supply that can comfortably handle that load without sagging. What I hadn't nailed down by the end of this session was the correct fuse sizing — I knew I needed fusing both on the main 12V input and on each individual LED row for safety, but hadn't worked out the exact amperage for each yet — and I also still needed to figure out the physical layout of where every one of these components (level shifter, regulator, fuse holder) would actually sit on the back of the board once it was built.
**Total time spent: 2.5 hour**

## Component Searching - Jul 12, 2026, 4:39 PM - 1.5h

<img width="645" height="446" alt="image" src="https://github.com/user-attachments/assets/5a597f91-3959-4e64-94f9-9927af3ee87d" />

With the diagram mostly locked in, I spent this session doing the less glamorous but necessary work of actually hunting down real, purchasable parts that matched every line item in my schematic — checking that connector types, wire gauges, and fuse ratings I'd specified on paper had real off-the-shelf equivalents I could buy, and that they'd physically fit together (right AWG wire fitting the terminal connectors I'd chosen, the level shifter's package type being something I could actually hand-solder, etc.). Cost was a constant factor in every decision here; since a custom LED matrix at this scale has a lot of line items that can each creep upward in price, I was comparing vendors and equivalent parts against each other to keep the running total as close to my original budget target as I could.
**Total time spent: 1.5 hour**

## Double Checked Diagrams and Parts - Jul 13, 2026, 4:14 PM - 2h

<img width="3024" height="4032" alt="lower me plz" src="https://github.com/user-attachments/assets/83df6204-6950-49c1-bb99-31e094f88c25" />

This session was a pass over everything I'd sourced the day before, specifically hunting for cheaper equivalents of the same parts, since a lot of the components (fuses, connectors, wire) have multiple suppliers at very different price points for functionally identical products. I also spent time working out how to combine orders across fewer shipments, since with this many small individual line items, shipping costs can quietly add up to a significant fraction of the total project cost if you're not careful about which vendor you're ordering each part from and whether orders can be consolidated.
**Total time spent: 2 hour**

## Finished Github Repo - Jul 15, 2026, 12:21 PM - 2.5h

<img width="1283" height="653" alt="image" src="https://github.com/user-attachments/assets/30dd34d8-da14-4f26-a52d-8d88b9a0a4a5" />

I put this session toward documenting the build so far in a public GitHub repository, rather than leaving all of this knowledge only in my own notes. I wrote out step-by-step build instructions covering the 3D-printed grid pieces, the drilling patterns, and the diffuser assembly, and attached all the supporting files people would need to actually replicate the build — the 3D models for the printed grid segments and the wiring/schematic diagrams from KiCad. One detail I made sure to call out explicitly in the instructions is that the screw lengths used to mount the aluminum plate to the printed grid (I used M2x10 screws in my own 5mm-thick aluminum build) aren't universal — since backplate thickness can vary depending on what aluminum stock someone else sources, I noted that builders should adjust screw length up or down to match whatever thickness plate they're actually using, rather than assuming my exact measurements will fit their build.
**Total time spent: 2.5 hour**

## Programming and Debugging Pi Pico - Aug 7th, 2026, 9:38 AM - 3.3h

<img width="538" height="260" alt="image" src="https://github.com/user-attachments/assets/542ba551-e33e-4a13-84e6-3722f7414291" />

With the physical matrix design largely settled, I shifted back to firmware, this time specifically targeting the Raspberry Pi Pico 2 W as my controller. Getting the board onto WiFi turned out to be shockingly painless — CircuitPython's networking support handled the connection with very little code on my end. Where I actually lost time was getting the right CircuitPython libraries imported and recognized on the board; between library version mismatches and making sure each required library (and its own dependencies) were copied correctly into the /lib folder on the CIRCUITPY drive, there was a fair amount of trial and error before imports stopped throwing errors and the board would boot cleanly into my actual application code.
**Total time spent: 3.3 hour**

## Updating GitHub Repo and Code - Aug 9, 2026, 9:13 PM - 3.5h

<img width="1048" height="390" alt="image" src="https://github.com/user-attachments/assets/3da58b24-14d2-4375-bfb1-7e885c303856" />

I went back into the code to remove the record-style spinning animation for the album art, since it was adding complexity and CPU overhead I decided wasn't worth keeping for now, and swapped out a few of the libraries I'd originally chosen for ones that worked more cleanly with the Pico 2 W. Alongside the code changes, I updated the GitHub repository to reflect both the software changes and the latest state of the hardware design. I also added a full Bill of Materials table to the README, listing every component, quantity, price, and purchase link, since that had been requested and it makes the project meaningfully easier for anyone else to actually replicate — without a BOM, someone would have to reverse-engineer the parts list from the wiring diagram alone.
**Total time spent: 3.5 hour**

## Rewrote Code For Raspberry Pi Pico 2w - aug 15, 2026, 10:09 PM - 1h

<img width="839" height="594" alt="image" src="https://github.com/user-attachments/assets/74cc19c5-287e-4cb1-a14a-2c1117d6a7e5" />

I did another pass on the firmware, this time rewriting it specifically around the Pico 2 W's NeoPixel-style addressable LED handling rather than code I'd adapted from a different board target. While I was in there, I also refactored the main loop, pulling repeated logic out into small helper functions (for things like polling Spotify, decoding the album art, and pushing pixel data to the matrix) instead of having it all inline in one long loop. This didn't change what the code actually does, but it made the codebase noticeably easier to read and to modify going forward.
**Total time spent: 1 hour**

## Online Demo Of Working code - aug 20, 2026, 10:15 AM - 5.8h

<img width="937" height="872" alt="image" src="https://github.com/user-attachments/assets/29568522-b1ab-450b-abc3-1c9900c78d65" />

For this session I built a browser-based demo so people could see how the project works without needing the physical hardware in front of them. The demo takes a user's Spotify credentials just long enough to fetch their current album art (nothing is saved or stored server-side) and renders that album art as pixel art at a few different resolutions, so viewers can get a sense of how the image would look at, say, 16x16 versus a higher-resolution matrix. Most of the time in this session went into the actual client-side programming — handling the Spotify auth flow in a browser context and writing the pixelation/downsampling logic so the art would actually look intentional at low resolution rather than just blurry. Once the logic was working, deploying it as a hosted site was comparatively quick.
**Total time spent: 5.8 hour**

## Transferred From Macondo - sep 1, 2026
I transferred from Macondo and I wasn't required to have either a hacktime or a lapse to show for my programming time. I was initially told I needed this but Cha Cha Cha Charles in slack said that I didn't need this and should add this note to my journal. I have been told MANY times that it is okay, so i'm making it clear that I DON'T have a hackatime or lapse.
<img width="1520" height="430" alt="image" src="https://github.com/user-attachments/assets/a7bc098b-3882-4199-9be0-e265a6d3e0d3" />

# Total Time: 39.4h

## Initial Research — Jun 26, 2026, 2:22 PM — 1h

<img width="553" height="488" alt="image" src="https://github.com/user-attachments/assets/890de1ac-e780-4340-982e-453ff7ecb252" />
<img width="453" height="470" alt="image" src="https://github.com/user-attachments/assets/e839eea0-1458-4847-8f35-4656cb64a8d4" />

**What I did:** Looked into RGB LED matrix panels and picked 64x64 as my target resolution.

**Why:** I wanna show album covers on it. Album art is pretty much always square so the real question was how much detail you can keep before it just turns into mush. I compared album art at diffrent resolutions. At 32x32 text and small stuff like logos just disapear. At 128x128 it barely looks better then 64x64 but the panel cost, wiring and power draw go up like 4x. So 64x64 is the sweet spot. You can still tell what the album is without needing a giant expensive panel.

I also decided the point of this project is the hardware not the software. The wiring, the matrix, the enclosure. Not writing my own image to matrix renderer from scratch. So instead of making a driver myself I looked on github for matrix code that already exists. That way I could spend my time on the physical build. I skimmed alot of READMEs and example code for some open source matrix libraries and made a shortlist of the ones that looked actually maintained (recent commits, people answering issues) vs the ones that looked abandoned.

**How I got there:** I read a few beginner tutorials on how RGB matrix addressing works. Basically the panels only do a few rows at a time not the whole thing at once. They use shift registers and a scan rate trick so every row looks like its always on even tho its being redrawn super fast. This matters because every manufacturer wires the scanning differently, like 1/8 scan, 1/16 scan, 1/32 scan. If your library is made for one scan type it wont work right on a different one. The image comes out sheared or doubled or with dead rows. I needed to understand this BEFORE buying stuff not after. If I got it wrong I'd be returning parts, paying return shipping and waiting a week or more for a replacement.

**Total time spent: 1 hour**

---

## Project Redesign — Jun 27, 2026, 3:13 PM — 3h

<img width="698" height="254" alt="image" src="https://github.com/user-attachments/assets/d250f90b-e8e5-4dab-b731-4536374f9443" />
<img width="1750" height="376" alt="image" src="https://github.com/user-attachments/assets/d76ee919-7a29-4493-9fb1-0d34bbed4108" />

**What I did:** Dropped the Raspberry Pi Zero as the controller and switched to an ESP32-S3.

**Why:** I let my first plan sit for a day before buying anything and im glad I did. The Pi Zero comes with way too much baggage. Its a full linux computer so it needs an SD card with an OS flashed on it, a boot sequence that has to finish before my code even runs, and power management stuff (undervoltage detection, proper shutdown) just to stay reliable. None of that is needed for something that just checks an API on a timer and sends pixels to a matrix. Thats a job for a microcontroller not a whole computer.

The ESP32-S3 does the same thing with way less complexity. It boots in milliseconds right into my code. No filesystem to corrupt, no OS services fighting for the cpu or the wifi. Its also cheaper, a bare ESP32-S3 board is well under half of a Pi Zero 2 W plus a good SD card. That mattered alot because I still had to buy LEDs, aluminum, wire, connectors and a power supply. I wanted to keep the total cost under control from the start.

I also thought about what debugging a Pi Zero would be like later. If the SD card gets corrupted after a power blip (which happens more then people think) the whole thing goes dark until you reflash a card. A microcontroller running from flash just reboots and keeps going.

**Problem it avoided:** If I stuck with the Pi Zero I'd be debugging a linux boot process and power sequencing on top of everything else. Thats a totally different skill set (systemd, boot logs, SD card corruption) stacked on the project I actually wanted to make. Catching it a day in before buying anything saved me from a way bigger rework. Switching controllers after wiring the whole matrix around Pi Zero GPIO pins would have meant redoing the entire electronics side.

**Total time spent: 3 hours**

---

## Library Research — Jun 27, 2026, 4:55 PM — 1h

<img width="1291" height="547" alt="image" src="https://github.com/user-attachments/assets/02f59d96-758f-410f-aebe-350f5ef8dfd7" />

**What I did:** Picked CircuitPython as the firmware language, picked out the libraries I need (matrix driving, HTTP requests for Spotify, image loading and decoding) and installed Mu as my editor.

**Why CircuitPython instead of MicroPython or bare C:** It came down to libraries. I checked if there were maintained libraries for driving an addressable LED matrix, making HTTPS requests (Spotifys API is TLS only), and decoding a compressed image on the device without using too much memory. CircuitPython had good options for all three with example code and recent commits. So I wouldnt have to write low level networking or display code on top of everything else. I thought about bare C with ESP-IDF for more control and speed but the extra dev time wasnt worth it. My time was the real bottleneck not the microcontrollers clock speed.

**Why Mu specifically:** Its made for CircuitPython and has a built in serial console. I could see print statements and errors from the board without setting up a seperate serial terminal or figuring out what COM port or /dev/tty the board is on. Its a small thing but it removes a step from every debug cycle and that adds up over dozens of cycles.

**How I used the time:** I wrote some small throwaway scripts, like blinking a pin, printing to serial and a basic wifi connect test, so when the ESP32-S3 showed up I'd already have working starter code. When the board came I could check it worked right away and go straight to the real project code.

**Total time spent: 1 hour**

---

## Block Out Programming — Jun 28, 2026, 5:09 PM — 5h

<img width="1673" height="591" alt="image" src="https://github.com/user-attachments/assets/e2778a1a-7ad5-4668-8cfa-a6202f4cdbea" />

**What I did:** Wrote the code to get the currently playing track and the album art URL from Spotifys API.

**Why the extra setup was needed:** Spotifys API wont give playback data to anonymous requests. You need an access token from a registered app with the right scope. So before I could even write "get current song" I had to make a Spotify Developer app, get a Client ID and Client Secret, and set up an OAuth redirect URI. Its not optional its a hard requirement. I read Spotifys Web API auth docs to figure out which flow to use and it was the Authorization Code flow, because I needed a refresh token. That way the device can log itself back in instead of me having to re-approve it every hour when the access token expires.

Once the app was registered I wrote the request code. Its an HTTPS GET to the "currently playing" endpoint and then I parse the JSON for the track name, artist and album art URL. Spotify gives you a few different sizes of the art not just one, so I had to pick which one to download. Grabbing the biggest would waste bandwidth and memory decoding a image way bigger then the matrix could ever show.

**Mistake/decision I made on purpose:** I left the Client ID, Client Secret and access token as placeholders in the script instead of my real ones, since the code was still being debugged and screenshotted. I didnt want real credentials in debug output or screenshots. Even a screenshot posted here could leak a secret. The tradeoff was I couldnt fully test the auth flow end to end this session. I checked that the logic for getting the song and art URL was right by tracing through the request/response and checking my parsing against Spotifys documented JSON. Real auth stayed untested until I could put in real credentials somewhere I control who sees them.

**Total time spent: 5 hours**

---

## Finished Display Code — Jun 29, 2026, 12:41 PM — 4.5h

<img width="1776" height="973" alt="image" src="https://github.com/user-attachments/assets/2f4387aa-436d-4205-8b28-e234e3222d3a" />

**What I did:** Closed the gap between "I can fetch the album art" and "I can see it on the matrix."

**Why this took 4.5 hours even tho the glue code was short:** Connecting the download to the display was like a handful of lines. Download the JPEG, give it to a decoder, give the decoded pixels to the matrix driver, call refresh. The real time sink was library compatibility. I needed a matrix library and an image decoding library that both supported the resolution and color depth I wanted AND could actually work together. Image decoders spit out pixels in whatever format is easiest for them (RGB565, RGB888, sometimes with alpha) and matrix libraries usually want a specific format too. When they dont match you need a conversion step or the image comes out garbled. I went through a couple library combos before finding a pair where the formats lined up enough that I only needed a small conversion function.

Once images were showing up the colors and orientation were wrong on the first few tries. Its a common problem when matrix libraries expect a certain pixel format or byte order. I had to work through that before the album art looked right. I tested with covers that have really distinct recognizable colors on purpose, so a color or orientation bug would be obvious right away. A mostly red cover showing up with blue and green swapped is easy to catch. A photo with muted similar tones might not be.

**Mistake and fix:** My first working render had swapped colors and was flipped. I had to trace how the image library encoded the pixel data vs what the matrix library wanted and fix the conversion step. The decoder output pixels top to bottom, left to right, but the matrix librarys buffer wanted a diffrent row order to match how it physically scans the panel. The color channel order (RGB vs BGR) was wrong too. I fixed both with a real conversion pass instead of a quick hack, because I knew I'd be coming back to this code later.

**Total time spent: 4.5 hours**

---

## Researching Custom Matrix — Jul 11, 2026, 1:02 PM — 1.8h

<img width="331" height="280" alt="image" src="https://github.com/user-attachments/assets/ded44f9e-6e39-4825-b161-0ba0600ec1e8" />
<img width="833" height="437" alt="Screenshot 2026-07-11 133824" src="https://github.com/user-attachments/assets/8b4c6994-4676-40b1-8d67-3d5ce108b857" />

**What I did:** Decided to drop the premade matrix panel and build a 16x16 LED matrix myself out of individual LED strips.

**Why (the mistake I was fixing):** A premade panel is the easy way but it locks you into fixed pixel spacing, fixed size and whatever mounting the manufacturer designed. I thought about how I wanted it to mount and look, like a specific pixel pitch and frame depth, sitting flush in a certain spot, and a premade panel just wasnt gonna get me there. The off the shelf ones came in sizes and spacings that didnt match what I wanted. This was a real scope change. Instead of plugging in a finished part I now had to lay out, wire and power over a thousand individually addressable LEDs myself. That meant redoing alot of the electrical and mechanical planning I already did around the premade panels built in driver board.

**How I approached it:** I read a bunch of build logs and forum threads about big DIY matrices. I looked at how people laid out data lines across that many LEDs without the wiring becoming a mess. I landed on 16 seperate 16-LED strips instead of one continuous 256-LED run. Shorter pre-cut pieces are way easier to route and solder than one giant strip. A bad solder joint in the middle of a 256 LED run means debugging or resoldering a huge length of wire. A bad joint on a 16 LED piece is a much smaller problem. This matters because the matrix needs a zig-zag ("boustrophedon") data line pattern to keep wiring manageable. The data line goes down one strip, jumps to the next one, and runs back, switching direction every row. That also meant planning to physically flip every other strips connector.

**Total time spent: 1.8 hours**

---

## Custom Matrix Parts — Jul 11, 2026, 2:36 PM — 1h

<img width="545" height="308" alt="image" src="https://github.com/user-attachments/assets/1b75bd7b-31ab-441b-a7d7-0407748c1fa6" />

**What I did:** Followed up on the last sessions decision and locked in the strip count and layout plan for the DIY matrix.

**Why I spent more time on something I already decided:** I wanted to double check my reasoning before spending money on it. I needed to confirm 16 strips of 16 LEDs was actually the right split and not like 8 strips of 32, and that it works cleanly with the boustrophedon data line thing. Buying strips is a real commitment, return shipping on cut LED strip is annoying at best and sometimes they dont even accept it. I didnt wanna order based on a plan I only thought through once. So I re-derived it on my own. I counted solder joints for each layout (16x16 needs less total jumper connections then 32 strips of 8). I checked how many power injection points each option needs because of voltage drop over the strips. I also re-confirmed the physical size still matched the panel size I wanted.

**Outcome:** The 16x16 strip plan was the right call. It keeps soldering and wiring simple compared to fewer longer strips, and keeps the number of jumpers lower then a layout with more shorter strips would. That gave me enough confidence to start sourcing parts.

**Total time spent: 1 hour**

---

## Wiring Diagram — Jul 12, 2026, 2:24 PM — 2.5h

<img width="1674" height="1186" alt="image" src="https://github.com/user-attachments/assets/73f3e662-ecfb-4634-a53f-b76cf2f7e867" />

**What I did:** Made a full KiCad wiring diagram. It has every electronic part in the system: the controller, level shifter, regulator, fusing, power supply and all 16 LED strips with their data and power connections.

**Why I picked each part:**
- **Level shifter:** The Pico outputs 3.3V logic but the LED data line needs 5V logic to work reliably. Without it the signal gets flaky, especially over long wires, which is exactly what happens with 16 strips spread over a panel. A weak 3.3V signal might work on a test bench with one short strip and then fail randomly once it has to travel real wire in the finished piece. I wasnt gonna skip it and just hope.
- **LM2596 buck regulator:** Steps the 12V supply down to 5V for the logic parts. The LEDs and the logic stuff need different voltages from the same supply. I picked a buck converter over a linear regulator because a linear one dropping 12V to 5V at any real current wastes a ton of power as heat. A switching regulator is way more efficient for that big of a drop.
- **Fusing:** Needed to protect the low voltage logic side AND the high current LED rails if something goes wrong. A short on the LED side shouldnt be able to kill the logic side and the other way around. Each one needs its own protection.
- **Mean Well 12V/8.5A power supply:** I sized this on purpose. 256 WS2815 LEDs at full brightness pull enough current that a too small supply would sag. You'd see dimming or color differences across the matrix, with LEDs near the power injection point staying bright and the far ones visibly dim. I figured out about what full white full brightness would draw across all 256 LEDs and made sure the supply had real headroom above the worst case, instead of sizing it for average brightness.

**What I left unfinished (and why):** By the end of this session I hadnt figured out the exact fuse amperage for the main 12V input or for each LED row. I knew fusing was needed in both places for safety but I hadnt done the current draw math yet. I also hadnt decided where the level shifter, regulator and fuse holder would physically go on the back of the board. I left both open on purpose and didnt just guess. Getting fuse sizing wrong is a safety issue not a "fix it later" thing. A too small fuse just blows all the time which is annoying. A too big fuse doesnt protect against a fault like its supposed to. I wasnt gonna pick a "probably fine" number without doing the math.

**Total time spent: 2.5 hours**

---

## Component Searching — Jul 12, 2026, 4:39 PM — 1.5h

<img width="645" height="446" alt="image" src="https://github.com/user-attachments/assets/5a597f91-3959-4e64-94f9-9927af3ee87d" />

**What I did:** Took every line from the schematic and hunted down real parts I can actually buy that match it.

**Why this needed its own time seperate from the diagram:** A schematic can say "20AWG wire" or "a level shifter in package X" but that doesnt mean a part exists that you can buy, fits the connectors I picked, or that I can solder by hand. I checked wire gauge against the terminal connectors, making sure the wire would actually seat and crimp right instead of being too thick to fit or too thin to make good contact. I also made sure the level shifters package was something I could hand solder (through-hole or a bigger SOIC style) and not something that needs reflow equipment I dont have, like a tiny QFN.

**Constraint I was working under:** Cost mattered for every choice. A custom matrix this big has so many line items (256 LEDs, connectors, wire, the level shifter, regulator, fuse holders, the power supply) that small price differences add up fast. I actively compared vendors and equivalent parts to stay close to my budget instead of just buying the first thing I found. For a bunch of things I kept a few tabs open comparing price per unit at different quantities. Some suppliers had big price breaks at round number quantities that were worth hitting even if I had to buy a little more then I needed.

**Total time spent: 1.5 hours**

---

## Double-Checked Diagrams and Parts — Jul 13, 2026, 4:14 PM — 2h

<img width="3024" height="4032" alt="lower me plz" src="https://github.com/user-attachments/assets/83df6204-6950-49c1-bb99-31e094f88c25" />

**What I did:** Went back over everything I sourced the day before, this time looking specificly for cheaper equivalents.

**Why a seperate pass instead of just buying what I found:** Alot of the parts (fuses, connectors, wire) have multiple suppliers selling basically the same thing for really different prices. If I bought off the first search result I would have overpayed on a few things without even knowing. I went line by line through my parts list and searched each one again while excluding the first vendor I found. That forced me to actually look at other options instead of getting stuck on what I already saw.

**Second thing I optimized:** Shipping. With this many small parts from different vendors, shipping can quietly become a huge part of the total cost if everything ships seperately. A $2 connector isnt worth much if it comes with $6 shipping. I spent part of this session figuring out which orders I could combine into fewer shipments from the same vendor instead of treating every part like its own purchase. In a few cases that meant picking a slightly more expensive part from a vendor I was already ordering from over a cheaper one from a vendor I'd have to pay seperate shipping for.

**Total time spent: 2 hours**

---

## Finished GitHub Repo — Jul 15, 2026, 12:21 PM — 2.5h

<img width="1283" height="653" alt="image" src="https://github.com/user-attachments/assets/30dd34d8-da14-4f26-a52d-8d88b9a0a4a5" />

**What I did:** Documented the build so far in a public GitHub repo. It has step by step instructions for the 3D printed grid pieces, drilling patterns and diffuser assembly, plus all the supporting files like the 3D models and the KiCad wiring and schematic diagrams.

**Why:** Up to this point all of this knowledge was only in my notes and my head. If I stopped working on it, or someone else wanted to copy it, none of it could be recovered. Making a public repo forces the documentation to actually be complete and understandable to someone who isnt me. Thats a different bar then notes I write for myself, since I have to write out steps I'd normally skip because I already know them.

I organized the repo so the 3D printable files, the KiCad project and the written build steps all have their own clearly labeled folders. I wrote the main README as a top down walkthrough: print the grid, drill the backplate, wire the strips, assemble the diffuser. Its in the order someone would actually do them not the order I happened to figure them out in.

**A mistake I made sure other builders wouldnt repeat:** My build used M2x10 screws to mount the aluminum plate to the printed grid, sized for my 5mm thick aluminum. If I just wrote "use M2x10 screws" with no context, someone with a diffrent plate thickness would get screws that are too short or too long and either strip the mount or poke out the front. So I pointed out that screw length isnt universal and has to match whatever backplate thickness you use. I put in the formula I used (grid mounting boss depth + plate thickness + a small margin) so someone with different stock can work out their own screw length instead of guessing.

**Total time spent: 2.5 hours**

---

## Programming and Debugging Pi Pico — Aug 7, 2026, 9:38 AM — 3.3h

<img width="538" height="260" alt="image" src="https://github.com/user-attachments/assets/542ba551-e33e-4a13-84e6-3722f7414291" />

**What I did:** Went back to firmware, this time targeting the Raspberry Pi Pico 2 W.

**What went smooth and why:** Getting wifi working was almost too easy. CircuitPythons built in networking handled the connection with barely any code, I just gave it the SSID and password and called connect. That proved the earlier choice to use CircuitPython was right. After how much time I already sunk into other parts of this project it was a relief to have at least one thing just work on the first real try.

**Where I actually lost time (the real story of this session):** Getting the right CircuitPython libraries to be recognized on the board. It wasnt one clean install. There were library version mismatches, where a library made for a diffrent CircuitPython version silently fails or throws a confusing error instead of a helpful "wrong version" message. I also had to make sure every library I needed, plus each ones own dependencies, got copied right into the /lib folder on the CIRCUITPY drive. CircuitPython libraries often depend on other libraries that arent obvious from the name. A missing dependency gives an import error that doesnt really tell you whats actually missing.

It took alot of trial and error. Install a library, reboot, get an import error, realize a dependency is missing, install that, reboot, get the next missing dependency, repeat. Thats how it went until the board would finally boot into my actual code instead of crashing on an import. I ended up keeping a running list of every library I installed and checking it against each ones documented requirements. Thats what finally broke the cycle.

**Total time spent: 3.3 hours**

---

## Updating GitHub Repo and Code — Aug 9, 2026, 9:13 PM — 3.5h

<img width="1048" height="390" alt="image" src="https://github.com/user-attachments/assets/3da58b24-14d2-4375-bfb1-7e885c303856" />

**What I did:** Removed the record style spinning animation for the album art, swapped out a few libraries for ones that work better with the Pico 2 W, and updated the GitHub repo including a full Bill of Materials table in the README.

**Why I cut the spinning animation:** It was adding real cpu overhead and code complexity for something thats purely cosmetic. Rotating the album art meant recalculating pixel positions every single frame instead of just pushing a static buffer to the matrix. On a microcontroller thats also doing wifi, HTTP polling and image decoding, that wasnt worth it right now. I'd rather have a snappy reliable core then a spinning animation that makes polling feel slow. So I cut it instead of trying to optimize around it.

**Why the library swap:** A few of the libraries I picked at first werent playing nice with the Pico 2 W specificly, since they were partly written and tested around the ESP32-S3. I was getting occasional hangs and one librarys timing assumptions didnt work on the Pico 2 Ws hardware. Instead of patching around board specific problems in libraries that werent made for this board, I moved to ones with cleaner and more actively tested Pico 2 W support. That meant I had to re-verify the display and networking code still worked after the swap.

**Why the BOM specificly:** This was directly requested. Without it, someone trying to copy the build would have to reverse engineer a full parts list from the wiring diagram, matching schematic symbols back to real parts you can buy. Thats exactly the boring work I already did in the Component Searching session. Publishing the BOM (component, quantity, price, purchase link) turns that into a copy paste job for anyone else building this instead of making them redo hours of vendor comparison.

**Total time spent: 3.5 hours**

---

## Rewrote Code for Raspberry Pi Pico 2 W — Aug 15, 2026, 10:09 PM — 1h

<img width="839" height="594" alt="image" src="https://github.com/user-attachments/assets/74cc19c5-287e-4cb1-a14a-2c1117d6a7e5" />

**What I did:** Rewrote the firmware around the Pico 2 Ws native NeoPixel style addressable LED handling instead of code adapted from a diffrent board. I also refactored the main loop.

**Why the rewrite instead of just patching the adapted code:** Code adapted from another boards approach builds up small mismatches and workarounds over time. Pin definitions that were copy pasted and only half updated. Timing constants tuned for a diffrent microcontrollers clock speed. If statements that only existed to handle the old boards quirks. Rewriting the LED part around what the Pico 2 W natively supports got rid of that whole "translation" layer, instead of patching around it and piling up even more workaround on workaround.

**Why the refactor:** The main loop had grown into one giant block doing Spotify polling, album art decoding and pixel pushing all inline. Its the kind of function where you have to read every single line to understand any of it because nothing is seperated. I pulled each piece out into small helper functions with clear names that each do one thing. Its purely a maintainability change and doesnt change how it behaves. But now if I need to debug just the polling, I dont have to read the whole loop at once. I can jump straight to the helper function.

**Total time spent: 1 hour**

---

## Online Demo of Working Code — Aug 20, 2026, 10:15 AM — 5.8h

<img width="937" height="872" alt="image" src="https://github.com/user-attachments/assets/29568522-b1ab-450b-abc3-1c9900c78d65" />

**What I did:** Built a browser based demo so people can see the project working without needing the actual hardware.

**Why:** Not everyone who finds this project is gonna build the hardware just to see if its worth building. A web demo makes it easier. Someone can log in with their own Spotify, see their real album art get fetched, and preview how it would look pixelated at different resolutions (16x16 vs a higher res matrix), all without touching a soldering iron. I wanted the demo to actually look like what the physical matrix would show, not just display the original album art. Getting the downsampling right was a real requirement not just a nice to have.

**Privacy decision:** The demo only uses the users Spotify credentials long enough to fetch their current album art on the client side. Nothing gets saved or stored on a server. I did this on purpose. I didnt want to be in the position of storing other peoples Spotify auth data on a server I run. Thats a real liability, both a "someone could hack my server and steal peoples tokens" problem and a "now I need a privacy policy and a data handling process" problem, that I didnt wanna deal with for a lightweight demo.

**Where the time actually went:** Most of the 5.8 hours was client side programming. I had to handle the Spotify OAuth flow completely in the browser instead of through a backend, which goes back to the "nothing stored server side" decision, and it meant working inside the limits of the Implicit Grant / PKCE style flow instead of the easier server side flow I used for the firmware. I also wrote the pixelation/downsampling logic so the low res previews looked intentionally blocky like real pixel art instead of just blurry from bad resizing. Normal image resizing (bilinear or nearest neighbor scaling down) gives a soft blurry result not the crisp blocky look of a real low res LED matrix. So I made a proper box-downsample then nearest-neighbor-upscale pipeline to get a preview that actually looks like what the hardware would show. Once that worked, deploying the site was pretty fast. Most of the leftover time went into picking a static hosting option and making sure the OAuth redirect URI was set up right for the deployed URL and not just my local dev server.

**Total time spent: 5.8 hours**

---

## Transferred From Macondo — Sep 1, 2026

I transferred over from Macondo. I was originally told I'd need either a Hackatime record or a lapse to account for my programming time on this project, but Charles confirmed in Slack that this isnt required for a transfer and asked me to note that in my journal. Ive been told this multiple times now so to be clear: **I do not have a Hackatime record or a lapse, and Ive been told thats expected/fine for a transfer.**

<img width="1520" height="430" alt="image" src="https://github.com/user-attachments/assets/a7bc098b-3882-4199-9be0-e265a6d3e0d3" />

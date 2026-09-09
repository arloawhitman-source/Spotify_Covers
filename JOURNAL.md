# Total Time: 39.4h

## Initial Research — Jun 26, 2026, 2:22 PM — 1h

<img width="553" height="488" alt="image" src="https://github.com/user-attachments/assets/890de1ac-e780-4340-982e-453ff7ecb252" />
<img width="453" height="470" alt="image" src="https://github.com/user-attachments/assets/e839eea0-1458-4847-8f35-4656cb64a8d4" />

**What I did:** Looked into RGB LED matrix panels. Picked 64x64 as the target resolution.

**Why:** I wanted to show album covers. Album art is basically always square, so the real question was how much detail I could keep before it turned into mush. I compared album art downsampled to different resolutions. At 32x32, text and small details like logos disappear. At 128x128, things barely improve over 64x64, but the panel cost, wiring, and power draw roughly quadruple. 64x64 is the sweet spot. Recognizable album art, without an oversized and expensive panel.

I also decided the point of this project was the hardware, not the software. The wiring, the physical matrix, the enclosure. Not writing my own image-to-matrix renderer from scratch. So instead of building a driver myself, I looked for existing matrix-driving code on GitHub. That let me spend my time on the physical build instead. I skimmed READMEs and example code for a handful of open-source matrix libraries. I made a shortlist of the ones that looked actively maintained (recent commits, issues getting answered) versus the ones that looked abandoned.

**How I got there:** I read a few beginner tutorials on RGB matrix addressing. How rows, data lines, and refresh rate work together. RGB matrix panels are addressed a few rows at a time, not the whole panel at once. They use shift registers and a scan-rate trick so each row looks constantly lit, even though it's actually being redrawn rapidly. This matters because manufacturers wire that scanning differently — 1/8 scan, 1/16 scan, 1/32 scan. A driver library built for one scan type won't work right on a panel using a different one. The image comes out sheared, doubled, or with dead rows. I needed to understand this before buying hardware, not after. Getting it wrong would have meant returning parts, eating return shipping, and losing a week or more waiting on a replacement.

**Total time spent: 1 hour**

---

## Project Redesign — Jun 27, 2026, 3:13 PM — 3h

<img width="698" height="254" alt="image" src="https://github.com/user-attachments/assets/d250f90b-e8e5-4dab-b731-4536374f9443" />
<img width="1750" height="376" alt="image" src="https://github.com/user-attachments/assets/d76ee919-7a29-4493-9fb1-0d34bbed4108" />

**What I did:** Dropped the Raspberry Pi Zero as the controller. Switched to an ESP32-S3.

**Why:** I let the original plan sit for a day before buying parts. The Pi Zero brought a lot of baggage I didn't need. It's a full Linux computer. It needs an SD card flashed with an OS image, a boot sequence that has to finish before my own code runs, and a power-management chain — undervoltage detection, proper shutdown handling — just to stay reliable long-term. None of that is necessary for something that just polls an API on a timer and pushes pixel data to a matrix. That's a job for a microcontroller, not a general-purpose computer.

The ESP32-S3 does that job with a fraction of the complexity. It boots in milliseconds straight into my code. No filesystem to corrupt. No OS-level services competing for CPU time or network bandwidth. It's also cheaper — a bare ESP32-S3 dev board costs well under half of a Pi Zero 2 W plus a reliable SD card. That mattered, since I still had LEDs, aluminum stock, wiring, connectors, and a power supply to buy. I wanted to keep the total build cost under control from the start.

I also thought through what debugging a Pi Zero in the field would look like. If the Pi Zero's SD card gets corrupted after a power blip, which happens more than people expect, the whole thing goes dark until you re-flash a card. A microcontroller running from flash just reboots and keeps going.

**Problem it avoided:** Had I stuck with the Pi Zero, I'd have been debugging a Linux boot process and power sequencing on top of everything else. That's an entirely separate skill set — systemd services, boot logs, SD card corruption — layered onto the project I actually wanted to build. Catching this a day in, before I'd bought anything, saved me from a much bigger rework later. Swapping controllers after wiring a whole matrix around Pi Zero-specific GPIO pinouts would have meant re-deriving the entire electronics side of the project.

**Total time spent: 3 hours**

---

## Library Research — Jun 27, 2026, 4:55 PM — 1h

<img width="1291" height="547" alt="image" src="https://github.com/user-attachments/assets/02f59d96-758f-410f-aebe-350f5ef8dfd7" />

**What I did:** Picked CircuitPython as the firmware language. Picked out the libraries I'd need — matrix driving, HTTP requests for Spotify, image loading and decoding. Installed Mu as my editor.

**Why CircuitPython instead of MicroPython or bare C:** Library availability decided it. I checked whether there were maintained libraries for driving an addressable LED matrix, making authenticated HTTPS requests (Spotify's API is TLS-only), and decoding a compressed image format on-device with a small memory footprint. CircuitPython had actively maintained options for all three, with example code and recent commit history. That meant I wouldn't be stuck writing low-level networking or display code myself on top of everything else. I briefly considered bare C with the ESP-IDF, for more control and better performance, but decided the extra development time wasn't worth it. My own time was the real bottleneck, not the microcontroller's clock speed.

**Why Mu specifically:** It's built for CircuitPython and has a built-in serial console. I could see print statements and errors from the board without setting up a separate serial terminal or figuring out which COM port or /dev/tty device the board showed up as. Small thing, but it removes a step from every debug cycle, and that adds up over dozens of cycles.

**How I used the time:** I wrote small throwaway scripts — blinking a pin, printing to serial, a basic WiFi connect test — so that the moment the ESP32-S3 arrived, I'd have known-good starter code to load. When the board arrived, I could verify it was working right away and move straight into project-specific code.

**Total time spent: 1 hour**

---

## Block Out Programming — Jun 28, 2026, 5:09 PM — 5h

<img width="1673" height="591" alt="image" src="https://github.com/user-attachments/assets/e2778a1a-7ad5-4668-8cfa-a6202f4cdbea" />

**What I did:** Wrote the code to fetch the currently-playing track and album art URL from Spotify's API.

**Why the extra setup was necessary:** Spotify's API doesn't return playback data to anonymous requests. You need an access token tied to a registered app with the right scope. So before writing any "get current song" logic, I had to register a Spotify Developer app, get a Client ID and Client Secret, and set up an OAuth redirect URI. This isn't optional, it's a hard requirement of the API. I read Spotify's Web API auth docs to figure out which OAuth flow fit — the Authorization Code flow, since I needed a refresh token. That way the device could re-authenticate itself instead of me manually re-approving it every hour when the access token expired.

Once the app was registered, I wrote the request logic. An HTTPS GET to the "currently playing" endpoint, parsing the JSON response for track name, artist, and the album art URL. Spotify returns several resolution options for the art, not one image. I had to pick which to download — grabbing the largest would waste bandwidth and memory decoding an image far bigger than the matrix could ever show.

**Mistake/decision I made on purpose:** I left Client ID, Client Secret, and access token as placeholders in the script instead of my real values, since this code was still being actively debugged and screenshotted. I didn't want real credentials sitting in debug output or screenshots. Even a screenshot posted here for documentation could leak a secret. The tradeoff was I couldn't fully verify the auth flow worked end-to-end this session. I confirmed the logic for fetching the song and album art URL was correct by tracing through the request/response structure and checking my parsing against Spotify's documented JSON schema. Real authentication stayed untested until I could swap in real credentials somewhere I controlled who'd see them.

**Total time spent: 5 hours**

---

## Finished Display Code — Jun 29, 2026, 12:41 PM — 4.5h

<img width="1776" height="973" alt="image" src="https://github.com/user-attachments/assets/2f4387aa-436d-4205-8b28-e234e3222d3a" />

**What I did:** Closed the gap between "I can fetch the album art" and "I can see it on the matrix."

**Why this took 4.5 hours despite the actual glue code being short:** Wiring the download logic to the display logic was maybe a handful of lines. Download the JPEG, hand it to a decoder, hand the decoded pixel buffer to the matrix driver, call refresh. The real time sink was library compatibility. I needed a matrix-driving library and an image-decoding library that both supported the resolution and color depth I wanted, and could actually talk to each other cleanly. Image-decoding libraries output pixel data in whatever format is convenient for them (RGB565, RGB888, sometimes with alpha). Matrix-driving libraries usually expect a specific format too. When those don't match you need a conversion step, or the image comes out garbled. I went through a couple of library combinations before finding a pair where the formats lined up well enough that I only needed a lightweight conversion function.

Once images were rendering, colors and orientation came out wrong on the first few attempts. This is a common issue with matrix libraries expecting a specific pixel format or byte order. I had to work through that before album art looked right on the panel. I tested with album covers that had very distinct, recognizable color schemes on purpose, so a color or orientation bug would be obvious right away. A mostly-red cover showing up with blue and green swapped is easy to catch. A photo with muted, similar tones might not be.

**Mistake and fix:** My first working render had swapped colors and a flipped orientation. I had to trace through how the image library encoded pixel data versus what the matrix library expected, and adjust the conversion step. The image decoder output pixels top-to-bottom, left-to-right. The matrix library's buffer expected a different row order, to match how it physically scans the panel. The color channel order (RGB vs BGR) didn't match either. I fixed both with an explicit conversion pass instead of a quick hack, since I knew I'd be revisiting this code later.

**Total time spent: 4.5 hours**

---

## Researching Custom Matrix — Jul 11, 2026, 1:02 PM — 1.8h

<img width="331" height="280" alt="image" src="https://github.com/user-attachments/assets/ded44f9e-6e39-4825-b161-0ba0600ec1e8" />
<img width="833" height="437" alt="Screenshot 2026-07-11 133824" src="https://github.com/user-attachments/assets/8b4c6994-4676-40b1-8d67-3d5ce108b857" />

**What I did:** Decided to drop the premade matrix panel. Decided to build the 16x16 LED matrix myself from individual LED strips.

**Why — the mistake I was correcting:** A premade panel is the easy path, but it locks you into fixed pixel spacing, fixed size, and whatever mounting the manufacturer designed for. I thought through how I wanted this to physically mount and look — a specific pixel pitch and frame depth, flush in a particular spot. A premade panel wasn't going to get me there. The off-the-shelf options came in fixed sizes and spacings that didn't match what I wanted. This was a real scope change. Instead of plugging in a finished part, I was now on the hook for laying out, wiring, and powering over a thousand individually addressable LEDs myself. That meant re-deriving a lot of the electrical and mechanical planning I'd already done around the premade panel's built-in driver board.

**How I approached it:** I read through a handful of build logs and forum threads on large DIY matrices. I looked at how people laid out data lines across that many LEDs without the wiring turning into a mess. I landed on 16 separate 16-LED strips instead of one continuous 256-LED run. Shorter pre-cut segments are much easier to route and solder than one giant strip. A bad solder joint partway down a 256-LED run means debugging or resoldering a huge length of wire. A bad joint on a 16-LED segment is a much smaller, contained problem. This matters because the whole matrix needs a zig-zag ("boustrophedon") data-line pattern to keep wiring manageable — the data line runs down one strip, jumps to the adjacent strip, and runs back, alternating direction row by row. That also meant planning for physically flipping every other strip's connector orientation.

**Total time spent: 1.8 hours**

---

## Custom Matrix Parts — Jul 11, 2026, 2:36 PM — 1h

<img width="545" height="308" alt="image" src="https://github.com/user-attachments/assets/1b75bd7b-31ab-441b-a7d7-0407748c1fa6" />

**What I did:** Followed up on the previous session's decision. Locked in the strip-count and layout plan for the DIY matrix.

**Why I spent more time on a decision I'd already made:** I wanted to sanity-check the earlier reasoning before spending money on it. Confirming that 16 strips of 16 LEDs was actually the right split, rather than 8 strips of 32, and that it would work cleanly with the boustrophedon data-line pattern. Buying strips is a real cost commitment — return shipping on cut LED strip is annoying at best, and sometimes not accepted at all. I didn't want to order off a plan I'd only reasoned through once. So I re-derived it independently. I counted solder joints under each layout option (16x16 needs fewer total inter-strip jumper connections than 32 strips of 8). I checked power-injection points needed for each option given voltage drop over LED strip runs. I re-confirmed the physical dimensions still matched the panel size I wanted.

**Outcome:** Confirmed the 16x16-strip plan was the right call. It minimizes soldering and wiring complexity compared to fewer, longer strips, while keeping the total jumper/connection count lower than a layout with more, shorter strips would need. That gave me enough confidence to move to sourcing parts.

**Total time spent: 1 hour**

---

## Wiring Diagram — Jul 12, 2026, 2:24 PM — 2.5h

<img width="1674" height="1186" alt="image" src="https://github.com/user-attachments/assets/73f3e662-ecfb-4634-a53f-b76cf2f7e867" />

**What I did:** Built a complete KiCad wiring diagram. It covers every electronic component in the system — controller, level shifter, regulator, fusing, power supply, and all 16 LED strips with their data and power connections.

**Why each part was chosen:**
- **Level shifter:** The Pico outputs 3.3V logic, but the LED data line needs 5V logic to register reliably. Without it, signal integrity gets flaky, especially over longer wire runs — exactly the situation with 16 strips spread across a physical panel. A marginal 3.3V signal might work on a test bench with one short strip, then fail intermittently once it has to travel real wire lengths in the finished piece. I wasn't willing to skip this and hope for the best.
- **LM2596 buck regulator:** Steps the 12V main supply down to 5V for the logic-side components. The LEDs and logic electronics need different voltages off the same supply. I picked a buck converter over a linear regulator because a linear regulator dropping 12V to 5V at any real current wastes a lot of power as heat. A switching regulator is far more efficient for that big a voltage drop.
- **Fusing:** Needed to protect both the low-voltage logic side and the high-current LED rails from a fault in either direction. A short on the LED side shouldn't be able to take out the logic side, and vice versa. Each needs its own protection.
- **Mean Well 12V/8.5A power supply:** Sized this deliberately. 256 WS2815 LEDs at full brightness draw enough current that an undersized supply would sag under load. That shows up as dimming or color inconsistency across the matrix — LEDs near the power injection point staying bright while ones further away visibly dim. I worked out roughly what full-white, full-brightness draw across all 256 LEDs would look like, and made sure the supply had meaningful headroom above that worst case, rather than sizing it to average expected brightness.

**What I left unfinished (and why):** By the end of this session I hadn't worked out exact fuse amperage for the main 12V input or for each individual LED row. I knew fusing was needed in both places for safety, but hadn't done the current-draw math yet. I also hadn't decided where the level shifter, regulator, and fuse holder would physically sit on the back of the board. Both were left open on purpose, not guessed at. Getting fuse sizing wrong is a safety issue, not a "fix it later" inconvenience. An undersized fuse just blows constantly and is annoying. An oversized fuse doesn't protect against a fault the way it's supposed to. I wasn't willing to pick a "probably fine" number without doing the calculation.

**Total time spent: 2.5 hours**

---

## Component Searching — Jul 12, 2026, 4:39 PM — 1.5h

<img width="645" height="446" alt="image" src="https://github.com/user-attachments/assets/5a597f91-3959-4e64-94f9-9927af3ee87d" />

**What I did:** Took every line item from the schematic and hunted down real, purchasable parts to match it.

**Why this needed dedicated time separate from the diagram itself:** A schematic can specify "20AWG wire" or "a level shifter in package X," but that doesn't guarantee a part exists that's actually buyable, fits the connectors I'd chosen, or is solderable by hand. I checked wire gauge against terminal connector compatibility, making sure the wire I picked would actually seat and crimp properly, rather than being too thick to fit or too thin to make solid contact. I also made sure the level shifter's package type was something I could hand-solder — through-hole or a larger SOIC-style package — rather than something needing reflow equipment I don't have, like a fine-pitch QFN package.

**Constraint I was working under:** Cost was a factor in every choice here. A custom matrix at this scale has enough individual line items — 256 LEDs, connectors, wire, the level shifter, the regulator, fuse holders, the power supply — that small per-part price creep adds up fast. I actively compared vendors and functionally-equivalent parts against each other to stay close to my budget target, instead of buying the first matching part I found. For several items I kept a couple of tabs open comparing price-per-unit at different quantities. Some suppliers had steep price breaks at round-number quantities worth hitting, even if it meant buying slightly more than I needed.

**Total time spent: 1.5 hours**

---

## Double-Checked Diagrams and Parts — Jul 13, 2026, 4:14 PM — 2h

<img width="3024" height="4032" alt="lower me plz" src="https://github.com/user-attachments/assets/83df6204-6950-49c1-bb99-31e094f88c25" />

**What I did:** Went back over everything sourced the day before, this time specifically hunting for cheaper equivalents.

**Why a separate pass instead of just buying what I'd found the day before:** A lot of the components — fuses, connectors, wire — have multiple suppliers selling functionally identical parts at very different prices. Buying on the first search result would've meant overpaying on several line items without realizing it. I went line by line back through my parts list, re-searching each one and specifically excluding the first vendor I'd already found. That forced me to actually look at alternatives instead of anchoring on what I'd already seen.

**Second thing I optimized for:** Shipping consolidation. With this many small individual parts spread across different vendors, shipping costs can quietly become a big chunk of total project cost if each part ships separately — a $2 connector isn't worth much if it comes with its own $6 shipping charge. I spent part of this session working out which orders could be combined onto fewer shipments from the same vendor, instead of treating each line item as an independent purchase. In a few cases that meant choosing a slightly more expensive per-part price from a vendor I was already ordering from, over a cheaper part from a vendor I'd otherwise have paid separate shipping to.

**Total time spent: 2 hours**

---

## Finished GitHub Repo — Jul 15, 2026, 12:21 PM — 2.5h

<img width="1283" height="653" alt="image" src="https://github.com/user-attachments/assets/30dd34d8-da14-4f26-a52d-8d88b9a0a4a5" />

**What I did:** Documented the build so far in a public GitHub repo. Step-by-step instructions for the 3D-printed grid pieces, drilling patterns, and diffuser assembly, plus all supporting files — 3D models, KiCad wiring and schematic diagrams.

**Why:** Up to this point all of this knowledge only lived in my own notes and head. If I stopped working on this, or someone else wanted to replicate it, none of that would be recoverable. Writing it as a public repo forces the documentation to actually be complete and understandable to someone who isn't me. That's a different bar than notes I write for myself, since I have to spell out steps I'd otherwise skip because I already know them.

I organized the repo so the 3D-printable files, the KiCad project, and the written build steps each live in their own clearly-labeled folder. I wrote the main README as a top-down walkthrough: print the grid, drill the backplate, wire the strips, assemble the diffuser — in the order someone would actually do them, not the order I happened to figure them out in.

**A mistake I made sure future builders wouldn't repeat:** My own build used M2x10 screws to mount the aluminum plate to the printed grid, sized for my specific 5mm-thick aluminum stock. If I'd just written "use M2x10 screws" without context, someone using a different plate thickness would get screws that are too short or too long, and either strip the mount or poke through the front. So I called out that screw length isn't universal, and needs to match whatever backplate thickness the builder is using. I included the formula I used — grid mounting-boss depth plus plate thickness plus a small margin — so someone with different stock could work out their own correct screw length instead of guessing.

**Total time spent: 2.5 hours**

---

## Programming and Debugging Pi Pico — Aug 7, 2026, 9:38 AM — 3.3h

<img width="538" height="260" alt="image" src="https://github.com/user-attachments/assets/542ba551-e33e-4a13-84e6-3722f7414291" />

**What I did:** Shifted back to firmware, now specifically targeting the Raspberry Pi Pico 2 W.

**What went smoothly and why:** Getting WiFi working was almost trivial. CircuitPython's built-in networking support handled the connection with very little code — just supplying SSID/password and calling connect. That validated the earlier decision to use CircuitPython in the first place. Given how much time I'd already sunk into other parts of this project, having at least one piece just work on the first real attempt was a relief.

**Where I actually lost time (the real story of this session):** Getting the right CircuitPython libraries recognized on the board. This wasn't one clean install. It involved library version mismatches — a library built against a different CircuitPython version silently failing or throwing an unclear error instead of a helpful "wrong version" message. It also meant making sure every required library, plus each of its own dependencies, got copied correctly into the `/lib` folder on the CIRCUITPY drive. CircuitPython libraries often depend on other libraries that aren't obvious from the top-level library's name. A missing transitive dependency produces an import error that doesn't obviously point at what's actually missing.

This took a lot of trial and error. Install a library, reboot, see an import error, realize a dependency was missing, install that, reboot, see the next missing dependency, repeat. That's how it went before the board would boot cleanly into my actual application code instead of failing on an import. I ended up keeping a running list of every library I'd installed, and cross-checking it against each one's documented requirements. That's what finally broke the cycle.

**Total time spent: 3.3 hours**

---

## Updating GitHub Repo and Code — Aug 9, 2026, 9:13 PM — 3.5h

<img width="1048" height="390" alt="image" src="https://github.com/user-attachments/assets/3da58b24-14d2-4375-bfb1-7e885c303856" />

**What I did:** Removed the record-style spinning animation for the album art. Swapped out a few libraries for ones that worked more cleanly with the Pico 2 W. Updated the GitHub repo, including a full Bill of Materials table in the README.

**Why I cut the spinning animation:** It was adding real CPU overhead and code complexity for a purely cosmetic feature. Rotating the rendered album art meant recalculating pixel positions on every frame, instead of just pushing a static buffer to the matrix. On a microcontroller that's also handling WiFi, HTTP polling, and image decoding, that overhead wasn't worth it right now. I'd rather have a snappy, reliable core experience than a spinning animation that made polling feel sluggish. So I cut it instead of trying to optimize around it.

**Why the library swap:** A few of my originally-chosen libraries weren't playing well with the Pico 2 W specifically, as opposed to the ESP32-S3 they were partly written and tested around. I was seeing occasional hangs, and one library's timing assumptions didn't hold on the Pico 2 W's hardware. Instead of patching around board-specific quirks in libraries that weren't written for this board, I moved to alternatives with cleaner, more actively-tested Pico 2 W support. That meant re-verifying the display and networking code still worked after the swap.

**Why the BOM specifically:** This had been directly requested. Without it, someone trying to replicate the build would have to reverse-engineer a full parts list from the wiring diagram alone — matching schematic symbols back to real purchasable parts. That's exactly the tedious work I'd already done in the Component Searching session. Publishing the BOM (component, quantity, price, purchase link) turns that reverse-engineering work into a copy-paste job for anyone else building this, instead of making them redo hours of vendor comparison I'd already done.

**Total time spent: 3.5 hours**

---

## Rewrote Code for Raspberry Pi Pico 2 W — Aug 15, 2026, 10:09 PM — 1h

<img width="839" height="594" alt="image" src="https://github.com/user-attachments/assets/74cc19c5-287e-4cb1-a14a-2c1117d6a7e5" />

**What I did:** Rewrote the firmware around the Pico 2 W's native NeoPixel-style addressable LED handling, instead of code adapted from a different board target. Also refactored the main loop.

**Why the rewrite instead of continuing to patch the adapted code:** Code adapted from another board's approach builds up small mismatches and workarounds over time. Pin definitions that were copy-pasted and half-updated. Timing constants tuned for a different microcontroller's clock speed. Conditional branches that only existed to handle the old board's quirks. Rewriting the LED-handling portion around what the Pico 2 W natively supports removed that layer of "translation" entirely, instead of patching around it and piling up even more workaround-on-workaround complexity.

**Why the refactor:** The main loop had grown into one long block handling Spotify polling, album art decoding, and pixel pushing all inline. The kind of function where you have to read every line to understand what any part does, because nothing is separated out. I pulled each piece into small helper functions with clear names and single responsibilities. This is purely a maintainability change, it doesn't alter behavior. But future changes, like debugging just the polling logic, don't require reading the entire loop at once. I can jump straight to the relevant helper function.

**Total time spent: 1 hour**

---

## Online Demo of Working Code — Aug 20, 2026, 10:15 AM — 5.8h

<img width="937" height="872" alt="image" src="https://github.com/user-attachments/assets/29568522-b1ab-450b-abc3-1c9900c78d65" />

**What I did:** Built a browser-based demo that lets people see the project working without needing the physical hardware.

**Why:** Not everyone who finds this project is going to build the hardware just to see if it's worth building. A web demo lowers the barrier. Someone can log in with their own Spotify account, see their real album art fetched, and preview how it would look pixelated at different resolutions (16x16 vs. a higher-res matrix), all without touching a soldering iron. I wanted the demo to actually reflect what the physical matrix would look like, not just show the original album art. Getting the downsampling behavior right was a real requirement, not a nice-to-have.

**Privacy decision:** The demo uses the user's Spotify credentials only long enough to fetch their current album art client-side. Nothing is saved or stored server-side. I made this choice on purpose. I didn't want to be in the position of storing other people's Spotify auth data on a server I run. That's a real liability — both a "someone could compromise my server and get people's tokens" angle, and a "now I need a privacy policy and data-handling process" angle — that I didn't want to take on for what's meant to be a lightweight demo.

**Where the time actually went:** Most of the 5.8 hours was client-side programming. Handling the Spotify OAuth flow entirely in the browser rather than through a backend, which ties back to the "nothing stored server-side" decision, and meant working within the constraints of the Implicit Grant / PKCE-style flow instead of the simpler server-side flow I'd used for the firmware. Also writing the pixelation/downsampling logic so low-resolution previews looked intentionally blocky like real pixel art, instead of just blurry from naive resizing. Naive image resizing (simple bilinear or nearest-neighbor scaling down) produces a soft, blurry result, not the crisp blocky look of an actual low-res LED matrix. So I implemented a proper box-downsample-then-nearest-neighbor-upscale pipeline, to get a preview that actually looked like what the hardware would show. Once that logic worked, deploying the site was comparatively fast. Most of the remaining time went into picking a static hosting option and making sure the OAuth redirect URI was correctly configured for the deployed URL, rather than just my local dev server.

**Total time spent: 5.8 hours**

---

## Transferred From Macondo — Sep 1, 2026

I transferred over from Macondo. I was originally told I'd need either a Hackatime record or a lapse to account for my programming time on this project, but Charles confirmed in Slack that this isn't required for a transfer and asked me to note that in my journal. I've been told this multiple times now, so to be clear: **I do not have a Hackatime record or a lapse, and I've been told that's expected/fine for a transfer.**

<img width="1520" height="430" alt="image" src="https://github.com/user-attachments/assets/a7bc098b-3882-4199-9be0-e265a6d3e0d3" />

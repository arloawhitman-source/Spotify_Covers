# Total Time: 39.4h

## Initial Research — Jun 26, 2026, 2:22 PM — 1h

<img width="553" height="488" alt="image" src="https://github.com/user-attachments/assets/890de1ac-e780-4340-982e-453ff7ecb252" />

**What I did:** Researched RGB LED matrix panels and picked a target resolution of 64x64.

**Why:** I wanted to display album covers, and album art is basically always square — the question was just how much detail I could preserve before it started looking like mush. 64x64 seemed like the sweet spot between "recognizable album art" and "not an enormous, expensive panel." I also decided early on that this project's value was in the *hardware* — the wiring, the physical matrix, the enclosure — not in reinventing an image-to-matrix renderer from scratch. So instead of writing my own driver, I went looking for existing matrix-driving code on GitHub that I could build on top of, which let me spend my time budget on the physical build instead of re-solving a problem other people had already solved well.

**How I got there:** Read through several beginner tutorials on RGB matrix addressing — specifically how rows, data lines, and refresh rate interact — since I needed to understand that *before* buying hardware, not after. Getting this wrong (e.g. buying a panel with an addressing scheme my chosen driver didn't support) would've meant returning parts.

**Total time spent: 1 hour**

---

## Project Redesign — Jun 27, 2026, 3:13 PM — 3h

<img width="698" height="254" alt="image" src="https://github.com/user-attachments/assets/d250f90b-e8e5-4dab-b731-4536374f9443" />

**What I did:** Scrapped the Raspberry Pi Zero as the project's controller and switched to an ESP32-S3.

**Why:** I let the original plan sit for a day before committing to parts, and on reflection the Pi Zero brought a lot of baggage I didn't actually need: a full SD card + OS install, and the power management chain a full Linux board requires just to boot reliably. None of that is necessary if all I'm doing is polling an API and pushing pixels to a matrix. The ESP32-S3 does that job with a fraction of the complexity, and it's also considerably cheaper — which mattered because I still had LEDs, aluminum stock, and wiring to buy, and I was trying to keep the total build cost under control.

**Problem it avoided:** Had I stuck with the Pi Zero, I'd have been debugging a Linux boot process and power sequencing on top of everything else. Catching this a day into the project, before I'd bought anything, saved me from a much bigger rework later.

**Total time spent: 3 hours**

---

## Library Research — Jun 27, 2026, 4:55 PM — 1h

<img width="1291" height="547" alt="image" src="https://github.com/user-attachments/assets/02f59d96-758f-410f-aebe-350f5ef8dfd7" />

**What I did:** Chose CircuitPython as the firmware language and picked out the libraries I'd need (matrix driving, HTTP requests for Spotify, image loading/decoding). Installed Mu as my editor.

**Why CircuitPython instead of MicroPython or bare C:** Availability of libraries was the deciding factor — CircuitPython has mature, actively maintained display and networking libraries, which meant I wasn't going to be stuck writing low-level networking or display code myself on top of everything else this project already required.

**Why Mu specifically:** It's purpose-built for CircuitPython and has a built-in serial console, which meant I could see print statements and errors from the board without setting up a separate serial terminal — a small thing, but it removes a step from every single debug cycle I'd be doing later.

**How I used the time:** Wrote small throwaway scripts (blinking a pin, printing to serial) so that the moment the ESP32-S3 physically arrived, I'd have known-good starter code to load rather than debugging "hello world" for the first time with real hardware in my hands.

**Total time spent: 1 hour**

---

## Block Out Programming — Jun 28, 2026, 5:09 PM — 5h

<img width="1673" height="591" alt="image" src="https://github.com/user-attachments/assets/e2778a1a-7ad5-4668-8cfa-a6202f4cdbea" />

**What I did:** Wrote the code to fetch the currently-playing track and album art URL from Spotify's API.

**Why the extra setup was necessary:** Spotify's API doesn't return playback data to anonymous requests — you need an access token tied to a registered app with the right scope. So before I could write a single line of "get current song" logic, I had to register a Spotify Developer app, get a Client ID and Client Secret, and configure an OAuth redirect URI. This wasn't optional overhead; it's a hard requirement of the API.

**Mistake/decision I made on purpose:** I deliberately left Client ID, Client Secret, and access token as placeholders in the script rather than my real values, since this code was still being actively debugged and screenshotted. I didn't want real credentials sitting in debug output or screenshots that could end up public. The tradeoff is that I couldn't fully verify the auth flow worked end-to-end this session — I confirmed the *logic* for fetching the song and album art URL was correct, but real authentication was still untested by the end of the session.

**Total time spent: 5 hours**

---

## Finished Display Code — Jun 29, 2026, 12:41 PM — 4.5h

<img width="1776" height="973" alt="image" src="https://github.com/user-attachments/assets/2f4387aa-436d-4205-8b28-e234e3222d3a" />

**What I did:** Closed the gap between "I can fetch the album art" and "I can see it on the matrix."

**Why this took 4.5 hours despite the actual glue code being short:** Wiring the download logic to the display logic was maybe a handful of lines. The real time sink was *library compatibility* — finding a matrix-driving library and an image-decoding library that both supported the resolution and color depth I wanted, and that could actually talk to each other cleanly. On top of that, once images were rendering, colors and orientation came out wrong on the first few attempts (a common issue with matrix libraries expecting a specific pixel format/byte order), so I had to work through that before album art actually looked correct on the panel.

**Mistake and fix:** My first working render had swapped colors and a flipped orientation — I had to trace through how the image library was encoding pixel data versus what the matrix library expected, and adjust the conversion step accordingly rather than assuming they'd agree by default.

**Total time spent: 4.5 hours**

---

## Researching Custom Matrix — Jul 11, 2026, 1:02 PM — 1.8h

<img width="331" height="280" alt="image" src="https://github.com/user-attachments/assets/ded44f9e-6e39-4825-b161-0ba0600ec1e8" />

**What I did:** Decided to abandon the premade matrix panel and build the 16x16 LED matrix myself from individual LED strips.

**Why — the mistake I was correcting:** A premade panel is the easy path, but it locks you into fixed pixel spacing, fixed size, and whatever mounting the manufacturer designed for. Once I actually thought through how I wanted this to physically mount and look, I realized a premade panel wasn't going to get me there. So this was a real scope change: instead of plugging in a finished part, I was now on the hook for laying out, wiring, and powering over a thousand individually addressable LEDs myself.

**How I approached it:** Researched how other people building large DIY matrices handle the physical layout, and landed on 16 separate 16-LED strips instead of one continuous 256-LED run. The reasoning: shorter pre-cut segments are dramatically easier to route and solder than one giant strip, which matters a lot when the whole matrix needs a zig-zag ("boustrophedon") data-line pattern to keep wiring manageable.

**Total time spent: 1.8 hours**

---

## Custom Matrix Parts — Jul 11, 2026, 2:36 PM — 1h

<img width="545" height="308" alt="image" src="https://github.com/user-attachments/assets/1b75bd7b-31ab-441b-a7d7-0407748c1fa6" />

**What I did:** Followed up on the decision from the previous session and locked in the actual strip-count/layout plan for the DIY matrix.

**Why I spent more time on a decision I'd already made:** I wanted to sanity-check the reasoning from the earlier session before committing money to it — confirming that 16 strips of 16 LEDs was actually the right split, rather than, say, 8 strips of 32, and that it would work cleanly with the boustrophedon data-line pattern the matrix needs. Re-deriving it independently was a way of pressure-testing the earlier decision rather than just assuming it was right.

**Outcome:** Confirmed the 16x16-strip plan was the right call — it minimizes soldering and wiring complexity compared to fewer, longer strips.

**Total time spent: 1 hour**

---

## Wiring Diagram — Jul 12, 2026, 2:24 PM — 2.5h

<img width="1674" height="1186" alt="image" src="https://github.com/user-attachments/assets/73f3e662-ecfb-4634-a53f-b76cf2f7e867" />

**What I did:** Built a complete KiCad wiring diagram covering every electronic component in the system.

**Why each part was chosen:**
- **Level shifter:** The Pico outputs 3.3V logic, but the LED data line needs 5V logic to register reliably — without it, signal integrity gets flaky, especially over longer wire runs.
- **LM2596 buck regulator:** Steps the 12V main supply down to 5V for the logic-side components, since the LEDs and the logic electronics need different voltages off the same supply.
- **Fusing:** Needed to protect both the low-voltage logic side and the high-current LED rails from a fault in either direction.
- **Mean Well 12V/8.5A power supply:** Sized this deliberately rather than picking something arbitrary — 256 WS2815 LEDs at full brightness draw enough current that an undersized supply would sag under load, which shows up as dimming or color inconsistency across the matrix.

**What I left unfinished (and why):** By the end of this session I hadn't worked out exact fuse amperage for the main 12V input or for each individual LED row — I knew fusing was needed in both places for safety, but hadn't done the current-draw math to size them correctly yet. I also hadn't decided the physical layout of where the level shifter, regulator, and fuse holder would actually sit on the back of the board. Both of those were explicitly left open rather than guessed at, since getting fuse sizing wrong is a safety issue, not just a "fix it later" inconvenience.

**Total time spent: 2.5 hours**

---

## Component Searching — Jul 12, 2026, 4:39 PM — 1.5h

<img width="645" height="446" alt="image" src="https://github.com/user-attachments/assets/5a597f91-3959-4e64-94f9-9927af3ee87d" />

**What I did:** Took every line item from the schematic and hunted down real, purchasable parts to match it.

**Why this needed dedicated time separate from the diagram itself:** A schematic can specify "20AWG wire" or "a level shifter in package X," but that doesn't guarantee a part exists that's actually buyable, fits the connectors I'd chosen, or is solderable by hand. I checked wire gauge against terminal connector compatibility, and specifically made sure the level shifter's package type was something I could hand-solder rather than something that would need reflow equipment I don't have.

**Constraint I was working under:** Cost was a factor in every single choice here — a custom matrix at this scale has enough individual line items that small per-part price creep adds up fast, so I was actively comparing vendors and functionally-equivalent parts against each other to stay close to my budget target rather than just buying the first matching part I found.

**Total time spent: 1.5 hours**

---

## Double-Checked Diagrams and Parts — Jul 13, 2026, 4:14 PM — 2h

<img width="3024" height="4032" alt="lower me plz" src="https://github.com/user-attachments/assets/83df6204-6950-49c1-bb99-31e094f88c25" />

**What I did:** Went back over everything sourced the day before, this time specifically hunting for cheaper equivalents.

**Why a separate pass instead of just buying what I'd found the day before:** A lot of the components — fuses, connectors, wire — have multiple suppliers selling functionally identical parts at very different price points. Buying on the first search result would've meant overpaying on several line items without realizing it.

**Second thing I optimized for:** Shipping consolidation. With this many small individual parts spread across different vendors, shipping costs can quietly become a significant fraction of total project cost if each part ships separately. I spent part of this session working out which orders could be combined onto fewer shipments from the same vendor, rather than treating each line item as an independent purchase.

**Total time spent: 2 hours**

---

## Finished GitHub Repo — Jul 15, 2026, 12:21 PM — 2.5h

<img width="1283" height="653" alt="image" src="https://github.com/user-attachments/assets/30dd34d8-da14-4f26-a52d-8d88b9a0a4a5" />

**What I did:** Documented the build so far in a public GitHub repo — step-by-step instructions for the 3D-printed grid pieces, drilling patterns, and diffuser assembly, plus all supporting files (3D models, KiCad wiring/schematic diagrams).

**Why:** Up to this point all of this knowledge only existed in my own notes and head — if I stopped working on this or wanted someone else to replicate it, none of that would be recoverable. Writing it as a public repo forces the documentation to actually be complete and understandable to someone who isn't me.

**A mistake I made sure future builders wouldn't repeat:** My own build used M2x10 screws to mount the aluminum plate to the printed grid, sized for my specific 5mm-thick aluminum stock. If I'd just written "use M2x10 screws" without context, someone using a different plate thickness would get screws that are too short or too long and either strip the mount or poke through the front. So instead I explicitly called out that screw length isn't universal and needs to be adjusted to match whatever backplate thickness the builder is actually using.

**Total time spent: 2.5 hours**

---

## Programming and Debugging Pi Pico — Aug 7, 2026, 9:38 AM — 3.3h

<img width="538" height="260" alt="image" src="https://github.com/user-attachments/assets/542ba551-e33e-4a13-84e6-3722f7414291" />

**What I did:** Shifted back to firmware, now specifically targeting the Raspberry Pi Pico 2 W.

**What went smoothly and why:** Getting WiFi working was almost trivial — CircuitPython's built-in networking support handled the connection with very little code, which validated the earlier decision to use CircuitPython in the first place.

**Where I actually lost time (the real story of this session):** Getting the right CircuitPython libraries recognized on the board. This wasn't one clean install — it involved library *version* mismatches (a library built against a different CircuitPython version silently failing or throwing unclear errors) and making sure every required library, plus each of *its own* dependencies, was copied correctly into the `/lib` folder on the CIRCUITPY drive. This took a fair amount of trial and error — installing a library, rebooting, seeing an import error, realizing a dependency was missing, and repeating — before the board would boot cleanly into my actual application code instead of failing on an import.

**Total time spent: 3.3 hours**

---

## Updating GitHub Repo and Code — Aug 9, 2026, 9:13 PM — 3.5h

<img width="1048" height="390" alt="image" src="https://github.com/user-attachments/assets/3da58b24-14d2-4375-bfb1-7e885c303856" />

**What I did:** Removed the record-style spinning animation for the album art, swapped out a few libraries for ones that worked more cleanly with the Pico 2 W, and updated the GitHub repo — including adding a full Bill of Materials table to the README.

**Why I cut the spinning animation:** It was adding real CPU overhead and code complexity for a purely cosmetic feature. On a microcontroller that's also handling WiFi, HTTP polling, and image decoding, that overhead wasn't worth it right now, so I cut it rather than trying to optimize it.

**Why the library swap:** A few of my originally-chosen libraries weren't playing well with the Pico 2 W specifically (as opposed to the ESP32-S3 they were partly written/tested around), so I moved to alternatives with cleaner Pico 2 W support.

**Why the BOM specifically:** This had been directly requested, and without it someone trying to replicate the build would have to reverse-engineer a full parts list from the wiring diagram alone — matching schematic symbols back to real purchasable parts, which is exactly the tedious work I'd already done in the Component Searching session. Publishing the BOM (component, quantity, price, purchase link) turns that reverse-engineering work into a copy-paste job for anyone else building this.

**Total time spent: 3.5 hours**

---

## Rewrote Code for Raspberry Pi Pico 2 W — Aug 15, 2026, 10:09 PM — 1h

<img width="839" height="594" alt="image" src="https://github.com/user-attachments/assets/74cc19c5-287e-4cb1-a14a-2c1117d6a7e5" />

**What I did:** Rewrote the firmware around the Pico 2 W's native NeoPixel-style addressable LED handling, instead of code that had been adapted from a different board target. Also refactored the main loop.

**Why the rewrite instead of continuing to patch the adapted code:** Code that was adapted from another board's approach tends to accumulate small mismatches and workarounds over time. Rewriting the LED-handling portion specifically around what the Pico 2 W natively supports removed that layer of "translation" entirely, rather than continuing to patch around it.

**Why the refactor:** The main loop had grown into one long block handling Spotify polling, album art decoding, and pixel pushing all inline. I pulled each of those into small helper functions. This is purely a maintainability change — it doesn't alter behavior — but it means future changes (like debugging just the polling logic) don't require reading and understanding the entire loop at once.

**Total time spent: 1 hour**

---

## Online Demo of Working Code — Aug 20, 2026, 10:15 AM — 5.8h

<img width="937" height="872" alt="image" src="https://github.com/user-attachments/assets/29568522-b1ab-450b-abc3-1c9900c78d65" />

**What I did:** Built a browser-based demo that lets people see the project working without needing the physical hardware.

**Why:** Not everyone who finds this project is going to build the hardware just to see if it's worth building. A web demo lowers the barrier — someone can log in with their own Spotify account, see their real album art fetched, and preview how it would look pixelated at different resolutions (e.g. 16x16 vs. a higher-res matrix), all without touching a soldering iron.

**Privacy decision:** The demo uses the user's Spotify credentials only long enough to fetch their current album art client-side — nothing is saved or stored server-side. I made this choice deliberately since I didn't want to be in the position of storing other people's Spotify auth data on a server I run.

**Where the time actually went:** Most of the 5.8 hours was the client-side programming — handling the Spotify OAuth flow entirely in the browser (rather than through a backend, which ties back to the "nothing stored server-side" decision), and writing the pixelation/downsampling logic so low-resolution previews looked intentionally blocky like real pixel art rather than just blurry from naive resizing. Once that logic worked, actually deploying the site was comparatively fast.

**Total time spent: 5.8 hours**

---

## Transferred From Macondo — Sep 1, 2026

I transferred over from Macondo. I was originally told I'd need either a Hackatime record or a lapse to account for my programming time on this project, but Charles confirmed in Slack that this isn't required for a transfer and asked me to note that in my journal. I've been told this multiple times now, so to be clear: **I do not have a Hackatime record or a lapse, and I've been told that's expected/fine for a transfer.**

<img width="1520" height="430" alt="image" src="https://github.com/user-attachments/assets/a7bc098b-3882-4199-9be0-e265a6d3e0d3" />

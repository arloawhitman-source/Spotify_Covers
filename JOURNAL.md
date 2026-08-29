# Total Time: 39.4h

## Initial Research - Jun 26, 2026, 2:22 PM - 1h

<img width="553" height="488" alt="image" src="https://github.com/user-attachments/assets/890de1ac-e780-4340-982e-453ff7ecb252" />

I researched my needed materials including a 64 x 64 RGB matrix.I also found small tutorials to help me along with choosing the right supplies as well as with programing, as I want to focus more on the hardware not the software. I also found a github repository that can help with the programming portion.

## Project Redesign - Jun 27, 2026, 3:13 PM - 3h


<img width="698" height="254" alt="image" src="https://github.com/user-attachments/assets/d250f90b-e8e5-4dab-b731-4536374f9443" />


I changed the components of my project from initially using a Raspberry Pi Zero to using a ESP32-S3, This simplified the number of items I need as well as reducing the price by around 50%. Finally I researched how to communicate using a Spotify API.

## Library Research - Jun 27, 2026, 4:55 PM - 1h

<img width="1291" height="547" alt="image" src="https://github.com/user-attachments/assets/02f59d96-758f-410f-aebe-350f5ef8dfd7" />

I researched the circuitpython libraries I would need as well as installing Mu as my code editor, i then wrote some basic scripts to run once i get the ESP32-S3.

## Block out programming - Jun 28, 2026, 5:09 PM - 5h

<img width="1673" height="591" alt="image" src="https://github.com/user-attachments/assets/e2778a1a-7ad5-4668-8cfa-a6202f4cdbea" />

I followed a few tutorials and wrote some simple code to get the current song and album cover, after debuging some more I plan on instating the actual display code. I used Spotify for Developers to make an app and get an API in order to get the song. As of right now the actual API codes arent in the program but have place holders instead.

## Finished Display Code - Jun 29, 2026, 12:41 PM - 4.5h

<img width="1776" height="973" alt="image" src="https://github.com/user-attachments/assets/2f4387aa-436d-4205-8b28-e234e3222d3a" />

I finished linking the code from earlier which gets the current song and album cover and added code for it to display on the matrix. In order to do this I use a matrix library and image loading libraries, this didn't take a lot of time to implement in code but finding the correct library and debugging did take a while.

## Researching Custom Matrix - Jul 11, 2026, 1:02 PM - 1.8h

<img width="331" height="280" alt="image" src="https://github.com/user-attachments/assets/ded44f9e-6e39-4825-b161-0ba0600ec1e8" />

I've decided to make the matrix myself so I've been researching some options and have decided on using 16 LED strips to cut down on the time of wiring over 1,000 LEDs in place.

## Custom Matrix Parts - Jul 11, 2026, 2:36 PM - 1h

<img width="545" height="308" alt="image" src="https://github.com/user-attachments/assets/1b75bd7b-31ab-441b-a7d7-0407748c1fa6" />

I researched the needed parts to make the matrix and got most of them however I was unable to figure out the wiring diagrams I need to base mine on, I also need to install more libraries to KICAD in order to make them correct.

## Wiring Diagram - Jul 12, 2026, 2:24 PM - 2.5h

<img width="1674" height="1186" alt="image" src="https://github.com/user-attachments/assets/73f3e662-ecfb-4634-a53f-b76cf2f7e867" />

I finished the wiring diagram with all of the electronic components, I also chose a power supply however I still need to figure out what size of a fuse to use as well as actually figure out where all of this will go on the back of the board.

## Component Searching - Jul 12, 2026, 4:39 PM - 1.5

<img width="645" height="446" alt="image" src="https://github.com/user-attachments/assets/5a597f91-3959-4e64-94f9-9927af3ee87d" />

I kept looking for components I need and made sure that they would fit, I also tried to keep the price as low as possible.

## Double Checked Diagrams and Parts - Jul 13, 2026, 4:14 PM - 2h

<img width="3024" height="4032" alt="lower me plz" src="https://github.com/user-attachments/assets/83df6204-6950-49c1-bb99-31e094f88c25" />

I spent time finding options that were cheaper and found the most efficient way to get them shipped for the lowest cost possible.

## Finished Github Repo - Jul 15, 2026, 12:21 PM - 2.5h

<img width="1283" height="653" alt="image" src="https://github.com/user-attachments/assets/30dd34d8-da14-4f26-a52d-8d88b9a0a4a5" />

I wrote out instructions as well as attaching all files such as models and wiring diagrams. Some things do vary based on the thickness of your back plate but you simply add or subtract from the screw length.

## Programming and Debugging Pi Pico - Aug 7th, 2026, 9:38 AM - 3.3h

I spent time debugging my code for the raspberry pi pico 2w. It was shockingly easy to get it to connect to WiFi however I did have some trouble importing libraries.

## Updating GitHub Repo and Code - Aug 9, 2026, 9:13 PM - 3.5h

<img width="1048" height="390" alt="image" src="https://github.com/user-attachments/assets/3da58b24-14d2-4375-bfb1-7e885c303856" />

I changed my code to remove spinning and changed some libraries that I am using. I updated my repo to show my changes in both code and hardware. I also displayed the BOM in my README as asked. 

## Rewrote Code For Raspberry Pi Pico 2w - aug 15, 2026, 10:09 PM - 1h

<img width="839" height="594" alt="image" src="https://github.com/user-attachments/assets/74cc19c5-287e-4cb1-a14a-2c1117d6a7e5" />

I rewrote the code so i could use a raspberry pi pico 2w and added neopixel and change the main loop to have helpers to make the code cleaner. 

## Online Demo Of Working code - aug 20, 2026, 10:15 AM - 5.8h

<img width="937" height="872" alt="image" src="https://github.com/user-attachments/assets/29568522-b1ab-450b-abc3-1c9900c78d65" />

I coded a demo which takes the users codes (Doesn't save them) and displays the album cover as pixel art in varying resolutions. The programming took a while however hosting the site was easy.

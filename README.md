Transparent Display
==================

Project for driving a transparent OLED screen with an Arduino.
The prototype uses a Crystalfontz display and Seeeduino 4.2 or 4.3
development board; see the [BOM](#bill-of-materials) for more detail.

![photo of display and dev board](docs/Transparent_Display_Action_Shot.jpg)

Quick Start
-----------

Make sure you have your Seeeduino, the breakout board, the display, and all wires and cables ready.

1. Install ArduinoIDE. You can get the latest version at https://www.arduino.cc/en/software
2. Plug in your Seeeduino by USB to make sure it shows up as serial (COM) device. This procedure differs depending on whether the dev board is 4.2 or 4.3:
   a. Seeeduino 4.2 should be automatically recognized by the serial drivers that come with ArduinoIDE.
   b. Seeeduino 4.3 requires an additional driver for its CP2102 USB to UART bridge chip. Get the "VCP Windows" or "VCP Mac" drivers from the [Silicon Labs CP210x Download Page][cp210x].
3. Install the board definitions for the Seeeduino 4.x in ArduinoIDE, following the instructions from https://wiki.seeedstudio.com/Seeed_Arduino_Boards/
   1. Note that the page has two different URLs listed, one for SAMD21 chips and another for all other Seeeduinos. We want the second one: `https://raw.githubusercontent.com/Seeed-Studio/Seeed_Platform/master/package_legacy_seeeduino_boards_index.json`
4. Use "Board Manager" in ArduinoIDE to set up the board. Seeeduino 4.x is covered by the "Seeeduino AVR" definition.
5. Load this project in the IDE as a sketch. Use "File" -> "Open..." to open `testTOLED/testTOLED.ino`
6. Make sure the breakout board is properly hooked up to the Seeeduino by means of the Dupont headers.
7. Press the "Upload" button (looks like an arrow pointing right) to compile the sketch and write it to the dev board.

At this point, the TOLED display should begin cycling through a series of images whenever the Seeeduino is powered.

Bill of Materials
-----------------

The components for this project are those from the [Crystalfontz Transparent OLED Development Kit][cfkit].

- 128x56 transparent OLED display (CFAL12856A0-0151-B)
- breakout board for the TOLED (CFA10105)
- Seeeduino 4.2 or 4.3

You will also need Dupont/Molex jumper wires and a micro-USB cable; both are supplied in the Crystalfontz kit linked above.

[seeed42]: https://wiki.seeedstudio.com/Seeeduino_v4.2/
[cp210x]: https://www.silabs.com/developer-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads
[cfkit]: https://www.crystalfontz.com/product/cfal12856a00151be12-transparent-oled-development-kit

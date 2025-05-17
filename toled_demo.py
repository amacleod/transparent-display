"""
toled_demo.py - demonstrate the transparent OLED (TOLED) system.

"""

import os

from toled_image_server import serial_responder

import logging as log

log.basicConfig(level=log.INFO, format="%(asctime)s %(levelname)-8s %(message)s")

COM_PORT = os.environ.get("ARDUINO_PORT", "COM3")

port = serial_responder.SerialPort(COM_PORT)
responder = serial_responder.SerialResponder(port)
responder.main_loop()

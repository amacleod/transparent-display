"""
serial_writer.py - proof of concept for Python writing to USB serial port.

"""

import logging as log
import os
import random
import time

from serial import Serial

from . import image_converter
from . import screenshot_puller

log.basicConfig(level=log.DEBUG, format="%(asctime)s %(levelname)-8s %(message)s")

COM_PORT = os.environ.get("ARDUINO_PORT", "COM3")
SLEEP_INTERVAL = 1
READ_TIMEOUT = 0.5


class ArduinoReader(object):
    def __init__(self):
        self.port = Serial(COM_PORT, timeout=READ_TIMEOUT, baudrate=9600)
        log.info(
            f"Serial port opened: {self.port.name}, {self.port.baudrate}, {self.port.bytesize}, {self.port.parity}, {self.port.timeout}")
        self.ready = False

    def read(self) -> str:
        """
        Read a single line from the serial port and log it, also checking
        for readiness by looking for a specific word.

        :return: the response string.
        """
        read_bytes = self.port.read_until(b"\r\n")
        read_string = read_bytes.decode("utf-8")
        response = read_string.strip()
        log.debug(f"From Arduino: '{response}'")
        if "ready" in response:
            self.ready = True
        return response

    def write(self, message: bytes) -> int:
        """
        Write a byte array to the Arduino over the serial port.

        :param message: the bytes to write.
        :return: quantity of bytes written.
        """
        return self.port.write(message)

    def close(self):
        self.port.close()


def main():
    reader = ArduinoReader()
    while True:
        try:
            # message = message_from_screenshot()
            message = message_from_file('data/Ellipse128x56.png')
            read_and_write(reader, message)
            time.sleep(SLEEP_INTERVAL)
        except KeyboardInterrupt:
            log.debug("Interrupted.")
            break
    reader.close()
    log.info("Done.")


def read_and_write(reader: ArduinoReader, message: bytes) -> int:
    """
    Use the Arduino port to read a message, and if it is ready for
    writing send a message and bump up the message index.

    :param reader: the ArduinoReader to use for communication.
    :param message: the message to send if the reader is ready.
    :return: index increment, or 0 if the index should not increase.
    """
    reader.read()
    if reader.ready:
        log.debug(f"Writing: {message}")
        bytes_written = reader.write(message)
        log.debug(f"Wrote {bytes_written} bytes.")
        return 1
    return 0


def random_message(quantity: int) -> bytes:
    return random.randbytes(quantity)


def message_from_screenshot() -> bytes:
    screenshot = screenshot_puller.make_screenshot()
    return image_converter.image_to_bytes(screenshot)


def message_from_file(filename: str) -> bytes:
    return image_converter.bytes_from_file(filename)


if __name__ == "__main__":
    main()

"""
serial-writer.py - proof of concept for Python writing to USB serial port.

"""

import os
import time
from serial import Serial

import logging as log
log.basicConfig(level=log.DEBUG, format="%(asctime)s %(levelname)-8s %(message)s")

COM_PORT = os.environ.get("ARDUINO_PORT", "COM3")
SLEEP_INTERVAL = 1.0
READ_TIMEOUT = 0.5


class ArduinoReader(object):
    def __init__(self, port: Serial):
        self.port = port
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


class ImageByteReader(object):
    def __init__(self):
        self.bytes = None

    def read(self, data_file):
        data_as_text = data_file.read()

        for character in data_as_text:
            pass # TODO: Actually do stuff with pixel data here! ~ACM 2025-03-22



def main():
    output_messages = [b"hello\n", b"everybody\n"]
    ser = Serial(COM_PORT, timeout=READ_TIMEOUT)
    log.info(f"Serial port opened: {ser.name}, {ser.baudrate}, {ser.bytesize}, {ser.parity}, {ser.timeout}")
    reader = ArduinoReader(ser)
    index = 0
    while True:
        try:
            index_delta = read_and_write(reader, get_current_message(index, output_messages))
            index += index_delta
            time.sleep(SLEEP_INTERVAL)
        except KeyboardInterrupt:
            log.debug("Interrupted.")
            break
    ser.close()
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


def get_current_message(index: int, messages: [bytes]) -> bytes:
    """
    Given an incrementing index and an array of byte blobs, pick one
    of the messages.

    :param index: numeric index; expected to start at 0 and increase by 1.
    :param messages: list of messages to choose from.
    :return: one of the messages.
    """
    return messages[index % len(messages)]


if __name__ == "__main__":
    main()

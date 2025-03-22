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
    def __init__(self):
        self.port = Serial(COM_PORT, timeout=READ_TIMEOUT, baudrate=9600)
        log.info(f"Serial port opened: {self.port.name}, {self.port.baudrate}, {self.port.bytesize}, {self.port.parity}, {self.port.timeout}")
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
    output_messages = [b"hello\n", b"everybody\n"]
    index = 0
    while True:
        try:
            #message = get_current_message(index, output_messages)
            message = random_message(896)
            index_delta = read_and_write(reader, message)
            #index += index_delta
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


def get_current_message(index: int, messages: [bytes]) -> bytes:
    """
    Given an incrementing index and an array of byte blobs, pick one
    of the messages.

    :param index: numeric index; expected to start at 0 and increase by 1.
    :param messages: list of messages to choose from.
    :return: one of the messages.
    """
    return messages[index % len(messages)]


def random_message(quantity: int) -> bytes:
    result = bytes()
    for i in range(quantity):
        b = b"\x55" if i%2 == 0 else b"\xaa"
        result+= b
    return result


if __name__ == "__main__":
    main()

"""
serial-writer-test-image.py - proof of concept for Python sending loaded image via USB serial port.

"""

import numpy
# import binascii
import PIL.Image

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 56
DISPLAY_HALF_WIDTH = DISPLAY_WIDTH / 2
DISPLAY_HALF_HEIGHT = DISPLAY_HEIGHT / 2


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


def main():
    test_image_path = "data/Bourbeau_FESCenter.jpg"
    test_image = PIL.Image.open(test_image_path)
    image_width, image_height = test_image.size
    center_x = image_width / 2
    center_y = image_height / 2
    vertical_shift = 75
    box = (
        center_x - DISPLAY_HALF_WIDTH,
        center_y - DISPLAY_HALF_HEIGHT - vertical_shift,
        center_x + DISPLAY_HALF_WIDTH,
        center_y + DISPLAY_HALF_HEIGHT - vertical_shift
    )
    test_image_black_and_white = test_image.convert("1")
    test_image_black_and_white_crop = test_image_black_and_white.crop(box)
    #test_image_black_and_white_crop.show()
    test_image_binary = numpy.asarray(test_image_black_and_white_crop).astype(int)
    # test_image_hex = binascii.hexlify(test_image_binary)
    #print(test_image_binary)



    #output_messages = [b"hello\n", b"everybody\n"]
    #output_messages = test_image_binary
    ser = Serial(COM_PORT, timeout=READ_TIMEOUT)
    log.info(f"Serial port opened: {ser.name}, {ser.baudrate}, {ser.bytesize}, {ser.parity}, {ser.timeout}")
    reader = ArduinoReader(ser)
    while True:
        try:
            read_and_write(reader, image_to_bytes(test_image_binary))
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

def image_to_bytes(input_image: numpy.ndarray) -> bytes:
    allbytes = bytearray()
    for strip in range (7):
        for column in range (128):
            bits = []
            for subrow in range (8):
                row = strip*8+7-subrow
                pixel = input_image[row][column]
                bits.append (pixel)
            currentbyte = bits_to_byte(bits)
            print (currentbyte)
            allbytes.append(currentbyte)
    return allbytes

def bits_to_byte(bits: [int]) -> int:
    result = 0
    for bit in bits:
        result = result<<1 | bit
    return int(result)

if __name__ == "__main__":
    main()

"""
image_converter.py - proof of concept for Python sending loaded image via USB serial port.

"""

import logging as log

import PIL.Image
import numpy

log.basicConfig(level=log.DEBUG, format="%(asctime)s %(levelname)-8s %(message)s")

DEBUG_EVERY_BYTE = False


def bytes_from_file(filename: str) -> bytes:
    image = PIL.Image.open(filename)
    return image_to_bytes(image)


def image_to_bytes(input_image: PIL.Image) -> bytes:
    array = numpy.asarray(input_image).astype(int)
    return array_to_bytes(array)


def array_to_bytes(input_array: numpy.ndarray) -> bytes:
    all_bytes = bytearray()
    for strip in range(7):
        for column in range(128):
            bits = []
            for sub_row in range(8):
                row = strip * 8 + 7 - sub_row
                pixel = input_array[row][column]
                bits.append(pixel)
            current_byte = bits_to_byte(bits)
            if DEBUG_EVERY_BYTE:
                log.debug(current_byte)
            all_bytes.append(current_byte)
    return all_bytes


def bits_to_byte(bits: [int]) -> int:
    result = 0
    for bit in bits:
        result = result << 1 | bit
    return int(result)

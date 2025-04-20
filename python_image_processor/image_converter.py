"""
image_converter.py - proof of concept for Python sending loaded image via USB serial port.

"""

import numpy
# import binascii
import PIL.Image
import logging as log
log.basicConfig(level=log.DEBUG, format="%(asctime)s %(levelname)-8s %(message)s")


def bytes_from_file(filename: str) -> bytes:
    image = PIL.Image.open(filename)
    return image_to_bytes(image)


def image_to_bytes(input_image :PIL.Image) -> bytes:
    array = numpy.asarray(input_image).astype(int)
    return array_to_bytes(array)



def array_to_bytes(input_array: numpy.ndarray) -> bytes:
    allbytes = bytearray()
    for strip in range (7):
        for column in range (128):
            bits = []
            for subrow in range (8):
                row = strip*8+7-subrow
                pixel = input_array[row][column]
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

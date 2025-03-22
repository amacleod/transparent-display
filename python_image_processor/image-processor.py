"""
image-processor - the main image processor program, to be run on the host PC.

"""

import logging as log
import time

import psutil
import PIL.Image
import PIL.ImageOps
from mss import mss

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 56
DISPLAY_HALF_WIDTH = DISPLAY_WIDTH / 2
DISPLAY_HALF_HEIGHT = DISPLAY_HEIGHT / 2

log.basicConfig(level=log.INFO, format="%(asctime)s %(levelname)-8s %(message)s")

# set SHOW_IMAGES to False to prevent image popup debugging
SHOW_IMAGES = True


def main():
    for i in range(5):
        make_screenshot()
    log.info("Done.")


def make_screenshot():
    screenshot = mss()
    screenshot_image = screenshot.grab(screenshot.monitors[1])
    # log.info(f"Loading image: {imageFileName}")
    # input_image = PIL.Image.open(imageFileName)
    image_width, image_height = screenshot_image.size
    input_image = PIL.Image.frombytes(
        "RGB", screenshot_image.size, screenshot_image.bgra, "raw", "BGRX")
    log.info(f"Image dimensions (width, height): ({image_width}, {image_height})")
    im_black_and_white = input_image.convert("1")
    # im_padded = PIL.ImageOps.pad(im_black_and_white, (DISPLAY_WIDTH, DISPLAY_HEIGHT), color="#000")
    center_x = image_width / 2
    center_y = image_height / 2
    box = (
        center_x - DISPLAY_HALF_WIDTH,
        center_y - DISPLAY_HALF_HEIGHT,
        center_x + DISPLAY_HALF_WIDTH,
        center_y + DISPLAY_HALF_HEIGHT
    )
    im_black_and_white_crop = im_black_and_white.crop(box)
    if SHOW_IMAGES:
        im_black_and_white_crop.show("black and white")
        time.sleep(2)
        for proc in psutil.process_iter():
            if proc.name() == "Photos.exe":
                log.info(proc.name())
                proc.kill()


if __name__ == "__main__":
    main()

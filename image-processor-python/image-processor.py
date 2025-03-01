"""
image-processor - the main image processor program, to be run on the host PC.

"""

import logging as log

import PIL.Image
import PIL.ImageOps

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 56
DISPLAY_HALF_WIDTH = DISPLAY_WIDTH / 2
DISPLAY_HALF_HEIGHT = DISPLAY_HEIGHT / 2

log.basicConfig(level=log.INFO, format="%(asctime)s %(levelname)-8s %(message)s")

# TODO: Eventually we want the file to come from outside. ~ACM 2025-03-01
imageFileName = "../MirrahRatio.jpg"
# set SHOW_IMAGES to False to prevent image popup debugging
SHOW_IMAGES = True


def main():
    log.info(f"Loading image: {imageFileName}")
    input_image = PIL.Image.open(imageFileName)
    width, height = input_image.size
    log.info(f"Image dimensions: {width}px wide x {height}px high")
    im_black_and_white = input_image.convert("1")
    im_padded = PIL.ImageOps.pad(im_black_and_white, (DISPLAY_WIDTH, DISPLAY_HEIGHT), color="#000")
    center_x = width / 2
    center_y = height / 2
    box = (
        center_x - DISPLAY_HALF_WIDTH,
        center_y - DISPLAY_HALF_HEIGHT,
        center_x + DISPLAY_HALF_WIDTH,
        center_y + DISPLAY_HALF_HEIGHT
    )
    im_black_and_white_crop = im_black_and_white.crop(box)
    if SHOW_IMAGES:
        im_black_and_white_crop.show("black and white")
    log.info("Done.")


if __name__ == "__main__":
    main()

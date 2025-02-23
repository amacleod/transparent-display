"""
image-processor - the main image processor program, to be run on the host PC.

"""

import logging as log

import PIL.Image
import PIL.ImageOps

log.basicConfig(level=log.INFO, format="%(asctime)s %(levelname)-8s %(message)s")

imageFileName = "../MirrahRatio.jpg"
# set SHOW_IMAGES to False to prevent image popup debugging
SHOW_IMAGES = True


def main():
    log.info(f"Loading image: {imageFileName}")
    input_image = PIL.Image.open(imageFileName)
    width, height = input_image.size
    log.info(f"Image dimensions: {width}px wide x {height}px high")
    im_black_and_white = input_image.convert("1")
    im_padded = PIL.ImageOps.pad(im_black_and_white, (128, 56), color="#000")
    center_x = 205 / 2
    center_y = 246 / 2
    box = (center_x - 64, center_y - 28, center_x + 64, center_y + 28)
    im_black_and_white_crop = im_black_and_white.crop(box)
    if SHOW_IMAGES:
        im_black_and_white_crop.show("black and white")
    log.info("Done.")


if __name__ == "__main__":
    main()

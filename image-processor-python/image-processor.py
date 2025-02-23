"""
image-processor - the main image processor program, to be run on the host PC.

"""

import os, sys
from PIL import Image, ImageOps
imageFileName = "../MirrahRatio.jpg"

def main():
    # for infile in sys.argv[1:]:
    #     f, e = os.path.splitext(infile)
    #     outfile = f + ".png"
    #     if infile != outfile:
    #         try:
    #             with Image.open(infile) as im:
    #                 im.save(outfile)
    #                 im.show()
    #         except OSError:
    #             print("cannot convert", infile)
    #     else:
    #         print("not converting because identical")
    input_image = Image.open(imageFileName)
    im_black_and_white = input_image.convert("1")
    # im_black_and_white.show()
    im_padded = ImageOps.pad(im_black_and_white, (128, 56), color="#000")
    # im_padded.show("padded")
    center_x = 205 / 2
    center_y = 246 / 2
    box = (center_x - 64, center_y - 28, center_x + 64, center_y + 28)
    im_black_and_white_crop = im_black_and_white.crop(box)
    im_black_and_white_crop.show("black and white")
    width, height = im_black_and_white.size
    print(width, height)
if __name__ == "__main__":
    main()

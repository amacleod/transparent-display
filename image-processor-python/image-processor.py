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
    with Image.open(imageFileName) as im:
        im_luminance = im.convert("1")
        im_luminance.show()
    box = (0,0, 128, 56)
    im_luminance_crop = im_luminance.crop(box)
    im_luminance_crop.show()
if __name__ == "__main__":
    main()

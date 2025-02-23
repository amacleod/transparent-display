"""
image-processor - the main image processor program, to be run on the host PC.

"""

import os, sys
from PIL import Image

def main():
    for infile in sys.argv[1:]:
        f, e = os.path.splitext(infile)
        outfile = f + ".png"
        if infile != outfile:
            try:
                with Image.open(infile) as im:
                    im.save(outfile)
                    im.show()
            except OSError:
                print("cannot convert", infile)
        else:
            print("not converting because identical")
if __name__ == "__main__":
    main()

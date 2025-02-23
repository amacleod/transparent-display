"""
image-processor - the main image processor program, to be run on the host PC.

"""

import PIL.Image, PIL.ImageOps

imageFileName = "../MirrahRatio.jpg"


def main():
    input_image = PIL.Image.open(imageFileName)
    im_black_and_white = input_image.convert("1")
    im_padded = PIL.ImageOps.pad(im_black_and_white, (128, 56), color="#000")
    center_x = 205 / 2
    center_y = 246 / 2
    box = (center_x - 64, center_y - 28, center_x + 64, center_y + 28)
    im_black_and_white_crop = im_black_and_white.crop(box)
    im_black_and_white_crop.show("black and white")
    width, height = im_black_and_white.size
    print(width, height)
    

if __name__ == "__main__":
    main()

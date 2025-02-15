// ImageEdit.c - Convert an image on disk to hexadecimal arrays.

// The expected format is an array of arrays of uint8 values
// const uint8_t Splash[7][128] PROGMEM = { ... };

int loadImage() {
	// 1. Find the image on disk (construct file path)
	// 2. Load the image (may need library)
	// 3. Convert the image to grayscale
	// 4. Convert grayscale to 1-bit mono by picking a threshold
	// 5. Scale (and crop) the resolution to produce a 128 wide, 56 tall pixmap
	// 6. Translate sets of 8 adjacent pixels to 8-bit unsigned ints and
	//    convert to hexadecimal literal, in arrays suitable for Arduino
	// 7. Write the hex values from step 6 to file.

	const char* outfile = "";

	return -1;
}

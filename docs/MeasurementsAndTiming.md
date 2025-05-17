Measurements and Timing
=======================

In a test on 2025-05-17 we found that, at 115200 baud, omitting "DEBUG" massages (that is,
keeping the Arduino to Python communication minimal), each frame took about 85 milliseconds
between "FRAME" commands. This works out to about 11.7 frames per second.

Baud rate is the largest determinant of the time per frame: when we were doing things at
9600 baud, the transfer of 896 bytes took nearly a whole second (about 960ms).

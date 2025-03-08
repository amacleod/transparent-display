"""
serial-writer.py - proof of concept for Python writing to USB serial port.

"""

import serial

import logging as log
log.basicConfig(level=log.DEBUG, format="%(asctime)s %(levelname)-8s %(message)s")

COM_PORT = "COM30"

def main():
    ser = serial.Serial(COM_PORT, timeout=0.5)
    log.info(f"Serial port opened: {ser.name}, {ser.baudrate}, {ser.bytesize}, {ser.parity}, {ser.timeout}")
    ser.write(b"hello")
    timed_out = False
    while not timed_out:
        response = ser.read(16)
        log.debug(response)
        if len(response) < 16:
            timed_out = True
    ser.close()
    log.info("Done.")

if __name__ == "__main__":
    main()

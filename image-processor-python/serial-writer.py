"""
serial-writer.py - proof of concept for Python writing to USB serial port.

"""
import time

import serial

import logging as log
log.basicConfig(level=log.DEBUG, format="%(asctime)s %(levelname)-8s %(message)s")

COM_PORT = "COM30"
BUFFER_LENGTH = 16
SLEEP_INTERVAL = 0.05

def main():
    ser = serial.Serial(COM_PORT, timeout=0.5)
    log.info(f"Serial port opened: {ser.name}, {ser.baudrate}, {ser.bytesize}, {ser.parity}, {ser.timeout}")
    ser.write(b"hello")
    timed_out = False
    while True:
        response = ser.read(BUFFER_LENGTH)
        log.debug(response)
        if len(response) < BUFFER_LENGTH:
            try:
                time.sleep(SLEEP_INTERVAL)
            except KeyboardInterrupt:
                log.debug("Interrupted.")
                break
    ser.close()
    log.info("Done.")

if __name__ == "__main__":
    main()

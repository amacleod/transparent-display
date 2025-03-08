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
READ_TIMEOUT = 0.5

def main():
    ser = serial.Serial(COM_PORT, timeout=READ_TIMEOUT)
    log.info(f"Serial port opened: {ser.name}, {ser.baudrate}, {ser.bytesize}, {ser.parity}, {ser.timeout}")
    bytes_to_write = b"hello"
    while True:
        try:
            log.debug(f"Writing '{bytes_to_write}'")
            write_result = ser.write(bytes_to_write)
            log.debug(f"Write result: {write_result}")
            response = ser.read(BUFFER_LENGTH)
            log.debug(response)
            if len(response) < BUFFER_LENGTH:
                time.sleep(SLEEP_INTERVAL)
            if bytes_to_write == b"hello":
                bytes_to_write = b"later"
            else:
                bytes_to_write = b"hello"
        except KeyboardInterrupt:
            log.debug("Interrupted.")
            break
    ser.close()
    log.info("Done.")

if __name__ == "__main__":
    main()

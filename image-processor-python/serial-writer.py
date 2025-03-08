"""
serial-writer.py - proof of concept for Python writing to USB serial port.

"""

import time
import serial

import logging as log
log.basicConfig(level=log.DEBUG, format="%(asctime)s %(levelname)-8s %(message)s")

COM_PORT = "COM30"
SLEEP_INTERVAL = 1.0
READ_TIMEOUT = 0.5

def main():
    ser = serial.Serial(COM_PORT, timeout=READ_TIMEOUT)
    log.info(f"Serial port opened: {ser.name}, {ser.baudrate}, {ser.bytesize}, {ser.parity}, {ser.timeout}")
    bytes_to_write = b"hello\n"
    ready = False
    while True:
        try:
            response = ser.read_until(b"\r\n")[:-2].decode("utf-8")
            log.debug(f"From Arduino: '{response}'")
            if "ready" in response:
                ready = True
            if ready:
                log.debug(f"Writing: {bytes_to_write}")
                bytes_written = ser.write(bytes_to_write)
                log.debug(f"Wrote {bytes_written} bytes.")
                if bytes_to_write == b"hello\n":
                    bytes_to_write = b"goodbye\n"
                else:
                    bytes_to_write = b"hello\n"
            time.sleep(SLEEP_INTERVAL)
        except KeyboardInterrupt:
            log.debug("Interrupted.")
            break
    ser.close()
    log.info("Done.")

if __name__ == "__main__":
    main()

"""
serial_responder - Call-and-response serial handler for communicating
between Python and an Arduino.

"""
import time

import serial
import logging as log

log.basicConfig(level=log.DEBUG, format="%(asctime)s %(levelname)-8s %(message)s")

class SerialPort(object):
    READ_TIMEOUT = 0.5
    BAUD_RATE = 9600

    def __init__(self, port_name: str, timeout=READ_TIMEOUT, baudrate=BAUD_RATE):
        self.port = serial.Serial(port_name, timeout=timeout, baudrate=baudrate)
        log.debug(f"Serial port opened: {self.port.name}, {self.port.baudrate}, {self.port.bytesize}, {self.port.parity}, {self.port.timeout}")

    def read(self) -> str:
        read_bytes = self.port.read_until(b"\r\n")
        read_string = read_bytes.decode("utf-8")
        response = read_string.strip()
        log.debug(f"Received on serial: '{response}'")
        return response

    def write(self, message: bytes) -> int:
        return self.port.write(message)

    def close(self):
        self.port.close()


class SerialResponder(object):
    POLLING_INTERVAL = 0.01

    def __init__(self, port: SerialPort, polling_interval=POLLING_INTERVAL):
        self.port = port
        self.interval = polling_interval

    def main_loop(self):
        log.debug(f"Beginning response loop with {self.interval} second interval.")
        while True:
            try:
                time.sleep(self.interval)
            except KeyboardInterrupt:
                break
        log.debug("Done.")

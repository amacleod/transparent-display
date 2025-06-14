"""
serial_responder - Call-and-response serial handler for communicating
between Python and an Arduino.

"""
import time

import serial
import logging as log

# log.basicConfig(level=log.DEBUG, format="%(asctime)s %(levelname)-8s %(message)s")

class SerialPort(object):
    READ_TIMEOUT = 10.0
    BAUD_RATE = 115200

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


class CommandHandler(object):
    def __init__(self):
        self.empty = bytes()
        from python_image_processor import image_converter
        self.ellipse = image_converter.bytes_from_file("data/Ellipse128x56.png")

    def handle(self, message: str) -> bytes:
        """
        Handle a command from the connected device. If the command
        should produce a response, return that response as bytes.

        :param message:
        :return:
        """
        if len(message) > 0:
            log.info(f"Command received: {message}")
            if "FRAME" in message:
                return self.ellipse
        return self.empty


class VideoReceiver(object):
    pass


class SerialResponder(object):
    POLLING_INTERVAL = 0.01

    def __init__(self, port: SerialPort, handler: CommandHandler = None, polling_interval=POLLING_INTERVAL):
        self.port = port
        self.handler = handler
        if self.handler is None:
            self.handler = CommandHandler()
        self.interval = polling_interval

    def main_loop(self):
        log.info(f"Beginning response loop with {self.interval} second interval.")
        while True:
            try:
                time.sleep(self.interval)
            except KeyboardInterrupt:
                break
        log.info("Done.")

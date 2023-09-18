import logging
import time

import serial


class Arduino:
    def __init__(self, port, timeout):
        self.serial = None
        self.port = port
        self.timeout = timeout
        self.connect()

    def connect(self):
        self.serial = serial.Serial(port=self.port, timeout=self.timeout)
        time.sleep(0.1)

    def on_message(self, message):
        data_str = message.strip()

        full_topic, data_value = data_str.split("=")
        full_topic_parts = full_topic.split("/")

        serial_type = full_topic_parts[0]
        data_type = full_topic_parts[1] if len(full_topic_parts) > 1 else None

        if serial_type == "serial-handshake":
            outcome = f"serial-handshake={data_value}".encode()
            logging.info(f"Incoming handshake. Validating back [{outcome}]")
            self.serial.write(outcome)
        elif serial_type == "serial-data":
            self.serial.write("serial-data=OK".encode())
            return [data_type, data_value]
        return None

import logging
import time

import paho.mqtt.client as mqtt
from paho.mqtt.client import ssl

from param import CLIENT_TIMEOUT, CLIENT_MESSAGE_TIMEOUT, CLIENT_ROOM_ID


class ClientService:
    __client = mqtt.Client()
    __topic = f"room-data/{CLIENT_ROOM_ID}/"

    def __init__(self):
        """
        Initialize the ClientService object.

        This method initializes the MQTT client, sets the username and password, sets the TLS parameters,
        connects to the MQTT broker, and starts the client loop. It also checks if the connection is
        established within a specified timeout duration.

        :raises Exception: If the MQTT connection timeout occurs.

        """

        # Initialize MQTT client
        logging.info("ICI ?")
        self.__client.username_pw_set("guest", "zK&hjVQhiPrwAu6F")
        self.__client.tls_set(certfile=None, keyfile=None, cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLS)
        self.__client.connect("mqtt.freezlex.dev", 1883)
        self.__client.loop_start()

        start_time = time.time()
        while not self.__client.is_connected() and time.time() - start_time < CLIENT_TIMEOUT:
            pass

        if self.__client.is_connected():
            logging.info("MQTT client connected")
        else:
            raise Exception("MQTT connection timeout")

    def send_date(self, endpoint, data):
        """
        Sends the given data to the MQTT broker.

        :param endpoint: the endpoint
        :param data: The data to be sent.
        :return: None
        :raises Exception: If the MQTT message timeout occurs.
        """
        message = self.__client.publish(self.__topic + endpoint, data)
        message.wait_for_publish(CLIENT_MESSAGE_TIMEOUT)

        # logging.info(f"Data sent successfully, topic: {self.__topic + endpoint}")

    def disconnect(self):
        """
        Disconnects the client from the MQTT broker.

        :return: None
        """
        self.__client.disconnect()

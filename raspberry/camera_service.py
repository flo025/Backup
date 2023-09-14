import base64
import logging
import time

import cv2

from param import CAMERA_IMAGE_RATIO, CAMERA_IMAGE_HEIGHT, CAMERA_WAIT


class CameraService:
    __camera = cv2.VideoCapture(0)

    def __init__(self):
        self.__camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_IMAGE_HEIGHT * CAMERA_IMAGE_RATIO)
        self.__camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_IMAGE_HEIGHT)
        self.__camera.set(cv2.CAP_PROP_BRIGHTNESS, 80)
        self.__camera.set(cv2.CAP_PROP_CONTRAST, 1)
        self.__camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)

        logging.info("Camera initialized")

    def disconnect(self):
        """
        Disconnects the client from the MQTT broker.

        :return: None
        """
        self.__camera.release()

    def capture_image(self):
        """
        Method to capture an image from the camera.

        :return: A base64 encoded string representing the captured image in JPEG format.
        :raise Exception: If camera fails to capture an image.
        """
        capture_time = time.time()

        ret, frame = self.__camera.read()

        while time.time() - capture_time < CAMERA_WAIT:
            ret, frame = self.__camera.read()
            pass

        if not ret:
            raise Exception("Camera fail")

        retval, buffer = cv2.imencode('.jpg', frame)
        return base64.b64encode(buffer)

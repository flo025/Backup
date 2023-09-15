import base64
import logging
import time

import cv2

from param import CAMERA_IMAGE_RATIO, CAMERA_IMAGE_HEIGHT, CAMERA_WAIT, CAMERA_BRIGHTNESS


class CameraService:
    __camera = cv2.VideoCapture(0)

    def __init__(self):
        self.__camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_IMAGE_HEIGHT * CAMERA_IMAGE_RATIO)
        self.__camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_IMAGE_HEIGHT)
        # CAP_PROP_POS_MSEC
        # CAP_PROP_MODE
        self.__camera.set(cv2.CAP_PROP_BRIGHTNESS, CAMERA_BRIGHTNESS)
        self.__camera.set(cv2.CAP_PROP_CONTRAST, 0.0)
        self.__camera.set(cv2.CAP_PROP_SATURATION, 100.0)
        self.__camera.set(cv2.CAP_PROP_ZOOM, 0.0)

        logging.info(f"CAP_PROP_FRAME_WIDTH {self.__camera.get(cv2.CAP_PROP_FRAME_WIDTH)}")
        logging.info(f"CAP_PROP_FRAME_HEIGHT {self.__camera.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
        logging.info(f"CAP_PROP_BRIGHTNESS {self.__camera.get(cv2.CAP_PROP_BRIGHTNESS)}")
        logging.info(f"CAP_PROP_CONTRAST {self.__camera.get(cv2.CAP_PROP_CONTRAST)}")
        logging.info(f"CAP_PROP_SATURATION {self.__camera.get(cv2.CAP_PROP_SATURATION)}")

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

import logging

from camera_service import CameraService
from client_service import ClientService

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

try:
    client_service = ClientService()
    camera_service = CameraService()

    base64_image = camera_service.capture_image()
    client_service.send_date('image', base64_image)

    client_service.disconnect()
    camera_service.disconnect()
except Exception as e:
    logging.error(e)

import socket

hostname = socket.gethostname()

CLIENT_ROOM_ID = "UNKNOWN"
CLIENT_TIMEOUT = 5
CLIENT_MESSAGE_TIMEOUT = 5

CAMERA_IMAGE_RATIO = 16 / 9
CAMERA_IMAGE_HEIGHT = 360
CAMERA_WAIT = 5
CAMERA_BRIGHTNESS = 80

if hostname == "pi39":
    CLIENT_ROOM_ID = "508d660b-7e59-475c-934b-de6aae7cecdc"
    CAMERA_BRIGHTNESS = 30
elif hostname == "pi43":
    CLIENT_ROOM_ID = "7c546cd9-4aa5-4ce9-b19e-b5029c87c49e"
    CAMERA_BRIGHTNESS = 115
elif hostname == "piadmin":
    CLIENT_ROOM_ID = "f62888bc-50db-4254-86cf-ec731c2fe4e9"
    CAMERA_BRIGHTNESS = 110

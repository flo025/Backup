import cv2, base64, time

camera: cv2.VideoCapture=None

def init() :
    image_ratio = 16/9
    image_height=360

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, image_height * image_ratio)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, image_height)
    camera.set(cv2.CAP_PROP_BRIGHTNESS, 80)
    camera.set(cv2.CAP_PROP_CONTRAST, 1)
    camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # turn the autofocus off

    return camera

def get_base64_capture()-> bytes:
    if camera==None:
        raise Exception("Camera object must be initilized first before capturing images.")
    camera.read() # Trigger camera to make focus
    time.sleep(1)
    ret, frame = camera.read()

    if not ret:
        raise Exception("Camera capture failed")
    
    return base64.b64encode(cv2.imencode('.jpg', frame)[1].tobytes())
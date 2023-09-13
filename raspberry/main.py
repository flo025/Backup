import serial, time, re, os, mqtt_service, asyncio, camera_service, multiprocessing
from dotenv import load_dotenv

ev=None


def manage_serial_handshake(data, arduino):
    outcome = f"serial-handshake={data}".encode()
    print(f"Incoming handshake. Validating back [{outcome}]")
    arduino.write(outcome)


def manage_serial_data(topic, data, arduino):
    arduino.write("serial-data=OK".encode())
    mqtt_service.send_data(("room-data", "7c546cd9-4aa5-4ce9-b19e-b5029c87c49e", topic), data)


def manage_serial_debug(payload, arduino):
    send_mqtt_debug(payload)

def send_mqtt_debug(payload):
    mqtt_service.send_data(("room-data", "7c546cd9-4aa5-4ce9-b19e-b5029c87c49e", "debug"), payload)

def manage_serial_income(message, arduino):
    matched = re.findall("([A-z-]*)(?:/)?([A-z-]*)?=([A-z0-9]*)", message)
    (topic, subtopic, data) = matched[0]

    if topic == "serial-handshake": manage_serial_handshake(data, arduino)
    elif topic == "serial-data": manage_serial_data(subtopic, data, arduino)
    elif topic == "serial-debug": manage_serial_debug(data, arduino)

def camera_capture():
    byte_data=camera_service.get_base64_capture()
    mqtt_service.send_data(("room-data", "7c546cd9-4aa5-4ce9-b19e-b5029c87c49e", "image"), byte_data)

def serial_listener():
    mqtt_service.client = mqtt_service.init_client(mqtt_service.MqttClient("mqtt.freezlex.dev", "guest", "zK&hjVQhiPrwAu6F", 1883, True, True))

    start_time = time.time()
    while not mqtt_service.client.is_connected() and time.time() - start_time < 5:
        pass

    if not mqtt_service.client.is_connected():
        raise Exception("MQTT Not connected after 5s.")

    connected=False
    loop=True
    arduino=None
    while loop:
        try:
            if connected==False:
                arduino = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
                time.sleep(0.1) # Wait 1s for serial to open
            connected = arduino.isOpen()
            if connected:
                while arduino.inWaiting()==0: pass
                if arduino.inWaiting()>0:
                    income=arduino.readline()
                    manage_serial_income(income.decode("utf-8"), arduino)
                    arduino.flushInput() # Remove data after reading
        except KeyboardInterrupt:
            send_mqtt_debug(f"KeyboardUnterrupt shuting down application.")
            mqtt_service.disconnect_client()
            print("KeyboardInterrupt has been caught.")
            loop=False
        except Exception as e:
            send_mqtt_debug(f"{e}")
            time.sleep(10)

def camera_capture_loop():
    mqtt_service.client = mqtt_service.init_client(mqtt_service.MqttClient("mqtt.freezlex.dev", "guest", "zK&hjVQhiPrwAu6F", 1883, True, True))

    start_time = time.time()
    while not mqtt_service.client.is_connected() and time.time() - start_time < 5:
        pass

    if not mqtt_service.client.is_connected():
        raise Exception("MQTT Not connected after 5s.")

    loop=True
    while loop:    
        try:
            print("Capture image")
            camera_capture()
            time.sleep(10)
        except KeyboardInterrupt:
            send_mqtt_debug(f"KeyboardUnterrupt shuting down application.")
            mqtt_service.disconnect_client()
            print("KeyboardInterrupt has been caught.")
            loop=False
        except Exception as e:
            send_mqtt_debug(f"{e}")

if __name__ == '__main__':
    load_dotenv()
    ev = dict(os.environ)

    camera_service.camera = camera_service.init()

    multiprocessing.Process(target=serial_listener).start()
    multiprocessing.Process(target=camera_capture_loop).start()
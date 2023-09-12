import serial, time, re, os, mqtt_service, asyncio, camera_service
from dotenv import load_dotenv

ev=None


def manage_serial_handshake(data, arduino):
    outcome = ("serial-handshake" + data).encode()
    print("Incoming handshake. Validating back [" + data + "]")
    arduino.write(outcome)


def manage_serial_data(topic, data, arduino):
    print("Data received : [" + topic + ", " + data + "]")
    arduino.write("serial-data=OK".encode())
    mqtt_service.send_data(("room-data", "TEST-ROOM", topic), data)

def manage_serial_debug(payload, arduino):
    print("Debug received : [" + payload + "]")
    send_mqtt_debug(payload)

def send_mqtt_debug(payload):
    mqtt_service.send_data(("room-data", "TEST-ROOM", "debug"), payload)

def manage_serial_income(message, arduino, mqttClient):
    matched = re.findAll("([A-z-]*)(?:/)?([A-z-]*)?=([A-z0-9]", message)
    (topic, subtopic, data) = matched[0]

    if topic == "serial-handshake": manage_serial_handshake(data, arduino)
    elif topic == "serial-data": manage_serial_data(subtopic, data, arduino, mqttClient)
    elif topic == "serial-debug": manage_serial_debug(data, arduino, mqttClient)

async def camera_capture():
    byte_data=await camera_service.get_base64_capture()
    mqtt_service.send_data(("room-data", "TEST-ROOM", "image"), byte_data)

async def main():
    load_dotenv()
    ev = dict(os.environ)

    await camera_service.init()

    await mqtt_service.init_client(mqtt_service.MqttClient("mqtt.freezlex.dev", "guest", "zK&hjVQhiPrwAu6F", 1883, True, True))

    connected=False
    loop=True
    arduino=None
    time_buffer=time.time()
    while loop:
        try:
            if connected==False:
                arduino = await serial.Serial("/dev/ttyACM0", 9600, timeout=1)
                time.sleep(0.1) # Wait 1s for serial to open
            connected = arduino.isOpen()
            if connected:
                while arduino.inWaiting()==0: pass
                if arduino.inWaiting()>0:
                    income=await arduino.readline()
                    manage_serial_income(income.decode("utf-8"), arduino)
                    arduino.flushInput() # Remove data after reading

            if time.time() - time_buffer > 5:
                camera_capture()
                time_buffer=time.time()
        except KeyboardInterrupt:
            await send_mqtt_debug(f"KeyboardUnterrupt shuting down application.")
            mqtt_service.disconnect_client()
            print("KeyboardInterrupt has been caught.")
            loop=False
        except Exception as e:
            send_mqtt_debug(f"Arduino disconnected, await 10s before new attempt.")
            time.sleep(10)

if __name__ == '__main__':
    asyncio.run(main())
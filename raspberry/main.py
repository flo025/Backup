import serial, time, re, random, string
import paho.mqtt.client as mqttc

def manageSerialHandshake(data, arduino):
    outcome = ("serial-handshake" + data).encode()
    print("Incoming handshake. Validating back [" + data + "]")
    arduino.write(outcome)


def manageSerialData(topic, data, arduino, mqttClient):
    print("Data received : [" + topic + ", " + data + "]")
    arduino.write("serial-data=OK".encode())
    mqttClient.publish("room-data/TEST/" + topic, data)

def manageSerialDebug(payload, arduino, mqttClient):
    print("Debug received : [" + payload + "]")
    mqttClient.publish("room-data/TEST/debug", payload)

def manageIncomingMessage(message, arduino, mqttClient):
    matched = re.findAll("([A-z-]*)(?:/)?([A-z-]*)?=([A-z0-9]", message)
    (topic, subtopic, data) = matched[0]

    if topic == "serial-handshake": manageSerialHandshake(data, arduino)
    elif topic == "serial-data": manageSerialData(subtopic, data, arduino, mqttClient)
    elif topic == "serial-debug": manageSerialDebug(data, arduino, mqttClient)

def mqttOnConnect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def mqttOnPublish(mqttc, obj, mid):
    print("mid: " + str(mid))

def mqttOnSubscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def connectToMqttBroker():
    random_cid = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
    mqtt = mqttc.Client(("rpiuhapj-" + random_cid), True, reconnect_on_failure=True, userdata=None)
    mqtt.on_connect=mqttOnConnect
    mqtt.on_publish=mqttOnPublish
    mqtt.on_subscribe=mqttOnSubscribe
    
    mqtt.tls_insecure_set(True)
    mqtt.connect("mqtt.freezlex.dev", 1883, 15)

    return mqtt

if __name__ == '__main__':
    mqttClient=connectToMqttBroker()
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
                    manageIncomingMessage(income.decode("utf-8"), arduinon, mqttClient)
                    arduino.flushInput() # Remove data after reading
        except KeyboardInterrupt:
            print("KeyboardInterrupt has been caught.")
            loop=False
        except:
            print("Arduino disconnected. Await 10s for it to be reconnected.")
            time.sleep(10)
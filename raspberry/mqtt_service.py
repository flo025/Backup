import paho.mqtt.client as mqtt
import ssl, random, string

class MqttClient:
    broker_url: str
    port: int
    user: str
    password: str
    use_ssl: bool
    ignore_ssl_errors: bool


    def __init__(self, broker_url: str, user: str, password: str, port: int = 1883, use_ssl: bool = True, ignore_ssl_erros: bool = False) -> None:
        self.broker_url = broker_url
        self.user = user
        self.password = password
        self.port = port
        self.use_ssl = use_ssl
        self.ignore_ssl_errors = ignore_ssl_erros


client: mqtt.Client=None

def on_client_connected(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_client_connect_fail(client, userdata, flags, rc):
    print(client, userdata, flags, rc)

def init_client(service_client: MqttClient) -> mqtt.Client:
    client = mqtt.Client(client_id=f"iot-rpi-{''.join(random.choice(string.ascii_letters) for i in range(8))}")
    client.username_pw_set(service_client.user, service_client.password)
    client.tls_set(certfile=None, keyfile=None, cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLS)
    client.connect(service_client.broker_url, service_client.port)

    client.on_connect=on_client_connected
    client.on_connect_fail=on_client_connect_fail

    client.loop_start()

    return client

def send_data(topics: tuple[str], data) -> bool:
    try :
        if not client.is_connected():
            print(f"MQTT broker not connected. MQTT_DATA_NOT_SENT [{'/'.join(topics)}, {data}]")
            return False
        client.publish('/'.join(topics), data)
        return True
    except Exception as e:
        print(f'Unable to send data to MQTT. ERROR:{str(e)}')
        return False


def disconnect_client():
    client.disconnect()
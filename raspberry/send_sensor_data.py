import datetime
import logging
import sys

from arduino_service import Arduino
from client_service import ClientService

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


try:
    arduino = Arduino("/dev/ttyACM0", 1)
    client_service = ClientService()

    logging.info('test')

    while True:
        current_time = datetime.datetime.now()
        if current_time.hour >= 17 and current_time.minute >= 30:
            logging.info("It's 17:30, exiting the program.")
            client_service.disconnect()
            sys.exit()

        if not arduino.serial.isOpen():
            arduino.connect()
            continue

        while arduino.serial.inWaiting() == 0:
            pass

        data = arduino.on_message(arduino.serial.readline().decode('utf-8'))
        if data is not None:
            client_service.send_date(data[0], int(float(data[1])))

except Exception as e:
    logging.error(e)

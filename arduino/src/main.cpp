#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define KY001_Signal_PIN 4

#pragma region func_def

#pragma region lib_def
OneWire oneWire(KY001_Signal_PIN);
DallasTemperature sensors(&oneWire);
#pragma endregion

int temperatureSensor = A0;

int uartConnect(int, bool);

bool sendData(String, double);

bool sendUART(String, String);

void sensorsInit();

String gen_random(int);
#pragma endregion

void setup() {
  uartConnect(5000, true);
  sensorsInit();
}

void loop() {
  sensors.requestTemperatures();
  double temp = sensors.getTempCByIndex(0);
  sendData("temperature", temp);

  double sound = analogRead(0);
  sendData("noise", sound);
  
  delay(1000);
}

int uartConnect(int timeout, bool retry) {
  bool uartStatus = false;
  String uid = gen_random(8);
  String handshake = "serial-handshake=" + uid;
  Serial.begin(9600);
  Serial.setTimeout(timeout);
  do
  {
    Serial.println(handshake);
  
    uartStatus = Serial.find(handshake.c_str());
    if(uartStatus) break;

  } while (retry && !uartStatus);
}

// sendUART("debug", "...")

bool sendData(String topic, double value) {
  topic = "serial-data/" + topic;
  return sendUART(topic, String(value, 4));
}

bool sendUART(String topic, String payload) {
  bool dataReceived = false;
  for(int i=0; i < 2; i++) {
    if(Serial) {
      String output = topic + "=";
      output.concat(payload);

      Serial.println(output);
      
      dataReceived = Serial.find("serial-data=OK");

      if(dataReceived) return true;

      for(int t=0; t < 3; t++) {
        uartConnect(5000, false);
      }
    }
  }
  return false;
}

String gen_random(int len) {
    static const char alphanum[] =
        "0123456789"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz";
    String tmp_s;
    tmp_s.reserve(len);

    for (int i = 0; i < len; ++i) {
        tmp_s += alphanum[rand() % (sizeof(alphanum) - 1)];
    }
    
    return tmp_s;
}

void sensorsInit() {
  analogReference(DEFAULT);
  sensors.begin();
}
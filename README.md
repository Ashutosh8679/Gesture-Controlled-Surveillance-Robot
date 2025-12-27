# Gesture-Controlled-Surveillance-Robot
A gesture controlled Survaillance bot using the following
  1. esp32 dev module
  2. esp32 cam
  3. DRV8833
  4. 4xBO motors (also runs on 2xBO motors)
  5. 6+ Volt DC source

The bot has an ESP32 dev module which hosts the Access Point(AP). The ESP32 Cam and client/control device connects to the AP. 
The default 
    SSID: "ESP32_Car"
     PASS: "12345678"
Please change this in the ESP32 dev module code if you want additional security.

The control pins for the esp32 dev module are:
    For Right Motor: 25 and 26
    For Left Motor: 27 and 14
Please refer to the circuit diagram if you have doubts.

The client code is to be run on python, you will need the following libararies:
    1. opencv
    2. mediapipe
    3. socket
    4. threading
    5. time
    6. numpy
  The client device MUST be connected to the AP created by the ESP32 dev module. 

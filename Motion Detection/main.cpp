#include "mbed.h"

// PIR connected to D2
DigitalIn pirSensor(D7);

// USB serial output
UnbufferedSerial pc(USBTX, USBRX, 115200);

int main() {

    while (1) {
        // check the pirSensor value: if 1 then send a flag MOTION to serial port
        if (pirSensor.read() == 1) {
            pc.write("MOTION\n", 7);
            ThisThread::sleep_for(20s);
        }
        ThisThread::sleep_for(500ms);
    }
}

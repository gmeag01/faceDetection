#include <Servo.h>

// 서보모터
Servo servoBase;
Servo servoTop;
char servoBasePosition = 90;
char servoTopPosition = 90;

// pc -> 아두이노 변수 설정
int myCoor[4];
byte* ddata = reinterpret_cast<byte*>(&myCoor); // pointer for transferData()
size_t pcDataLen = sizeof(myCoor);
bool newData = false;

// 아두이노 변수 설정
int rate = 14400;
int base = 3;
int top = 6;

// 목표 좌표
int targetX = 320; 
int targetY = 240;
int mid = 20;


// 모터 이동값
int stepsize = 1;

void setup() {
	Serial.begin(rate);
    servoBase.attach(base);
    servoTop.attach(top);
    servoBase.write(servoBasePosition);
    servoTop.write(servoTopPosition);
}

void loop() {
    checkForNewData();
    if (newData == true) {
        // Print coordinate for serial bus test
        // Serial.print(". coordinate :  ");
        // Serial.print(myCoor[0]);
        // Serial.print(" ");
        // Serial.println(myCoor[2]);
        controlServo(myCoor[0], myCoor[2]);
        newData = false;
    }

}

void checkForNewData() {
    if (Serial.available() >= pcDataLen && newData == false) {
        byte inByte;
        for (byte n = 0; n < pcDataLen; n++) {
            ddata [n] = Serial.read();
        }
        while (Serial.available()) {
            byte dumpByte =  Serial.read();
        }
        newData = true;
    }
}

void controlServo(int x, int y) {   
    if (x > (targetX + mid)) {
            if (servoBasePosition >= 5) {
                servoBasePosition -= stepsize;
        }
    }
    else if (x < (targetX - mid)) {
        if (servoBasePosition <= 175) {
            servoBasePosition += stepsize;
        }
    }

    if (y < (targetY - mid)) {
            if (servoTopPosition >= 5) {
                servoTopPosition -= stepsize;
        }
    }
    else if (y > (targetY + mid)) {
        if (servoTopPosition <= 175) {
            servoTopPosition += stepsize;
        }
    }
    servoBase.write(servoBasePosition);
    servoTop.write(servoTopPosition);
}


import time

import cv2
import serial

ser = serial.Serial('COM9', 115200)   # set correct COM port

while True:
    data = ser.readline().decode().strip()


    if data == "MOTION":
        print("Motion Detected — Recording video for 10 seconds")

        cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter("intruder.mp4", fourcc, 20.0, (640,480))

        start = time.time()

        while time.time() - start < 10:
            ret, frame = cap.read()
            out.write(frame)

        cap.release()
        out.release()
        print("Recording Saved")

    print("No motion Detected")
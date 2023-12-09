import torch
import matplotlib.pyplot as plt
import numpy as np
import cv2
import uuid
import os
import time
import RPi.GPIO as GPIO          
from time import sleep
# import keyboard

# Motor 1 configuration
en_motor1 = 18
in1_motor1 = 23
in2_motor1 = 24

# Motor 2 configuration
en_motor2 = 12
in1_motor2 = 20
in2_motor2 = 16

# Ultrasonic sensor configuration
trig_pin = 17
echo_pin = 27

direction = 1

GPIO.setmode(GPIO.BCM)

# Motor 1 setup
GPIO.setup(in1_motor1, GPIO.OUT)   # Set GPIO pin for input 1 of Motor 1 as an output
GPIO.setup(in2_motor1, GPIO.OUT)   # Set GPIO pin for input 2 of Motor 1 as an output
GPIO.setup(en_motor1, GPIO.OUT)    # Set GPIO pin for enable of Motor 1 as an output

GPIO.output(in1_motor1, GPIO.LOW)  # Set initial state of input 1 of Motor 1 to LOW (off)
GPIO.output(in2_motor1, GPIO.LOW)  # Set initial state of input 2 of Motor 1 to LOW (off)

# Create a PWM (Pulse Width Modulation) object for Motor 1
p_motor1 = GPIO.PWM(en_motor1, 1000)  # Create a PWM object for Motor 1 with a frequency of 1000 Hz
p_motor1.start(35)  # Start PWM for Motor 1 with an initial duty cycle of 25%


# Motor 2 setup
GPIO.setup(in1_motor2, GPIO.OUT)   # Set GPIO pin for input 1 of Motor 2 as an output
GPIO.setup(in2_motor2, GPIO.OUT)   # Set GPIO pin for input 2 of Motor 2 as an output
GPIO.setup(en_motor2, GPIO.OUT)    # Set GPIO pin for enable of Motor 2 as an output

GPIO.output(in1_motor2, GPIO.LOW)  # Set initial state of input 1 of Motor 2 to LOW (off)
GPIO.output(in2_motor2, GPIO.LOW)  # Set initial state of input 2 of Motor 2 to LOW (off)

# Create a PWM (Pulse Width Modulation) object for Motor 2
p_motor2 = GPIO.PWM(en_motor2, 1000)  # Create a PWM object for Motor 2 with a frequency of 1000 Hz
p_motor2.start(35)  # Start PWM for Motor 1 with an initial duty cycle of 25%


# Ultrasonic sensor setup
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

def get_distance():
    # Trigger ultrasonic sensor
    GPIO.output(trig_pin, True)
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)

    # Wait for echo pin to go high (start of pulse)
    while GPIO.input(echo_pin) == 0:
        pulse_start_time = time.time()

    # Wait for echo pin to go low (end of pulse)
    while GPIO.input(echo_pin) == 1:
        pulse_end_time = time.time()

    # Calculate distance
    pulse_duration = pulse_end_time - pulse_start_time
    distance = pulse_duration * 17150  # Speed of sound is approximately 343 meters per second
    distance = round(distance, 2)

    return distance

def forward():
    GPIO.output(in1_motor1, GPIO.HIGH)
    GPIO.output(in2_motor1, GPIO.LOW)
    GPIO.output(in1_motor2, GPIO.HIGH)
    GPIO.output(in2_motor2, GPIO.LOW)
    global direction
    direction = 1
    medium()
    print("forward")

def backward():
    GPIO.output(in1_motor1, GPIO.LOW)
    GPIO.output(in2_motor1, GPIO.HIGH)
    GPIO.output(in1_motor2, GPIO.LOW)
    GPIO.output(in2_motor2, GPIO.HIGH)
    global direction
    direction = 0
    medium()
    print("backward")

def right_turn():
    high()
    GPIO.output(in1_motor1, GPIO.LOW)
    GPIO.output(in2_motor1, GPIO.HIGH)
    GPIO.output(in1_motor2, GPIO.HIGH)
    GPIO.output(in2_motor2, GPIO.LOW)
    sleep(0.5)
    print("Right turn")
    forward()

def left_turn():
    high()
    GPIO.output(in1_motor1, GPIO.HIGH)
    GPIO.output(in2_motor1, GPIO.LOW)
    GPIO.output(in1_motor2, GPIO.LOW)
    GPIO.output(in2_motor2, GPIO.HIGH)
    sleep(0.5)
    print("Left turn")
    forward()

def stop():
    GPIO.output(in1_motor1, GPIO.LOW)
    GPIO.output(in2_motor1, GPIO.LOW)
    GPIO.output(in1_motor2, GPIO.LOW)
    GPIO.output(in2_motor2, GPIO.LOW)
    print("Stopped")

def low():
    print("low")
    p_motor1.ChangeDutyCycle(25)
    p_motor2.ChangeDutyCycle(25)

def medium():
    print("medium")
    p_motor1.ChangeDutyCycle(50)
    p_motor2.ChangeDutyCycle(50)

def high():
    print("high")
    p_motor1.ChangeDutyCycle(75)
    p_motor2.ChangeDutyCycle(75)


# Load the pre-trained Haar Cascade face classifier which can be changed
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

forward()

# Function for face detection and robot movement
def detect_and_move(frame):
    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

     # Draw bounding boxes around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 127, 255), 2)

    # Check for obstacles using ultrasonic sensor
    obstacle_distance = get_distance()
    print(f"Obstacle distance: {obstacle_distance} cm")
    
    # Check if faces are detected
    if len(faces) > 0 and obstacle_distance < 20:  # Adjust this threshold based on your robot's capabilities:
        stop()  # Stop both motors
        sleep(2)  # Pause for 2 seconds
        right_turn()  # Example: Turn right when a face is detected

    return frame

# Video capture and robot movement loop
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    # Perform face detection and move the robot
    processed_frame = detect_and_move(frame)

    # Display the processed frame
    cv2.imshow('Face Detection', processed_frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        GPIO.cleanup()
        break

cap.release()
cv2.destroyAllWindows()
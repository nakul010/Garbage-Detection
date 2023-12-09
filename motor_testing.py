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
p_motor1.start(25)  # Start PWM for Motor 1 with an initial duty cycle of 25%


# Motor 2 setup
GPIO.setup(in1_motor2, GPIO.OUT)   # Set GPIO pin for input 1 of Motor 2 as an output
GPIO.setup(in2_motor2, GPIO.OUT)   # Set GPIO pin for input 2 of Motor 2 as an output
GPIO.setup(en_motor2, GPIO.OUT)    # Set GPIO pin for enable of Motor 2 as an output

GPIO.output(in1_motor2, GPIO.LOW)  # Set initial state of input 1 of Motor 2 to LOW (off)
GPIO.output(in2_motor2, GPIO.LOW)  # Set initial state of input 2 of Motor 2 to LOW (off)

# Create a PWM (Pulse Width Modulation) object for Motor 2
p_motor2 = GPIO.PWM(en_motor2, 1000)  # Create a PWM object for Motor 2 with a frequency of 1000 Hz
p_motor2.start(25)  # Start PWM for Motor 1 with an initial duty cycle of 25%


def forward():
    GPIO.output(in1_motor1, GPIO.HIGH)
    GPIO.output(in2_motor1, GPIO.LOW)
    GPIO.output(in1_motor2, GPIO.HIGH)
    GPIO.output(in2_motor2, GPIO.LOW)
    global direction
    direction = 1
    print("forward")

def backward():
    GPIO.output(in1_motor1, GPIO.LOW)
    GPIO.output(in2_motor1, GPIO.HIGH)
    GPIO.output(in1_motor2, GPIO.LOW)
    GPIO.output(in2_motor2, GPIO.HIGH)
    global direction
    direction = 0
    print("backward")

def right_turn():
    medium()
    GPIO.output(in1_motor1, GPIO.LOW)
    GPIO.output(in2_motor1, GPIO.HIGH)
    GPIO.output(in1_motor2, GPIO.HIGH)
    GPIO.output(in2_motor2, GPIO.LOW)
    sleep(1)
    print("Right turn")
    forward()

def left_turn():
    medium()
    GPIO.output(in1_motor1, GPIO.HIGH)
    GPIO.output(in2_motor1, GPIO.LOW)
    GPIO.output(in1_motor2, GPIO.LOW)
    GPIO.output(in2_motor2, GPIO.HIGH)
    sleep(1)
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
    

print("The default speed & direction is LOW & Forward")
print(" r-run\n s-stop\n f-forward\n b-backward\n le-left\n ri-right\n l-low\n m-medium\n h-high\n e-exit")
print("\n")

while True:
    x = input()
    
    if x == 'r':
        print("Run")
        if direction == 1:
            forward()
        else:
            backward()

    elif x == 's':
        stop()
    
    elif x == 'f':
        forward()
    
    elif x == 'b':
        backward()
    
    elif x == 'le':
        left_turn()

    elif x == 'ri':
        right_turn()

    elif x == 'l':
        low()
    
    elif x == 'm':
        medium()
    
    elif x == 'h':
        high()
    
    elif x == 'e':
        stop()
        print("exit")
        GPIO.cleanup()
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")


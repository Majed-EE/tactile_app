#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 16:31:29 2026

@author: user
"""

import time
import sys
import select
import termios
import tty
import Jetson.GPIO as GPIO

# Motor control pins (using BOARD pin numbering)
motor2pin1 = 38  # GPIO 38 (Pin 38)
motor2pin2 = 37  # GPIO 37 (Pin 37)
motor1pin1 = 36  # GPIO 36 (Pin 36)
motor1pin2 = 35  # GPIO 35 (Pin 35)

# Enable pins (PWM)
ENA = 32   # GPIO 2 (Pin 3)
ENB = 33   # GPIO 3 (Pin 5)

# Setup GPIO
GPIO.setmode(GPIO.BOARD)  # Use BOARD pin numbering

# Setup pins as output
GPIO.setup([motor1pin1, motor1pin2, motor2pin1, motor2pin2], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup([ENA, ENB], GPIO.OUT, initial=GPIO.HIGH)

# Create PWM objects for speed control (1000 Hz frequency)
pwm_a = GPIO.PWM(ENA, 1000)  # 1000 Hz frequency
pwm_b = GPIO.PWM(ENB, 1000)

# Start PWM with 60% duty cycle (equivalent to analogWrite(ENA, 150) for 0-255 range)
pwm_a.start(60)  # 60% duty cycle
pwm_b.start(60)  # 60% duty cycle

print("Use W A S D keys to control the motors. Press 'q' to quit.")

def stop_motors():
    print("Stop")
    GPIO.output(motor1pin1, GPIO.LOW)
    GPIO.output(motor1pin2, GPIO.LOW)
    GPIO.output(motor2pin1, GPIO.LOW)
    GPIO.output(motor2pin2, GPIO.LOW)

def forward():
    print("Forward")
    
    GPIO.output(motor1pin1, GPIO.HIGH) # 36
    GPIO.output(motor1pin2, GPIO.LOW) # 35
    GPIO.output(motor2pin1, GPIO.HIGH) # 38
    GPIO.output(motor2pin2, GPIO.LOW) # 37

def backward():
    print("Backward")
    GPIO.output(motor1pin1, GPIO.LOW) # 36
    GPIO.output(motor1pin2, GPIO.HIGH) # 35
    GPIO.output(motor2pin1, GPIO.LOW) #38
    GPIO.output(motor2pin2, GPIO.HIGH) #37

def right():
    print("right")
    GPIO.output(motor1pin1, GPIO.LOW)   # left motor stop
    GPIO.output(motor1pin2, GPIO.LOW)
    GPIO.output(motor2pin1, GPIO.HIGH)  # right motor forward
    GPIO.output(motor2pin2, GPIO.LOW)

def left():
    print("Left")
    GPIO.output(motor1pin1, GPIO.HIGH)  # left motor forward
    GPIO.output(motor1pin2, GPIO.LOW)
    GPIO.output(motor2pin1, GPIO.LOW)   # right motor stop
    GPIO.output(motor2pin2, GPIO.LOW)

def get_key():
    """Get a single key press without waiting for Enter"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key

try:
    while True:
        key = get_key()
        if key:
            if key.lower() == 'q':
                break
                
            if key.lower() == 'w':
                forward()
            elif key.lower() == 's':
                backward()
            elif key.lower() == 'a':
                left()
            elif key.lower() == 'd':
                right()
            else:
                stop_motors()
            
            # Wait a bit for the command to execute
            time.sleep(0.1)
            stop_motors()  # Stop after each command (like the Arduino delay)

except KeyboardInterrupt:
    print("\nProgram interrupted")
finally:
    # Cleanup
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
    print("GPIO cleaned up")
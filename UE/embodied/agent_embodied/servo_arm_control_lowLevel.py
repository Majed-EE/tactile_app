#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 12:12:29 2026

@author: user
"""

import time
import serial

# ========== CONFIG ==========
ARDUINO_PORT = "ttyACM0"       # Change if needed
ARDUINO_BAUD = 115200

SERVO_MIN = 0
SERVO_MAX = 180
STEP_DEG = 3               # smoothness
UPDATE_DELAY = 0.04        # ~25 Hz
# ============================


def open_serial():
    while True:
        try:
            ser = serial.Serial(ARDUINO_PORT, ARDUINO_BAUD, timeout=1)
            print(f"Connected to Arduino on {ARDUINO_PORT}")
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            time.sleep(2)  # wait for Arduino reset
            return ser
        except Exception as e:
            print("Serial connection failed:", e)
            time.sleep(2)


def send_servo(ser, servo_id, angle):
    angle = max(SERVO_MIN, min(SERVO_MAX, angle))
    cmd = f"{servo_id} {angle}\n"
    ser.write(cmd.encode())
    print("Sent:", cmd.strip())


def main():
    print("hiiiii")
    ser = open_serial()

    try:
        while True:
            # ============================
            # OPEN → CLOSE
            # ============================
            for angle in range(SERVO_MIN, SERVO_MAX + 1, STEP_DEG):
                send_servo(ser, 0, angle)          # thumb
                send_servo(ser, 1, SERVO_MAX-angle)  # index (opposite)
                time.sleep(UPDATE_DELAY)

            # ============================
            # CLOSE → OPEN
            # ============================
            for angle in range(SERVO_MAX, SERVO_MIN - 1, -STEP_DEG):
                send_servo(ser, 0, angle)
                send_servo(ser, 1, SERVO_MAX-angle)
                time.sleep(UPDATE_DELAY)

    except KeyboardInterrupt:
        print("\nStopping local driver...")

    finally:
        ser.close()
        print("Serial closed")


if __name__ == "__main__":
    
    main()
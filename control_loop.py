import RPi.GPIO as GPIO
import time
import os

# Setup GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)  # Left Motor Forward
GPIO.setup(32, GPIO.OUT)  # Left Motor Backward
GPIO.setup(33, GPIO.OUT)  # Right Motor Forward
GPIO.setup(35, GPIO.OUT)  # Right Motor Backward
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Limit Switch 1
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Limit Switch 2

# Set up PWM for motor speed control
left_pwm_fwd = GPIO.PWM(12, 500)
left_pwm_bwd = GPIO.PWM(32, 500)
right_pwm_fwd = GPIO.PWM(33, 500)
right_pwm_bwd = GPIO.PWM(35, 500)

left_pwm_fwd.start(0)
right_pwm_fwd.start(0)

# Global variables
target_speed = 0
is_running = False  # Indicates if the robot is allowed to move

# Function to read target speed from file


def read_target_speed():
    if not os.path.exists('target_speed.txt'):
        return None  # File does not exist
    with open('target_speed.txt', 'r') as file:
        speed = file.read()
        return int(speed) if speed.isdigit() else None

# Function to control left motor (only forward)


def control_left_motor(speed):
    calibrated_speed = max(0, min(speed * 0.9, 100))  # Apply a 10% calibration
    left_pwm_fwd.ChangeDutyCycle(calibrated_speed)

# Function to control right motor (only forward)


def control_right_motor(speed):
    right_pwm_fwd.ChangeDutyCycle(speed)

# Function to adjust speed based on limit switches


def adjust_speed(target_speed):
    switch1 = GPIO.input(36)
    switch2 = GPIO.input(38)

    if not switch1 and not switch2:
        print("Both limit switches inactive. Stopping motors for safety.")
        return 0  # Stop motors completely
    elif switch1 and switch2:
        return target_speed
    elif switch1 and not switch2:
        return max(target_speed - 10, 0)  # Reduce speed
    elif not switch1 and switch2:
        return min(target_speed + 10, 100)  # Increase speed

# Main control loop


def control_loop():
    global is_running, target_speed

    print("Starting control loop...")
    while True:
        # Wait until is_running is set to True
        if not is_running:
            print("Robot paused. Waiting to start...")
            time.sleep(1)
            continue

        # Read the target speed
        target_speed = read_target_speed()
        if target_speed is None or target_speed <= 0:
            print("Invalid or missing target speed. Waiting for valid input...")
            time.sleep(1)
            continue

        print(f"Target speed: {target_speed}")
        adjusted_speed = adjust_speed(target_speed)

        # Control motors based on adjusted speed
        control_left_motor(adjusted_speed)
        control_right_motor(adjusted_speed)
        time.sleep(0.1)  # Run at a rate of 10 Hz


if __name__ == '__main__':
    try:
        control_loop()
    except KeyboardInterrupt:
        left_pwm_fwd.stop()
        right_pwm_fwd.stop()
        GPIO.cleanup()

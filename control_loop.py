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
left_pwm_bwd.start(0)
right_pwm_fwd.start(0)
right_pwm_bwd.start(0)

# Function to read target speed from file
def read_target_speed():
    if not os.path.exists('target_speed.txt'):
        return None  # File does not exist
    with open('target_speed.txt', 'r') as file:
        speed = file.read()
    return int(speed)

# Function to control left motor (only forward)
def control_left_motor(speed):
    left_pwm_bwd.ChangeDutyCycle(0)  # Ensure backward PWM is off
    left_pwm_fwd.ChangeDutyCycle(speed)  # Set forward PWM to desired speed

# Function to control right motor (only forward)
def control_right_motor(speed):
    right_pwm_bwd.ChangeDutyCycle(0)  # Ensure backward PWM is off
    right_pwm_fwd.ChangeDutyCycle(speed)  # Set forward PWM to desired speed


# Function to adjust speed based on limit switches
def adjust_speed(target_speed):
    switch1 = GPIO.input(36)
    switch2 = GPIO.input(38)

    if not switch1 and not switch2:
        print("Both limit switches inactive. Stopping motors for 5 seconds.")
        control_left_motor(0)
        control_right_motor(0)
        time.sleep(2)
        return 0
    elif switch1 and switch2:
        print(f"Both limit switches active. Moving forward with target speed: {target_speed}")
        return target_speed
    elif switch1 and not switch2:
        print(f"Limit switch 1 active. Moving forward with target speed: {target_speed - 10}")
        return target_speed - 10
    elif not switch1 and switch2:
        print(f"Limit switch 2 active. Moving forward with target speed: {target_speed +  10}")
        return target_speed + 10

# Main control loop
def control_loop():
    print("Starting control loop...")
    while True:
        target_speed = read_target_speed()
        
        if target_speed is None or target_speed <= 0:
            print("Waiting for initial input speed...")
            time.sleep(1)  # Avoid busy waiting
            continue
        
        print(f"Target speed received: {target_speed}")
        adjusted_speed = adjust_speed(target_speed)
        control_left_motor(adjusted_speed)
        control_right_motor(adjusted_speed)
        time.sleep(1)

if __name__ == '__main__':
    try:
        control_loop()
    except KeyboardInterrupt:
        GPIO.cleanup()

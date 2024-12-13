import RPi.GPIO as GPIO
import time

# Setup GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)  # Left Motor Forward
GPIO.setup(32, GPIO.OUT)  # Left Motor Backward
GPIO.setup(33, GPIO.OUT)  # Right Motor Forward
GPIO.setup(35, GPIO.OUT)  # Right Motor Backward
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Limit Switch 1
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Limit Switch 2

# Set up PWM for motor speed control
left_pwm_fwd = GPIO.PWM(12, 500)
left_pwm_bwd = GPIO.PWM(32, 500)
right_pwm_fwd = GPIO.PWM(33, 500)
right_pwm_bwd = GPIO.PWM(35, 500)

left_pwm_fwd.start(0)
left_pwm_bwd.start(0)
right_pwm_fwd.start(0)
right_pwm_bwd.start(0)

# Function to control left motor
def control_left_motor(speed, direction):
    if direction == 1:  # Forward
        left_pwm_bwd.ChangeDutyCycle(0)
        left_pwm_fwd.ChangeDutyCycle(speed)
    elif direction == -1:  # Backward
        left_pwm_fwd.ChangeDutyCycle(0)
        left_pwm_bwd.ChangeDutyCycle(speed)

# Function to control right motor
def control_right_motor(speed, direction):
    if direction == 1:  # Forward
        right_pwm_bwd.ChangeDutyCycle(0)
        right_pwm_fwd.ChangeDutyCycle(speed)
    elif direction == -1:  # Backward
        right_pwm_fwd.ChangeDutyCycle(0)
        right_pwm_bwd.ChangeDutyCycle(speed)

# Function to read limit switches
def read_limit_switches():
    switch1 = GPIO.input(36)
    switch2 = GPIO.input(38)
    return switch1, switch2

# Function to adjust speed based on limit switches
def adjust_speed(target_speed):
    switch1, switch2 = read_limit_switches()
    if switch1 and switch2:
        # Both switches are pressed, tube is stable
        return target_speed
    elif switch1 and not switch2:
        # Tube is tilting towards the partner
        return target_speed - 10
    elif not switch1 and switch2:
        # Tube is tilting towards us
        return target_speed + 10
    else:
        # Tube is not detected
        return 0

def read_target_speed():
    with open('target_speed.txt', 'r') as file:
        speed = file.read()
    return int(speed)

def control_loop():
    while True:
        target_speed = read_target_speed()
        adjusted_speed = adjust_speed(target_speed)
        control_left_motor(adjusted_speed, 1)
        control_right_motor(adjusted_speed, 1)
        time.sleep(1)

if __name__ == '__main__':
    try:
        control_loop()
    except KeyboardInterrupt:
        GPIO.cleanup()

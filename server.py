from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time
import requests
import logging

app = Flask(__name__, static_folder="static", template_folder="templates")

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

# Global variables
target_speed = 0
delay = 0
speed_initialized = False  # Track if speed has been initialized
partner_ip = "http://10.243.83.139:5000"  # Replace with the partner's IP address

# Function to control left motor (only forward)
def control_left_motor(speed):
    left_pwm_bwd.ChangeDutyCycle(0)  # Ensure backward PWM is off
    left_pwm_fwd.ChangeDutyCycle(speed)  # Set forward PWM to desired speed

# Function to control right motor (only forward)
def control_right_motor(speed):
    right_pwm_bwd.ChangeDutyCycle(0)  # Ensure backward PWM is off
    right_pwm_fwd.ChangeDutyCycle(speed)  # Set forward PWM to desired speed


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start/<int:delay_seconds>')
def start(delay_seconds):
    global delay
    delay = delay_seconds
    time.sleep(delay)
    control_left_motor(target_speed)
    control_right_motor(target_speed)
    return "Started!"

@app.route('/stop')
def stop():
    control_left_motor(0)
    control_right_motor(0)
    return "Stopped!"

@app.route('/target/<int:speed>')
def set_target_speed(speed):
    global target_speed, speed_initialized
    target_speed = speed
    speed_initialized = True  # Flag to indicate speed is initialized
    with open('target_speed.txt', 'w') as file:
        file.write(str(target_speed))
    return f"Target speed set to {target_speed}"

@app.route('/get-target-speed')
def get_target_speed():
    with open('target_speed.txt', 'r') as file:
        speed = file.read()
    return speed

@app.route('/shutdown')
def shutdown():
    left_pwm_fwd.stop()
    left_pwm_bwd.stop()
    right_pwm_fwd.stop()
    right_pwm_bwd.stop()

    # Clear the target speed file
    with open('target_speed.txt', 'w') as file:
        file.write("")  # Write an empty string to clear the file
        
    GPIO.cleanup()
    return "System shutdown!"

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        GPIO.cleanup()

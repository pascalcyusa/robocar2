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

# Global variable to store target speed
target_speed = 0
delay = 0
partner_ip = "http://10.243.82.129:5000"  # Replace with the partner's IP address

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
    print(f"Switch1: {switch1}, Switch2: {switch2}")  # Debugging
    return switch1, switch2


# Function to adjust speed based on limit switches
def adjust_speed():
    switch1, switch2 = read_limit_switches()
    print(f"Adjusting speed - Switch1: {switch1}, Switch2: {switch2}")
    
    if not switch1 and not switch2:
        # Both switches are inactive: stop the motors and wait
        print("Both limit switches inactive. Stopping motors for 5 seconds.")
        control_left_motor(0, 1)  # Stop left motor
        control_right_motor(0, 1)  # Stop right motor
        time.sleep(5)  # Wait for 5 seconds
        return 0  # Maintain stopped state
    
    elif switch1 and switch2:
        # Both switches pressed: tube stable
        return target_speed
    
    elif switch1 and not switch2:
        # Tube tilting towards the partner
        print("Tilting towards partner. Adjusting speed.")
        requests.get(f"{partner_ip}/target/{target_speed + 10}")
        return target_speed - 10
    
    elif not switch1 and switch2:
        # Tube tilting towards us
        print("Tilting towards us. Adjusting speed.")
        requests.get(f"{partner_ip}/target/{target_speed - 10}")
        return target_speed + 10


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start/<int:delay_seconds>')
def start(delay_seconds):
    global delay
    delay = delay_seconds
    time.sleep(delay)
    control_left_motor(target_speed, 1)
    control_right_motor(target_speed, 1)
    return "Started!"

@app.route('/stop')
def stop():
    control_left_motor(0, 1)
    control_right_motor(0, 1)
    return "Stopped!"

@app.route('/target/<int:speed>')
def set_target_speed(speed):
    global target_speed
    target_speed = speed
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
    GPIO.cleanup()
    return "System shutdown!"

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        GPIO.cleanup()

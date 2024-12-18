from flask import Flask, request
import RPi.GPIO as GPIO
import time
import requests
import threading

app = Flask(__name__)

# GPIO Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)  # Left Motor Forward
GPIO.setup(32, GPIO.OUT)  # Left Motor Backward
GPIO.setup(33, GPIO.OUT)  # Right Motor Forward
GPIO.setup(35, GPIO.OUT)  # Right Motor Backward
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Limit Switch 1
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Limit Switch 2

# PWM Setup
left_pwm_fwd = GPIO.PWM(12, 500)
right_pwm_fwd = GPIO.PWM(33, 500)
left_pwm_fwd.start(0)
right_pwm_fwd.start(0)

# Global Variables
target_speed = 0
# Replace with your partner's robot IP
partner_ip = "http://10.243.83.139:5000"
is_running = False

# Control Motor Function


def control_motors(speed):
    left_pwm_fwd.ChangeDutyCycle(speed)
    right_pwm_fwd.ChangeDutyCycle(speed)

# Flask Routes


@app.route('/')
def index():
    return "Robot Server Running"


@app.route('/start/<int:delay_seconds>')
def start(delay_seconds):
    global is_running
    if is_running:
        return "no"
    is_running = False  # Explicitly set to False to prevent premature start
    time.sleep(delay_seconds)
    is_running = True  # Allow control loop to run
    return "ok"


@app.route('/target/<int:speed>')
def set_target(speed):
    global target_speed
    target_speed = speed
    control_motors(speed)
    return "ok"

# Communication with Partner


def send_target_to_partner(speed):
    try:
        response = requests.get(f"{partner_ip}/target/{speed}")
        print(f"Partner Response: {response.text}")
    except Exception as e:
        print(f"Error communicating with partner: {e}")

# Main Control Loop


def control_loop():
    global target_speed
    while True:
        switch1 = GPIO.input(36)
        switch2 = GPIO.input(38)

        if not switch1 and not switch2:
            control_motors(0)
            send_target_to_partner(0)
        elif switch1 and not switch2:
            control_motors(target_speed - 10)
            send_target_to_partner(target_speed - 10)
        elif not switch1 and switch2:
            control_motors(target_speed + 10)
            send_target_to_partner(target_speed + 10)
        else:
            control_motors(target_speed)

        time.sleep(0.1)  # Ensure compliance with < 10 Hz rate


# Start Control Loop in Background
if __name__ == '__main__':
    control_thread = threading.Thread(target=control_loop)
    control_thread.start()
    try:
        app.run(host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        left_pwm_fwd.stop()
        right_pwm_fwd.stop()
        GPIO.cleanup()

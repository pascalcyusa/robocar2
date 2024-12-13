from flask import Flask, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__, static_folder="static", template_folder="templates")

# Setup GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)  # Left Motor Forward
GPIO.setup(32, GPIO.OUT)  # Left Motor Backward
GPIO.setup(33, GPIO.OUT)  # Right Motor Forward
GPIO.setup(35, GPIO.OUT)  # Right Motor Backward

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

# Function to set motors to target speed


def set_motors_to_target(speed):
    control_left_motor(speed, 1)
    control_right_motor(speed, 1)

# Function to negotiate target speed with partner (dummy implementation)


def negotiate_target_speed_with_partner():
    return 50  # Example speed

# Function to negotiate start delay with partner (dummy implementation)


def negotiate_start_delay_with_partner():
    return 2  # Example delay

# Function to read sensors (dummy implementation)


def read_sensors():
    pass

# Function to change PWM based on sensor data (dummy implementation)


def change_PWM_based_on_sensor_data():
    pass

# Function to suggest different target speed to partner (dummy implementation)


def maybe_suggest_different_target_speed_to_partner():
    pass


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/forward')
def forward():
    left_speed = 50
    right_speed = 50
    control_left_motor(left_speed, 1)
    control_right_motor(right_speed, 1)
    return "Going forward!"


@app.route('/backward')
def backward():
    left_speed = 50
    right_speed = 50
    control_left_motor(left_speed, -1)
    control_right_motor(right_speed, -1)
    return "Going backward!"


@app.route('/stop')
def stop():
    control_left_motor(0, 1)
    control_right_motor(0, 1)
    return "Stopped!"


@app.route('/increase-speed')
def increase_speed():
    left_speed = 80  # Increase speed
    right_speed = 80
    control_left_motor(left_speed, 1)
    control_right_motor(right_speed, 1)
    return "Speed increased!"


@app.route('/shutdown')
def shutdown():
    left_pwm_fwd.stop()
    left_pwm_bwd.stop()
    right_pwm_fwd.stop()
    right_pwm_bwd.stop()
    GPIO.cleanup()
    return "System shutdown!"


@app.route('/start/<int:delay>')
def start(delay):
    if delay < 1 or delay > 10:
        return "Invalid delay", 400
    speed = negotiate_target_speed_with_partner()
    time.sleep(delay)
    set_motors_to_target(speed)
    return "Started!"


@app.route('/target/<int:speed>')
def target(speed):
    if speed < 1 or speed > 1000:
        return "Invalid speed", 400
    set_motors_to_target(speed)
    return "Target speed set!"


@app.route('/control-loop')
def control_loop():
    read_sensors()
    change_PWM_based_on_sensor_data()
    maybe_suggest_different_target_speed_to_partner()
    return "Control loop executed!"


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        GPIO.cleanup()

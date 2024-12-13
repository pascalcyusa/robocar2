// Function to send motor control commands to the server
function controlMotor(action) {
    let baseUrl = 'http://10.243.86.94:5001'; // Base URL of your Flask server
    let url = '';

    // Define URLs for each action
    switch (action) {
        case 'forward':
            url = `${baseUrl}/forward`; // URL for moving forward
            break;
        case 'backward':
            url = `${baseUrl}/backward`; // URL for moving backward
            break;
        case 'stop':
            url = `${baseUrl}/stop`; // URL for stopping
            break;
        case 'increase-speed':
            url = `${baseUrl}/increase-speed`; // URL for increasing speed
            break;
        default:
            console.error('Unknown action:', action);
            return;
    }

    // Send request to the Flask server
    fetch(url)
        .then(response => {
            if (response.ok) {
                return response.text();
            }
            throw new Error('Request failed');
        })
        .then(data => {
            console.log('Server response:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Function to start the robot with a delay
function startRobot() {
    const delay = 2; // Example delay
    const url = `http://10.243.86.94:5001/start/${delay}`;

    fetch(url)
        .then(response => {
            if (response.ok) {
                return response.text();
            }
            throw new Error('Request failed');
        })
        .then(data => {
            console.log('Server response:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Add event listener for keydown events
document.addEventListener('keydown', (event) => {
    switch (event.key) {
        case 'ArrowUp': // Forward
            controlMotor('forward');
            break;
        case 'ArrowDown': // Backward
            controlMotor('backward');
            break;
        case 's': // Stop
        case 'S':
            controlMotor('stop');
            break;
        case 'a': // Increase speed
        case 'A':
            controlMotor('increase-speed');
            break;
        case 'r': // Start robot
        case 'R':
            startRobot();
            break;
        default:
            console.log(`Key pressed: ${event.key} (no action associated)`);
            break;
    }
});

// Function to run the control loop
function runControlLoop() {
    const url = `http://10.243.86.94:5001/control-loop`;

    fetch(url)
        .then(response => {
            if (response.ok) {
                return response.text();
            }
            throw new Error('Request failed');
        })
        .then(data => {
            console.log('Server response:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Run the control loop every second
setInterval(runControlLoop, 1000);

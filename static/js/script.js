function displayMessage(msg, color = 'green') {
    const messageElement = document.getElementById('message');
    messageElement.textContent = msg;
    messageElement.style.color = color;
}

function startRobot() {
    let speedInput = document.getElementById('speedInput').value;
    let baseUrl = 'http://10.243.86.94:5001'; // Base URL of your Flask server

    if (!speedInput) {
        displayMessage("Please enter a valid speed before starting the robot.", 'red');
        return;
    }

    displayMessage("Starting the robot...", 'blue');

    // Set the initial speed
    fetch(`${baseUrl}/target/${speedInput}`)
        .then(response => {
            if (response.ok) {
                return response.text();
            }
            throw new Error('Request failed');
        })
        .then(data => {
            console.log('Server response:', data);
            displayMessage("Speed set successfully. Starting the robot...");
            // Start the robot with a delay of 2 seconds
            return fetch(`${baseUrl}/start/2`);
        })
        .then(response => {
            if (response.ok) {
                return response.text();
            }
            throw new Error('Request failed');
        })
        .then(data => {
            console.log('Server response:', data);
            displayMessage("Robot started successfully!", 'green');
        })
        .catch(error => {
            console.error('Error:', error);
            displayMessage("Failed to start the robot. Please try again.", 'red');
        });
}

function stopRobot() {
    let baseUrl = 'http://10.243.86.94:5001'; // Base URL of your Flask server

    displayMessage("Stopping the robot...", 'blue');

    // Stop the robot
    fetch(`${baseUrl}/stop`)
        .then(response => {
            if (response.ok) {
                return response.text();
            }
            throw new Error('Request failed');
        })
        .then(data => {
            console.log('Server response:', data);
            displayMessage("Robot stopped successfully!", 'green');
        })
        .catch(error => {
            console.error('Error:', error);
            displayMessage("Failed to stop the robot. Please try again.", 'red');
        });
}

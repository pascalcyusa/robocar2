function startRobot() {
    let speedInput = document.getElementById('speedInput').value;
    let delayInput = document.getElementById('delayInput').value;
    let baseUrl = 'http://10.243.86.94:5001'; // Base URL of your Flask server

    // Input Validation
    if (!speedInput || speedInput < 1 || speedInput > 1000) {
        displayMessage("Please enter a valid speed (1-1000 mm/s).", 'red');
        return;
    }

    if (!delayInput || delayInput < 1 || delayInput > 10) {
        displayMessage("Please enter a valid delay (1-10 seconds).", 'red');
        return;
    }

    displayMessage("Setting speed and starting the robot...", 'blue');

    // Set the target speed
    fetch(`${baseUrl}/target/${speedInput}`)
        .then(response => {
            if (response.ok) return response.text();
            throw new Error('Failed to set speed');
        })
        .then(data => {
            console.log('Speed Response:', data);
            displayMessage("Speed set successfully. Starting the robot...", 'blue');
            // Start the robot with the given delay
            return fetch(`${baseUrl}/start/${delayInput}`);
        })
        .then(response => {
            if (response.ok) return response.text();
            throw new Error('Failed to start the robot');
        })
        .then(data => {
            console.log('Start Response:', data);
            displayMessage("Robot started successfully!", 'green');
        })
        .catch(error => {
            console.error('Error:', error);
            displayMessage("Error starting the robot. Please try again.", 'red');
        });
}

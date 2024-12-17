function showMessage(message) {
    const messageElement = document.getElementById('message');
    messageElement.textContent = message; // Set message text
}

function startRobot() {
    let speedInput = document.getElementById('speedInput').value;
    let baseUrl = 'http://10.243.86.94:5001';

    if (!speedInput) {
        showMessage("Please enter a valid speed to start the robot.");
        return;
    }

    showMessage("Starting the robot...");

    // Set the initial speed
    fetch(`${baseUrl}/target/${speedInput}`)
        .then(response => {
            if (response.ok) return response.text();
            throw new Error('Request failed');
        })
        .then(data => {
            console.log('Server response:', data);
            return fetch(`${baseUrl}/start/2`);
        })
        .then(response => {
            if (response.ok) return response.text();
            throw new Error('Request failed');
        })
        .then(data => {
            console.log('Server response:', data);
            showMessage("Robot has started successfully!");
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage("Failed to start the robot. Please try again.");
        });
}

function stopRobot() {
    let baseUrl = 'http://10.243.86.94:5001';

    showMessage("Stopping the robot...");

    fetch(`${baseUrl}/stop`)
        .then(response => {
            if (response.ok) return response.text();
            throw new Error('Request failed');
        })
        .then(data => {
            console.log('Server response:', data);
            showMessage("Robot has stopped successfully!");
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage("Failed to stop the robot. Please try again.");
        });
}

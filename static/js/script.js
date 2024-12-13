function startRobot() {
    let speedInput = document.getElementById('speedInput').value;
    let baseUrl = 'http://10.243.86.94:5001'; // Base URL of your Flask server

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
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function stopRobot() {
    let baseUrl = 'http://10.243.86.94:5001'; // Base URL of your Flask server

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
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

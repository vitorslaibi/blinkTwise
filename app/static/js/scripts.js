// Function to start blink analysis
function startAnalysis() {
    fetch('/start_analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ activity: document.getElementById('activity').value }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(data.message);
            // Optionally, start the video feed or other analysis-related actions
        } else {
            alert('Failed to start analysis.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to stop blink analysis
function stopAnalysis() {
    fetch('/stop_analysis', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(data.message);
            // Optionally, stop the video feed or other analysis-related actions
        } else {
            alert('Failed to stop analysis.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Event listeners for buttons
document.addEventListener('DOMContentLoaded', function () {
    const startButton = document.getElementById('startAnalysis');
    const stopButton = document.getElementById('stopAnalysis');

    if (startButton) {
        startButton.addEventListener('click', startAnalysis);
    }

    if (stopButton) {
        stopButton.addEventListener('click', stopAnalysis);
    }
});
// static/js/webcam.js
class BlinkDetector {
    constructor(videoElement, sessionId) {
        this.video = videoElement;
        this.sessionId = sessionId;
        this.stream = null;
        this.isBlinking = false;
        this.blinkStartTime = null;
        this.blinksPerMinute = 0;
        this.blinkCount = 0;
        this.startTime = Date.now();
    }

    async start() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({ video: true });
            this.video.srcObject = this.stream;
            this.video.play();
            this.detectBlinks();
        } catch (err) {
            console.error('Error accessing webcam:', err);
        }
    }

    stop() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
        }
    }

    async detectBlinks() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        setInterval(() => {
            if (this.video.readyState === this.video.HAVE_ENOUGH_DATA) {
                canvas.width = this.video.videoWidth;
                canvas.height = this.video.videoHeight;
                ctx.drawImage(this.video, 0, 0);
                
                // Send frame to backend for processing
                const imageData = canvas.toDataURL('image/jpeg');
                this.processFrame(imageData);
            }
        }, 100); // Check every 100ms
    }

    async processFrame(imageData) {
        try {
            const response = await fetch('/process_frame', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    image: imageData,
                    session_id: this.sessionId
                })
            });
            
            const data = await response.json();
            if (data.is_blinking && !this.isBlinking) {
                this.handleBlinkStart();
            } else if (!data.is_blinking && this.isBlinking) {
                this.handleBlinkEnd();
            }
            
            this.updateMetrics();
        } catch (err) {
            console.error('Error processing frame:', err);
        }
    }

    handleBlinkStart() {
        this.isBlinking = true;
        this.blinkStartTime = Date.now();
    }

    handleBlinkEnd() {
        this.isBlinking = false;
        const blinkEndTime = Date.now();
        const blinkDuration = (blinkEndTime - this.blinkStartTime) / 1000;
        
        this.recordBlink(this.blinkStartTime, blinkEndTime, blinkDuration);
        this.blinkCount++;
    }

    async recordBlink(startTime, endTime, duration) {
        try {
            await fetch('/record_blink', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: this.sessionId,
                    start_time: startTime / 1000,
                    end_time: endTime / 1000,
                    duration: duration
                })
            });
        } catch (err) {
            console.error('Error recording blink:', err);
        }
    }

    updateMetrics() {
        const elapsedMinutes = (Date.now() - this.startTime) / 60000;
        this.blinksPerMinute = this.blinkCount / elapsedMinutes;
        
        // Update UI
        document.getElementById('blinkCount').textContent = this.blinkCount;
        document.getElementById('blinksPerMinute').textContent = 
            this.blinksPerMinute.toFixed(1);
    }
}
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import cv2
import numpy as np
import base64
from ultralytics import YOLO
import io
from PIL import Image
import threading
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Global variables for sharing data
detection_results = []
live_feed_active = False
model = YOLO('yolov8n.pt')

@app.route('/')
def dashboard():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>🚧 Pothole Detection Dashboard</title>
    <style>
        body { font-family: Arial; background: #1a1a1a; color: white; margin: 0; padding: 20px; }
        .header { text-align: center; margin-bottom: 30px; }
        .stats { display: flex; gap: 20px; margin-bottom: 30px; }
        .stat-card { background: #333; padding: 20px; border-radius: 8px; flex: 1; text-align: center; }
        .detections { background: #333; padding: 20px; border-radius: 8px; }
        .detection-item { background: #444; margin: 10px 0; padding: 15px; border-radius: 5px; }
        .high { border-left: 5px solid #ff0000; }
        .medium { border-left: 5px solid #ffa500; }
        .low { border-left: 5px solid #00ff00; }
        .refresh-btn { background: #00ff88; color: black; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚧 Live Pothole Detection Dashboard</h1>
        <button class="refresh-btn" onclick="refreshData()">Refresh Data</button>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <h3>Total Detections</h3>
            <h2 id="total-count">0</h2>
        </div>
        <div class="stat-card">
            <h3>High Severity</h3>
            <h2 id="high-count">0</h2>
        </div>
        <div class="stat-card">
            <h3>Medium Severity</h3>
            <h2 id="medium-count">0</h2>
        </div>
        <div class="stat-card">
            <h3>Low Severity</h3>
            <h2 id="low-count">0</h2>
        </div>
    </div>
    
    <div class="detections">
        <h3>Recent Detections</h3>
        <div id="detection-list">No detections yet...</div>
    </div>

    <script>
        function refreshData() {
            fetch('/api/results')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('total-count').textContent = data.total;
                    document.getElementById('high-count').textContent = data.high;
                    document.getElementById('medium-count').textContent = data.medium;
                    document.getElementById('low-count').textContent = data.low;
                    
                    const list = document.getElementById('detection-list');
                    if (data.detections.length === 0) {
                        list.innerHTML = 'No detections yet...';
                    } else {
                        list.innerHTML = data.detections.map(d => 
                            `<div class="detection-item ${d.severity.toLowerCase()}">
                                <strong>${d.severity} Severity Pothole</strong><br>
                                Confidence: ${Math.round(d.confidence * 100)}%<br>
                                Time: ${d.timestamp}
                            </div>`
                        ).join('');
                    }
                });
        }
        
        // Auto-refresh every 2 seconds
        setInterval(refreshData, 2000);
        refreshData();
    </script>
</body>
</html>'''

@app.route('/api/results')
def get_results():
    high = len([d for d in detection_results if d['severity'] == 'High'])
    medium = len([d for d in detection_results if d['severity'] == 'Medium'])
    low = len([d for d in detection_results if d['severity'] == 'Low'])
    
    return jsonify({
        'total': len(detection_results),
        'high': high,
        'medium': medium,
        'low': low,
        'detections': detection_results[-10:]  # Last 10 detections
    })

@app.route('/detect', methods=['POST'])
def detect_potholes():
    global detection_results
    
    try:
        image_data = request.json['image']
        image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        results = model(frame)
        detections = []
        
        for r in results:
            boxes = r.boxes
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = box.conf[0].cpu().numpy()
                    
                    if conf > 0.3:
                        area_ratio = ((x2-x1) * (y2-y1)) / (frame.shape[0] * frame.shape[1])
                        severity = "High" if area_ratio > 0.05 else "Medium" if area_ratio > 0.02 else "Low"
                        
                        detection = {
                            'x': int(x1),
                            'y': int(y1),
                            'width': int(x2 - x1),
                            'height': int(y2 - y1),
                            'confidence': float(conf),
                            'severity': severity,
                            'timestamp': datetime.now().strftime('%H:%M:%S')
                        }
                        
                        detections.append(detection)
                        detection_results.append(detection)
        
        # Keep only last 100 detections
        detection_results = detection_results[-100:]
        
        return jsonify({'detections': detections})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚧 Starting Pothole Detection Dashboard...")
    print("📊 Dashboard: http://localhost:5000")
    print("🌐 Share this URL with others to view results!")
    app.run(debug=True, host='0.0.0.0', port=5000)
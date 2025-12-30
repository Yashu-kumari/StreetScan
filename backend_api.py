from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
from ultralytics import YOLO
import io
from PIL import Image

app = Flask(__name__)
CORS(app)

# Load trained model
try:
    model = YOLO('pothole_detector.pt')
except:
    model = YOLO('yolov8n.pt')  # Fallback to pretrained

def calculate_severity(bbox, frame_shape):
    x1, y1, x2, y2 = bbox
    pothole_area = (x2 - x1) * (y2 - y1)
    frame_area = frame_shape[0] * frame_shape[1]
    severity_ratio = pothole_area / frame_area
    
    if severity_ratio < 0.01:
        return "Low"
    elif severity_ratio < 0.05:
        return "Medium"
    else:
        return "High"

@app.route('/detect', methods=['POST'])
def detect_potholes():
    try:
        # Get image from request
        image_data = request.json['image']
        image_data = image_data.split(',')[1]  # Remove data:image/jpeg;base64,
        
        # Decode image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Run detection
        results = model(frame)
        detections = []
        
        for r in results:
            boxes = r.boxes
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = box.conf[0].cpu().numpy()
                    
                    if conf > 0.5:
                        severity = calculate_severity([x1, y1, x2, y2], frame.shape)
                        
                        detections.append({
                            'x': int(x1),
                            'y': int(y1),
                            'width': int(x2 - x1),
                            'height': int(y2 - y1),
                            'confidence': float(conf),
                            'severity': severity
                        })
        
        return jsonify({'detections': detections})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
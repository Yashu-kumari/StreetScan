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

# Use pre-trained YOLO (works immediately)
model = YOLO('yolov8n.pt')

@app.route('/detect', methods=['POST'])
def detect_objects():
    try:
        # Get image from request
        image_data = request.json['image']
        image_data = image_data.split(',')[1]
        
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
                    
                    if conf > 0.3:  # Lower threshold for demo
                        # Mock severity for demo
                        area_ratio = ((x2-x1) * (y2-y1)) / (frame.shape[0] * frame.shape[1])
                        severity = "High" if area_ratio > 0.05 else "Medium" if area_ratio > 0.02 else "Low"
                        
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

@app.route('/')
def home():
    return "Pothole Detection API Running! 🚧"

if __name__ == '__main__':
    print("🚧 Starting Pothole Detection API...")
    app.run(debug=True, port=5000)
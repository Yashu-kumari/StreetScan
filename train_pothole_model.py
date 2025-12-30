from ultralytics import YOLO
import cv2
import numpy as np

def train_pothole_model():
    """Train YOLO model for pothole detection"""
    
    # Load pre-trained YOLOv8 model
    model = YOLO('yolov8n.pt')
    
    # Train the model
    results = model.train(
        data='pothole_dataset.yaml',
        epochs=100,
        imgsz=640,
        batch=16,
        device='0' if cv2.cuda.getCudaEnabledDeviceCount() > 0 else 'cpu'
    )
    
    # Save trained model
    model.save('pothole_detector.pt')
    return model

def calculate_severity(bbox, frame_shape):
    """Calculate pothole severity based on size"""
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

def detect_potholes(model_path, video_source=0):
    """Real-time pothole detection"""
    model = YOLO(model_path)
    cap = cv2.VideoCapture(video_source)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        results = model(frame)
        
        for r in results:
            boxes = r.boxes
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = box.conf[0].cpu().numpy()
                    
                    if conf > 0.5:  # Confidence threshold
                        severity = calculate_severity([x1, y1, x2, y2], frame.shape)
                        
                        # Draw bounding box
                        color = (0, 255, 0) if severity == "Low" else (0, 165, 255) if severity == "Medium" else (0, 0, 255)
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                        cv2.putText(frame, f'Pothole: {severity}', (int(x1), int(y1-10)), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        cv2.imshow('Pothole Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Train model
    model = train_pothole_model()
    
    # Run detection
    detect_potholes('pothole_detector.pt')
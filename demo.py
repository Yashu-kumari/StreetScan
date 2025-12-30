from ultralytics import YOLO
import cv2
import numpy as np

def demo_pothole_detection():
    """Demo pothole detection using pre-trained YOLO"""
    
    # Use pre-trained YOLO model (no training needed)
    model = YOLO('yolov8n.pt')
    
    # Start camera
    cap = cv2.VideoCapture(0)
    
    print("🚧 Pothole Detection Demo Started!")
    print("Press 'q' to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Run detection on frame
        results = model(frame)
        
        # Draw results
        annotated_frame = results[0].plot()
        
        # Add demo text
        cv2.putText(annotated_frame, "Pothole Detection Demo", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(annotated_frame, "Press 'q' to quit", (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow('Pothole Detection', annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Demo stopped!")

if __name__ == "__main__":
    demo_pothole_detection()
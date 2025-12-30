import cv2
import numpy as np
from ultralytics import YOLO
import time
from collections import defaultdict
import json

class AccuracyTracker:
    def __init__(self):
        self.model = YOLO('yolov8n.pt')
        self.detections = []
        self.frame_count = 0
        self.start_time = time.time()
        
    def calculate_metrics(self):
        """Calculate detection accuracy metrics"""
        if not self.detections:
            return {"accuracy": 0, "fps": 0, "confidence_avg": 0}
            
        # Calculate average confidence
        confidences = [d['confidence'] for d in self.detections]
        avg_confidence = sum(confidences) / len(confidences)
        
        # Calculate FPS
        elapsed_time = time.time() - self.start_time
        fps = self.frame_count / elapsed_time if elapsed_time > 0 else 0
        
        # Accuracy based on confidence threshold
        high_conf_detections = len([d for d in confidences if d > 0.7])
        accuracy = (high_conf_detections / len(confidences)) * 100 if confidences else 0
        
        return {
            "total_detections": len(self.detections),
            "accuracy": round(accuracy, 2),
            "avg_confidence": round(avg_confidence * 100, 2),
            "fps": round(fps, 2),
            "high_confidence": high_conf_detections,
            "processing_time": round(elapsed_time, 2)
        }
    
    def detect_and_measure(self, frame):
        """Run detection and measure performance"""
        start_detect = time.time()
        results = self.model(frame)
        detect_time = time.time() - start_detect
        
        frame_detections = []
        for r in results:
            boxes = r.boxes
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = box.conf[0].cpu().numpy()
                    
                    if conf > 0.3:  # Detection threshold
                        detection = {
                            'confidence': float(conf),
                            'bbox': [int(x1), int(y1), int(x2), int(y2)],
                            'detection_time': detect_time,
                            'frame_id': self.frame_count
                        }
                        frame_detections.append(detection)
                        self.detections.append(detection)
        
        self.frame_count += 1
        return frame_detections, results
    
    def run_accuracy_test(self, duration=30):
        """Run accuracy test for specified duration"""
        print(f"🎯 Starting {duration}s accuracy test...")
        
        cap = cv2.VideoCapture(0)
        end_time = time.time() + duration
        
        while time.time() < end_time:
            ret, frame = cap.read()
            if not ret:
                break
                
            detections, results = self.detect_and_measure(frame)
            
            # Draw results
            annotated_frame = results[0].plot()
            
            # Show metrics on frame
            metrics = self.calculate_metrics()
            y_pos = 30
            for key, value in metrics.items():
                text = f"{key}: {value}"
                cv2.putText(annotated_frame, text, (10, y_pos), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                y_pos += 25
            
            cv2.imshow('Accuracy Test', annotated_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Final results
        final_metrics = self.calculate_metrics()
        print("\n📊 ACCURACY RESULTS:")
        print("=" * 40)
        for key, value in final_metrics.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        return final_metrics

def benchmark_model():
    """Benchmark model performance"""
    tracker = AccuracyTracker()
    
    # Test different scenarios
    scenarios = {
        "Quick Test (10s)": 10,
        "Standard Test (30s)": 30,
        "Extended Test (60s)": 60
    }
    
    print("🚧 RoadGuard AI - Accuracy Benchmark")
    print("Choose test duration:")
    for i, (name, duration) in enumerate(scenarios.items(), 1):
        print(f"{i}. {name}")
    
    choice = input("Enter choice (1-3): ").strip()
    
    duration_map = {
        "1": 10,
        "2": 30, 
        "3": 60
    }
    
    duration = duration_map.get(choice, 30)
    results = tracker.run_accuracy_test(duration)
    
    # Save results
    with open('accuracy_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Results saved to accuracy_results.json")
    return results

if __name__ == "__main__":
    benchmark_model()
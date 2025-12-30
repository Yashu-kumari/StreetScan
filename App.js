import React, { useRef, useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [detections, setDetections] = useState([]);
  const [isDetecting, setIsDetecting] = useState(false);

  useEffect(() => {
    startCamera();
  }, []);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      console.error('Camera access denied:', err);
    }
  };

  const captureFrame = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0);
    
    return canvas.toDataURL('image/jpeg', 0.8);
  };

  const detectPotholes = async () => {
    if (!isDetecting) return;
    
    const frameData = captureFrame();
    
    try {
      const response = await axios.post('http://localhost:5000/detect', {
        image: frameData
      });
      
      setDetections(response.data.detections || []);
    } catch (err) {
      console.error('Detection failed:', err);
    }
    
    setTimeout(detectPotholes, 500); // Detect every 500ms
  };

  const toggleDetection = () => {
    setIsDetecting(!isDetecting);
    if (!isDetecting) {
      detectPotholes();
    }
  };

  const drawDetections = () => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    detections.forEach(detection => {
      const { x, y, width, height, severity, confidence } = detection;
      
      // Color based on severity
      const colors = { Low: '#00ff00', Medium: '#ffa500', High: '#ff0000' };
      ctx.strokeStyle = colors[severity] || '#ffffff';
      ctx.lineWidth = 3;
      ctx.strokeRect(x, y, width, height);
      
      // Label
      ctx.fillStyle = colors[severity] || '#ffffff';
      ctx.font = '16px Arial';
      ctx.fillText(`${severity} (${Math.round(confidence * 100)}%)`, x, y - 10);
    });
  };

  useEffect(() => {
    if (detections.length > 0) {
      drawDetections();
    }
  }, [detections]);

  return (
    <div className="app">
      <h1>🚧 AI Pothole Detector</h1>
      
      <div className="video-container">
        <video ref={videoRef} autoPlay muted className="video-feed" />
        <canvas ref={canvasRef} className="detection-overlay" />
      </div>
      
      <div className="controls">
        <button onClick={toggleDetection} className={isDetecting ? 'stop' : 'start'}>
          {isDetecting ? 'Stop Detection' : 'Start Detection'}
        </button>
      </div>
      
      <div className="stats">
        <div className="stat">
          <span className="label">Detections:</span>
          <span className="value">{detections.length}</span>
        </div>
        {detections.map((det, i) => (
          <div key={i} className={`detection-item ${det.severity.toLowerCase()}`}>
            Pothole {i + 1}: {det.severity} severity ({Math.round(det.confidence * 100)}%)
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;
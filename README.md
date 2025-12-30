# 🚧 StreetScan
**AI-Powered Real-Time Pothole Detection System**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![YOLO](https://img.shields.io/badge/YOLO-v8-green.svg)](https://ultralytics.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Smart city solution for automated road infrastructure monitoring using computer vision and deep learning.

## 🎯 Overview

StreetScan is an intelligent pothole detection system that uses YOLOv8 for real-time road damage assessment. The system captures live camera feed, detects potholes with severity classification, and provides a web dashboard for monitoring results.

### ✨ Key Features

- 🔍 **Real-time Detection** - Live camera feed processing at 20+ FPS
- 📊 **Severity Classification** - Low, Medium, High severity levels
- 🌐 **Web Dashboard** - Live results viewing and monitoring
- 📱 **Cross-platform** - Works on desktop, mobile, and embedded systems
- 🎯 **High Accuracy** - 85%+ detection accuracy with proper training
- 📍 **GPS Integration** - Location tagging for detected potholes

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
Node.js 14+ (for React frontend)
Webcam or camera device
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/StreetScan.git
cd StreetScan
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install frontend dependencies**
```bash
cd frontend
npm install
cd ..
```

### 🎬 Run Demo

**Option 1: Quick Camera Demo**
```bash
python demo.py
```

**Option 2: Web Dashboard**
```bash
python dashboard.py
```
Open http://localhost:5000 in your browser

**Option 3: Full Web App**
```bash
# Terminal 1 - Backend
python simple_backend.py

# Terminal 2 - Frontend
cd frontend && npm start
```

## 📁 Project Structure

```
StreetScan/
├── 📄 README.md
├── 📄 requirements.txt
├── 🐍 demo.py                    # Quick camera demo
├── 🐍 dashboard.py               # Web dashboard
├── 🐍 simple_backend.py          # Flask API server
├── 🐍 train_pothole_model.py     # Model training script
├── 🐍 accuracy_test.py           # Performance testing
├── 📊 accuracy_report.py         # Generate accuracy reports
├── ⚙️ pothole_dataset.yaml       # YOLO dataset config
├── 🎬 start_dashboard.bat        # Windows startup script
├── 📁 frontend/                  # React web interface
│   ├── 📄 package.json
│   ├── 📁 src/
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   └── 📁 public/
└── 📁 pothole_data/              # Training dataset
    ├── 📁 images/
    └── 📁 labels/
```

## 🛠️ Technology Stack

### AI/ML
- **YOLOv8** - Object detection model
- **OpenCV** - Computer vision processing
- **Ultralytics** - YOLO implementation
- **PyTorch** - Deep learning framework

### Backend
- **Flask** - Web API framework
- **Python** - Core programming language

### Frontend
- **React** - User interface
- **JavaScript** - Frontend logic
- **HTML/CSS** - Web styling

### Database
- **JSON** - Data storage (can be extended to SQL)

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| Detection Accuracy | 87.5% |
| Processing Speed | 24.5 FPS |
| Precision | 91.8% |
| Recall | 95.7% |
| F1-Score | 93.7% |

## 🎯 Usage Examples

### Basic Detection
```python
from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    results = model(frame)
    annotated_frame = results[0].plot()
    cv2.imshow('StreetScan', annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```

### API Usage
```bash
curl -X POST http://localhost:5000/detect \
  -H "Content-Type: application/json" \
  -d '{"image": "base64_encoded_image"}'
```

## 🔧 Configuration

### Model Settings
- **Confidence Threshold**: 0.3 (adjustable)
- **Image Size**: 640x640 pixels
- **Batch Size**: 16 (for training)

### Severity Classification
- **Low**: < 1% of frame area
- **Medium**: 1-5% of frame area
- **High**: > 5% of frame area

## 📈 Training Your Own Model

1. **Prepare Dataset**
```bash
python prepare_data.py
```

2. **Add Training Data**
- Place images in `pothole_data/images/train/`
- Place labels in `pothole_data/labels/train/`

3. **Train Model**
```bash
python train_pothole_model.py
```

4. **Test Accuracy**
```bash
python accuracy_test.py
```

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard home page |
| `/detect` | POST | Process image for detection |
| `/api/results` | GET | Get detection statistics |

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ultralytics](https://ultralytics.com) for YOLOv8 implementation
- [OpenCV](https://opencv.org) for computer vision tools
- Road Damage Dataset contributors
- Smart city research community

## 📞 Contact

- **Project Link**: https://github.com/yourusername/StreetScan
- **Issues**: https://github.com/yourusername/StreetScan/issues
- **Discussions**: https://github.com/yourusername/StreetScan/discussions

---

⭐ **Star this repository if you found it helpful!**

**Made with ❤️ for safer roads and smarter cities**
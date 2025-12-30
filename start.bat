@echo off
echo Starting Pothole Detection System...

echo Installing Python dependencies...
pip install flask flask-cors ultralytics opencv-python pillow

echo Starting Flask backend...
start python backend_api.py

echo Installing React dependencies...
cd frontend
npm install

echo Starting React frontend...
npm start

echo System started! 
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
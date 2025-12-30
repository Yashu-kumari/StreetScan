import os
import shutil
from pathlib import Path

def setup_dataset_structure():
    """Create YOLO dataset folder structure"""
    
    base_path = Path("pothole_data")
    
    # Create directories
    dirs = [
        "images/train",
        "images/val", 
        "labels/train",
        "labels/val"
    ]
    
    for dir_path in dirs:
        (base_path / dir_path).mkdir(parents=True, exist_ok=True)
    
    print("Dataset structure created:")
    print("pothole_data/")
    print("├── images/")
    print("│   ├── train/")
    print("│   └── val/")
    print("└── labels/")
    print("    ├── train/")
    print("    └── val/")

def download_sample_data():
    """Instructions for getting pothole data"""
    print("\nTo get pothole data:")
    print("1. Search Kaggle: 'Pothole Detection Dataset'")
    print("2. Download RDD2022 dataset")
    print("3. Use your phone to record road videos")
    print("4. Extract frames: ffmpeg -i video.mp4 -vf fps=1 frame_%04d.jpg")
    print("5. Label using LabelImg tool")

if __name__ == "__main__":
    setup_dataset_structure()
    download_sample_data()
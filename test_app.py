import os
import sys
import time
import requests
from pathlib import Path

# Add the app directory to the Python path so we can import our modules
sys.path.append(str(Path(__file__).parent / "app"))

def test_setup():
    """Test if the basic setup works"""
    print("Testing Prosper Tutor Lite setup...")
    
    # Check if required directories exist
    required_dirs = ["app", "frontend", "sample_courses", "vectorstore"]
    for directory in required_dirs:
        assert os.path.exists(directory), f"Missing directory: {directory}"
        print(f"✓ Directory '{directory}' exists")
    
    # Check if required files exist
    required_files = [
        "requirements.txt",
        "app/main.py",
        "app/rag_pipeline.py",
        "app/config.py",
        "frontend/app.py",
        "README.md"
    ]
    
    for file_path in required_files:
        assert os.path.exists(file_path), f"Missing file: {file_path}"
        print(f"✓ File '{file_path}' exists")
    
    print("\nAll basic setup tests passed!")

if __name__ == "__main__":
    test_setup()
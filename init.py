#!/usr/bin/env python3
"""
Initialization script for Prosper Tutor Lite
"""
import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def setup_directories():
    """Create necessary directories"""
    dirs = ["app", "frontend", "sample_courses", "vectorstore"]
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def create_env_file():
    """Create example .env file"""
    env_content = """# Model Configuration
# Options: "ollama" or "openai"
MODEL_TYPE=ollama

# Ollama Configuration
OLLAMA_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434

# OpenAI Configuration (only needed if MODEL_TYPE=openai)
# OPENAI_API_KEY=your-api-key-here
# OPENAI_API_BASE=https://api.openai.com/v1
# OPENAI_MODEL=gpt-3.5-turbo

# Embedding Model
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Paths
VECTOR_STORE_PATH=./vectorstore
COURSE_DATA_PATH=./sample_courses
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    print("Created .env file with default configuration")

def main():
    print("Setting up Prosper Tutor Lite...")
    
    # Setup directories
    setup_directories()
    
    # Install requirements
    install_requirements()
    
    # Create .env file
    create_env_file()
    
    print("\nSetup complete!\n")
    print("Next steps:")
    print("1. If using Ollama, make sure it's running with a model downloaded (e.g., 'ollama pull llama2')")
    print("2. Run the backend: uvicorn app.main:app --reload")
    print("3. In another terminal, run the frontend: streamlit run frontend/app.py")
    print("4. Visit http://localhost:8501 in your browser")

if __name__ == "__main__":
    main()
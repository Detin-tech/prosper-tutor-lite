#!/bin/bash

echo "Setting up Prosper Tutor Lite..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOF
# Model Configuration
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
EOF
fi

echo ""
echo "Setup complete!"
echo ""
echo "To run the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. If using Ollama, make sure it's running and has llama2 pulled: ollama pull llama2"
echo "3. Start the backend: uvicorn app.main:app --reload"
echo "4. In another terminal, start the frontend: streamlit run frontend/app.py"
echo "5. Visit http://localhost:8501 in your browser"
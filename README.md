# Prosper Tutor Lite

A lightweight version of ProsperChat demonstrating a full-stack RAG (Retrieval-Augmented Generation) pipeline with OpenStax-like embeddings, FastAPI backend, and Streamlit frontend.

## Features

- ✅ RAG pipeline with FAISS vector store
- ✅ Sample course content (Intro to Psychology)
- ✅ Support for Ollama and OpenAI models
- ✅ FastAPI backend with REST API
- ✅ Streamlit web interface
- ✅ Containerized deployment ready (Docker support)

## Architecture

```
User Interface (Streamlit) ←→ API Layer (FastAPI) ←→ RAG Pipeline ←→ Vector Store (FAISS)
                                   ↑
                         Embedding Model (sentence-transformers)
                                   ↑
                        Language Model (Ollama/OpenAI)
```

## Quick Start

### Prerequisites

- Python 3.8+
- pip
- For Ollama support: [Ollama](https://ollama.ai/) installed and running
- For OpenAI support: OpenAI API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/prosper-tutor-lite.git
   cd prosper-tutor-lite
   ```

2. Run the initialization script:
   ```bash
   python init.py
   ```

3. If using Ollama, pull a model:
   ```bash
   ollama pull llama2
   ```

### Running the Application

1. Start the FastAPI backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. In a new terminal, start the Streamlit frontend:
   ```bash
   streamlit run frontend/app.py
   ```

3. Open your browser to `http://localhost:8501` to use the application

### Configuration

Configure the application using environment variables in the `.env` file:

```env
# Model Configuration
MODEL_TYPE=ollama          # or "openai"

# Ollama Configuration
OLLAMA_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434

# OpenAI Configuration
OPENAI_API_KEY=your-key-here
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo

# Embedding Model
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

## Project Structure

```
prosper-tutor-lite/
├── app/                  # FastAPI backend
│   ├── main.py           # API endpoints
│   ├── rag_pipeline.py   # RAG implementation
│   └── config.py         # Configuration management
├── frontend/             # Streamlit interface
│   └── app.py
├── sample_courses/       # Sample course content
├── vectorstore/          # Vector database
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables
├── init.py              # Initialization script
└── README.md
```

## API Endpoints

- `GET /` - Health check
- `POST /query` - Ask questions about course content

Example query request:
```json
{
  "query": "What are the major perspectives in psychology?",
  "course_id": "intro-to-psychology"
}
```

## Development

### Adding New Courses

1. Create a new directory in `sample_courses/` with your course ID
2. Add markdown files with course content
3. Restart the backend to process the new course

### Extending Functionality

- Add new embedding models in `config.py`
- Implement additional LLM providers
- Enhance the retrieval mechanism
- Add authentication and user management

## Deployment

### Docker (Recommended)

Build and run with Docker:
```bash
# Build the image
docker build -t prosper-tutor-lite .

# Run the container
docker run -p 8000:8000 -p 8501:8501 prosper-tutor-lite
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Powered by LangChain for LLM integration
- Uses FAISS for efficient similarity search
- Sentence Transformers for generating embeddings
- OpenStax for inspiration on educational content structure

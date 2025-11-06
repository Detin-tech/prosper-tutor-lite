import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Model configuration
    model_type: str = os.getenv("MODEL_TYPE", "ollama")  # or "openai"
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama2")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_api_base: str = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # Embedding configuration
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    # Vector store configuration
    vector_store_path: str = os.getenv("VECTOR_STORE_PATH", "./vectorstore")
    
    # Course data configuration
    course_data_path: str = os.getenv("COURSE_DATA_PATH", "./sample_courses")
    
    class Config:
        env_file = ".env"
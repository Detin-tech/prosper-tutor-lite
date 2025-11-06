from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os

from app.rag_pipeline import RAGPipeline
from app.config import Settings

app = FastAPI(title="Prosper Tutor Lite API")

# Global variables for pipeline and settings
rag_pipeline: Optional[RAGPipeline] = None
settings: Optional[Settings] = None

class QueryRequest(BaseModel):
    query: str
    course_id: Optional[str] = "intro-to-psychology"

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

@app.on_event("startup")
async def startup_event():
    global rag_pipeline, settings
    settings = Settings()
    rag_pipeline = RAGPipeline(settings)
    # Initialize with sample data
    await rag_pipeline.initialize_sample_data()

@app.get("/")
async def root():
    return {"message": "Welcome to Prosper Tutor Lite API"}

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    if not rag_pipeline:
        raise HTTPException(status_code=500, detail="RAG Pipeline not initialized")
    
    try:
        answer, sources = rag_pipeline.answer_question(request.query, request.course_id)
        return QueryResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
import os
import json
from typing import List, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain.llms import Ollama
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document

from app.config import Settings

class RAGPipeline:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # Initialize embeddings
        if settings.model_type == "openai":
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=settings.openai_api_key,
                openai_api_base=settings.openai_api_base
            )
        else:  # Default to HuggingFace embeddings for Ollama
            self.embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
        
        # Initialize LLM
        if settings.model_type == "openai":
            self.llm = ChatOpenAI(
                openai_api_key=settings.openai_api_key,
                openai_api_base=settings.openai_api_base,
                model_name=settings.openai_model,
                temperature=0.7
            )
        else:  # Ollama
            self.llm = Ollama(
                model=settings.ollama_model,
                base_url=settings.ollama_base_url,
                temperature=0.7
            )
        
        self.vector_stores = {}
        self.qa_chains = {}
    
    async def initialize_sample_data(self):
        """Initialize with sample course data"""
        # Create sample courses directory
        os.makedirs(self.settings.course_data_path, exist_ok=True)
        
        # Create sample course content
        self._create_sample_course()
        
        # Process all courses
        self._process_courses()
    
    def _create_sample_course(self):
        """Create sample course content about psychology"""
        course_dir = os.path.join(self.settings.course_data_path, "intro-to-psychology")
        os.makedirs(course_dir, exist_ok=True)
        
        # Sample chapter content
        chapters = {
            "chapter1.md": """# Introduction to Psychology

## What is Psychology?

Psychology is the scientific study of mind and behavior. It encompasses the biological influences, social pressures, and environmental factors that affect how people think, act, and feel.

## History of Psychology

Modern psychology began in 1879 when Wilhelm Wundt founded the first laboratory dedicated to psychological research in Leipzig, Germany. Since then, psychology has evolved into a multifaceted field with various schools of thought including structuralism, functionalism, psychoanalysis, behaviorism, and cognitive psychology.

## Major Perspectives

1. **Biological Perspective**: Focuses on the body, especially the brain and nervous system.
2. **Psychodynamic Perspective**: Emphasizes unconscious drives and conflicts.
3. **Behavioral Perspective**: Concentrates on observable behaviors.
4. **Cognitive Perspective**: Examines mental processes like thinking and problem-solving.
5. **Humanistic Perspective**: Stresses free will, conscious choices, and self-determination.""",
            
            "chapter2.md": """# Research Methods in Psychology

## The Scientific Method

Psychologists use the scientific method to conduct research:
1. Make observations
2. Form hypotheses
3. Test hypotheses through experiments or other studies
4. Analyze data
5. Draw conclusions
6. Report results

## Types of Research

### Experimental Research
Experiments involve manipulating one variable to determine if changes in one variable cause changes in another variable.

### Correlational Research
Correlational research examines the relationship between two or more variables without manipulation.

### Observational Research
Researchers observe behavior in natural environments without intervention.

## Ethical Considerations

Psychological research must follow ethical guidelines including informed consent, protection from harm, confidentiality, and debriefing.""",
            
            "chapter3.md": """# Biological Bases of Behavior

## Neurons

Neurons are specialized cells that transmit information throughout the nervous system. They consist of:
- Cell body (soma)
- Dendrites (receive signals)
- Axon (transmits signals)
- Synapses (connections between neurons)

## Nervous System

The nervous system is divided into:
1. **Central Nervous System (CNS)**: Brain and spinal cord
2. **Peripheral Nervous System (PNS)**: Nerves outside the CNS
   - Somatic nervous system (controls voluntary movements)
   - Autonomic nervous system (controls involuntary functions)
     * Sympathetic division (arousing)
     * Parasympathetic division (calming)

## Brain Structures

Key brain regions include:
- **Cerebral cortex**: Outer layer responsible for complex thought
- **Hippocampus**: Memory formation
- **Amygdala**: Emotional processing
- **Hypothalamus**: Homeostasis regulation
- **Cerebellum**: Motor coordination"""
        }
        
        # Write chapter files
        for filename, content in chapters.items():
            with open(os.path.join(course_dir, filename), "w") as f:
                f.write(content)
        
        # Create course metadata
        metadata = {
            "title": "Introduction to Psychology",
            "description": "An introductory course covering basic concepts in psychology",
            "chapters": list(chapters.keys())
        }
        
        with open(os.path.join(course_dir, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)
    
    def _process_courses(self):
        """Process all courses and create vector stores"""
        if not os.path.exists(self.settings.course_data_path):
            return
        
        for course_id in os.listdir(self.settings.course_data_path):
            course_path = os.path.join(self.settings.course_data_path, course_id)
            if os.path.isdir(course_path):
                self._process_course(course_id, course_path)
    
    def _process_course(self, course_id: str, course_path: str):
        """Process a single course"""
        documents = []
        
        # Load all markdown files in the course directory
        for filename in os.listdir(course_path):
            if filename.endswith(".md") and filename != "metadata.json":
                file_path = os.path.join(course_path, filename)
                with open(file_path, "r") as f:
                    content = f.read()
                
                # Create a Document object
                doc = Document(
                    page_content=content,
                    metadata={"course_id": course_id, "source": filename}
                )
                documents.append(doc)
        
        # Split documents into chunks
        split_documents = self.text_splitter.split_documents(documents)
        
        # Create or load vector store
        vector_store_path = os.path.join(self.settings.vector_store_path, course_id)
        if os.path.exists(vector_store_path):
            # Load existing vector store
            vector_store = FAISS.load_local(vector_store_path, self.embeddings)
        else:
            # Create new vector store
            vector_store = FAISS.from_documents(split_documents, self.embeddings)
            # Save vector store
            os.makedirs(vector_store_path, exist_ok=True)
            vector_store.save_local(vector_store_path)
        
        self.vector_stores[course_id] = vector_store
        
        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(search_kwargs={"k": 4}),
            return_source_documents=True
        )
        
        self.qa_chains[course_id] = qa_chain
    
    def answer_question(self, question: str, course_id: str = "intro-to-psychology") -> Tuple[str, List[str]]:
        """Answer a question using the RAG pipeline"""
        if course_id not in self.qa_chains:
            raise ValueError(f"Course {course_id} not found")
        
        # Get answer from QA chain
        result = self.qa_chains[course_id]({"query": question})
        answer = result["result"]
        
        # Extract source documents
        sources = [doc.metadata.get("source", "Unknown") for doc in result["source_documents"]]
        sources = list(set(sources))  # Remove duplicates
        
        return answer, sources

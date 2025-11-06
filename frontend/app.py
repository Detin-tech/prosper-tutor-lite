import streamlit as st
import requests
import os
from typing import Dict, Any

# App configuration
st.set_page_config(
    page_title="Prosper Tutor Lite",
    page_icon="🎓",
    layout="wide"
)

# API endpoint configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def query_api(query: str, course_id: str = "intro-to-psychology") -> Dict[str, Any]:
    """Send query to the API and return response"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/query",
            json={"query": query, "course_id": course_id},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")
        return {}
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return {}

def main():
    st.title("🎓 Prosper Tutor Lite")
    st.markdown("""
    Welcome to Prosper Tutor Lite - a lightweight version of ProsperChat!
    This demo showcases a RAG (Retrieval-Augmented Generation) pipeline with:
    - OpenStax-like course content
    - Vector database powered by FAISS
    - Integration with Ollama or OpenAI models
    """)
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    
    # Course selection
    course_options = {
        "Intro to Psychology": "intro-to-psychology"
    }
    selected_course_name = st.sidebar.selectbox(
        "Select Course",
        list(course_options.keys()),
        index=0
    )
    selected_course_id = course_options[selected_course_name]
    
    # Model information
    st.sidebar.info("""
    The backend supports both Ollama and OpenAI models.
    Configure your preference in the `.env` file.
    """)
    
    # Main interface
    st.subheader(f"Ask about {selected_course_name}")
    
    # Example questions
    example_questions = [
        "What are the major perspectives in psychology?",
        "Explain the scientific method in psychology research.",
        "Describe the structure of a neuron.",
        "What is the difference between sympathetic and parasympathetic nervous systems?"
    ]
    
    selected_example = st.selectbox(
        "Choose an example question or write your own below:",
        [""] + example_questions,
        format_func=lambda x: x if x else "Write your own question..."
    )
    
    # Question input
    question = st.text_input("Your Question:", value=selected_example, placeholder="Enter your question here...")
    
    # Submit button
    if st.button("Get Answer", type="primary") or (selected_example and st.button("Ask Example")):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                result = query_api(question, selected_course_id)
                
                if result:
                    # Display answer
                    st.subheader("Answer:")
                    st.write(result.get("answer", "No answer provided."))
                    
                    # Display sources
                    sources = result.get("sources", [])
                    if sources:
                        st.subheader("Sources:")
                        for source in sources:
                            st.markdown(f"- {source}")
                else:
                    st.error("Failed to get a response from the API.")
    
    # Additional information
    st.divider()
    st.markdown("""
    ### About this Demo
    
    This application demonstrates a simplified version of the ProsperChat architecture:
    1. **Data Processing**: Course content is split into chunks and embedded
    2. **Vector Storage**: Embeddings are stored in a FAISS vector database
    3. **Retrieval**: Relevant content is retrieved based on user queries
    4. **Generation**: An LLM generates answers based on retrieved context
    
    **Tech Stack:**
    - Backend: FastAPI
    - Frontend: Streamlit
    - Vector Store: FAISS
    - LLM: Ollama or OpenAI
    - Embeddings: sentence-transformers
    """)

if __name__ == "__main__":
    main()
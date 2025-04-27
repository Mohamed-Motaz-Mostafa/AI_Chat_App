# main file

# Import necessary libraries
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from rag import RAGSystem
from agent import AIAgent

from dotenv import load_dotenv

# Set OpenAI API key
print("OpenAI API Key status:", load_dotenv(dotenv_path=".env"))

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize RAG system and agent
rag_system = RAGSystem()
ai_agent = AIAgent()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    used_tools: List[str] = []

@app.post("/upload")
async def upload_document(file: UploadFile):
    """Endpoint to upload a document for processing."""
    result = await rag_system.process_document(file.file, file.filename)
    return result

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Endpoint to process a chat message and return a response."""
    # Retrieve relevant context from RAG
    context_docs = await rag_system.retrieve_context(request.message , 2)
    



    # Process the query using the agent
    result = ai_agent.process_query(request.message, context_docs)
    print("=============================**********************==================================")
    result = await result
    return ChatResponse(
        response=result["response"],
        used_tools=result["used_tools"]
    )


# Add this to your main.py in the FastAPI backend

@app.delete("/delete")
async def delete_documents():
    """Endpoint to delete all documents from the vector store."""
    try:
        # Reset the vector store
        rag_system.delete_vector_store()
        return {"status": "success", "message": "All documents have been deleted"}
    except Exception as e:
        return {"status": "error", "message": f"Error deleting documents: {str(e)}"}


@app.get("/documents")
async def get_documents():
    """Endpoint to get the list of documents in the vector store."""
    try:
        doc_summary = rag_system.get_docs_summary()
        # Convert to a list format that's easier to work with in frontend
        documents = [{"name": source, "chunks": count} for source, count in doc_summary.items()]
        return {"status": "success", "documents": documents}
    except Exception as e:
        return {"status": "error", "message": f"Error retrieving documents: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
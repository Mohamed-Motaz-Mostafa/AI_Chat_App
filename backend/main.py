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
    context_docs = await rag_system.retrieve_context(request.message)
    

    # print("***********************************************")
    # print("Context documents retrieved:", context_docs)
    # print("***********************************************")
    # print(request)
    # print("***********************************************")

    # Process the query using the agent
    result = ai_agent.process_query(request.message, context_docs)
    print("=============================**********************==================================")
    result = await result
    return ChatResponse(
        response=result["response"],
        used_tools=result["used_tools"]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
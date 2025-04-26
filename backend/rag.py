# RAG System

import os
import tempfile
from typing import List, Dict, Any
from langchain.document_loaders import TextLoader, PyPDFLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import TokenTextSplitter

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document

class RAGSystem:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None
        self.text_splitter = TokenTextSplitter(
            chunk_size=700,
            chunk_overlap=200
        )
    
    async def process_document(self, file, filename: str):
        """Process a document and store it in the vector database."""
        # Create a temporary file to store the uploaded content
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
            temp_file.write(await file.read())
            temp_path = temp_file.name
            # Because PyPDFLoader and TextLoader expect a file path, not a file object or bytes stream.
        
        try:
            # Load the document based on file type
            if filename.endswith('.pdf'):
                loader = PyPDFLoader(temp_path)
            else:  # Default to text
                loader = TextLoader(temp_path)
                
            documents = loader.load()
            
            # Split the documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            # Create or update the vector store
            if self.vector_store is None:
                self.vector_store = FAISS.from_documents(chunks, self.embeddings)
            else:
                self.vector_store.add_documents(chunks)
                
            return {"status": "success", "message": f"Document '{filename}' processed successfully"}
            
        except Exception as e:
            return {"status": "error", "message": f"Error processing document: {str(e)}"}
        finally:

            # Clean up the temporary file
            os.unlink(temp_path)
    
    async def retrieve_context(self, query: str, k: int = 5) -> List[Document]:
        """Retrieve relevant document chunks based on the query."""
        if self.vector_store is None:
            return []
        
        # Perform similarity search
        documents = self.vector_store.similarity_search(query, k=k)
        return documents
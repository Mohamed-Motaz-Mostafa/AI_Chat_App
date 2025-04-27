# RAG System

# import necessary libraries
import os
import tempfile
from typing import List, Dict, Any
from langchain_community.document_loaders import TextLoader , PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import TokenTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document


import shutil

class RAGSystem:
    def __init__(self):
        """
        Initialize the RAG system.
        This includes setting up the embedding model, vector store, and text splitter.
        TODO: Make it possible to set the embedding model and text splitter type from the frontend.
        """
        self.embeddings = OpenAIEmbeddings() # default embedding model "text-embedding-ada-002"
        self.vector_store = self.read_current_victor_store()
        self.text_splitter = TokenTextSplitter(
            chunk_size=700,
            chunk_overlap=200
        )
        self.doc_summary = self.get_docs_summary()

    def read_current_victor_store(self):

        """Read the current vector store from disk."""

        if os.path.exists("faiss_index"):
            self.vector_store = FAISS.load_local("faiss_index", self.embeddings, allow_dangerous_deserialization=True)
            print("Existing vector store loaded from disk.")
        else:
            print("No existing vector store found. A new one will be created.")
            self.vector_store = None
        return self.vector_store

    def get_docs_summary(self) -> dict:
        """Get a summary of the documents in the vector store."""
        if self.vector_store is None:
            return {"status": "No Data", "message": "No vector store found."}
        
        doc_summary = {}
        for doc_id, doc in self.vector_store.docstore._dict.items():
            source = doc.metadata.get('source', 'unknown').split("\\")[-1]
            
            if source not in doc_summary:
                doc_summary[source] = 0
            doc_summary[source] += 1

        print("\nDocument Summary:")
        for source, count in doc_summary.items():
            print(f"- {source}: {count} chunks")
        return doc_summary

    
    
    def delete_vector_store(self):
        """
        Delete the current vector store.
        This will remove the vector store file from disk.
        """
        if os.path.exists("faiss_index"):
            # change permissions to allow deletion
            os.chmod("faiss_index", 0o777)
            print("Deleting vector store...")
            # delete the vector store file
            shutil.rmtree("faiss_index")
            self.vector_store = None

            print("Vector store deleted.")
        else:
            print("No vector store found to delete.")

    async def process_document(self, file, filename: str) -> Dict[str, Any]:
        """Process a document and store it in the vector database.
        Args:
            file (file): The uploaded file object.
            filename (str): The name of the uploaded file.
        Returns:
                dict: A dictionary containing the status and message."""
        # Create a temporary file to store the uploaded content


        suff , pref = os.path.splitext(filename)

        with tempfile.NamedTemporaryFile(delete=False, suffix=suff , prefix=pref) as temp_file:
            temp_file.write(file.read())
            temp_path = temp_file.name
        
        try:
            # Load the document based on file type
            if filename.endswith('.pdf'):
                loader = PyPDFLoader(temp_path)
            else:  
                loader = TextLoader(temp_path)
                
            documents = loader.load()

            for doc in documents:
                doc.metadata["source"] = filename
                
            # Split the documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            # Create or update the vector store
            if self.vector_store is None:
                self.vector_store = FAISS.from_documents(chunks, self.embeddings)
            else:
                self.vector_store.add_documents(chunks)
                
            # save our vector store to disk with the new document
            self.vector_store.save_local("faiss_index")
                
            return {"status": "success", "message": f"Document '{filename}' processed successfully"}
            
        except Exception as e:
            return {"status": "error", "message": f"Error processing document: {str(e)}"}
        
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)
    


    async def retrieve_context(self, query: str, k: int = 5) -> List[Document]:
        """Retrieve relevant document chunks based on the query.
        Args:
            query (str): The query string to search for.
            k (int): The number of top results to return.
        Returns:
            List[Document]: A list of relevant document chunks.
        """

        if self.vector_store is None:
            return []
        
        # Perform similarity search
        documents = self.vector_store.similarity_search(query, k=k)
        return documents
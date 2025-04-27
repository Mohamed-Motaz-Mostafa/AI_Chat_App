# Agent file

# Import necessary libraries
from typing import List, Dict, Any
from langchain.schema import Document
from langchain_openai.chat_models import ChatOpenAI

from langchain.tools import BaseTool
from langchain.agents import AgentType, initialize_agent
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
# from langchain.chains import LLMChain

from tools.calculator import CalculatorTool



class AIAgent:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        self.tools = [CalculatorTool()]
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        # Initialize agent
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory
        )
    
    async def process_query(self, query: str, context_docs: List[Document] = None) -> Dict[str, Any]:
        """
        Process a query using the RAG context and agent tools.
        """
        try:
            # Prepare context from relevant documents
            context_text = ""
            if context_docs:
                context_text = "\n\n".join([doc.page_content for doc in context_docs])
            
            # Create system prompt with context
            if context_text:
                enriched_query = (
                    f"I have a question that may require information from these documents:\n\n"
                    f"{context_text}\n\n"
                    f"My question is: {query}"
                )
            else:
                enriched_query = query
            
            # Get response from the agent
            response = self.agent.run(input=enriched_query)
            
            return {
                "response": response,
                "used_tools": [tool.name for tool in self.tools if tool.name in str(self.agent.agent.llm_chain.prompt)]
            }
            
        except Exception as e:
            return {"response": f"Error processing query: {str(e)}", "used_tools": []}
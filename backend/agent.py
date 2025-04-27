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
from tools.currentDate import CurrentDateTool  # or wherever you save it



class AIAgent:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0, model="gpt-4o")
        self.tools = [CalculatorTool() , CurrentDateTool()]
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        # Initialize agent
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory,
            return_intermediate_steps=True
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
                    f"Context: {context_text} ... end of context\n\n"
                    f"If the question is related to math, ALWAYS use the calculator tool to calculate the answer, even simple qusitions like 1 + 1 \n"
                    f"If the context is not relevant to the question, please ignore it and answer the question directly.\n"
                    f"If the question is requiring a not provided context, please just say that you don't have the context to answer the question.\n\n"
                    f"My question is: {query} don't forget to use the calculator tool if its a math question.\n\n"
                )
            else:
                enriched_query = query
            
            # Get response from the agent
            full_response = self.agent.invoke({"input": enriched_query})
            print("Full response from agent:", full_response)
        
        # Extract used tools from intermediate steps
            used_tools = []
            if "intermediate_steps" in full_response:
                for step in full_response["intermediate_steps"]:
                    if len(step) >= 2 and hasattr(step[0], "tool"):
                        used_tools.append(step[0].tool)

            print("Used tools:", used_tools)
            
            return {
                "response": full_response.get("output", full_response.get("response")),
                "used_tools": used_tools
            }
        except Exception as e:
            return {"response": f"Error processing query: {str(e)}", "used_tools": []}
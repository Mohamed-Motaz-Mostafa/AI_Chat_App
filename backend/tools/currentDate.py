from datetime import datetime
from langchain.tools import BaseTool

class CurrentDateTool(BaseTool):
    name: str = "current_date"
    description: str = "Use this tool to get the current date. Useful if the user asks about today's date, or how old something is."

    def _run(self, query: str = "") -> str:
        # Return today's date
        return datetime.now().strftime("%Y-%m-%d")

    def _arun(self, query: str = "") -> str:
        raise NotImplementedError("This tool does not support async")

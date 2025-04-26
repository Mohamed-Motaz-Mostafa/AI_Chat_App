# Calculator Tool

import math
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type


class CalculatorInput(BaseModel):
    expression: str = Field(description="Mathematical expression to evaluate")

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Useful for performing mathematical calculations"
    args_schema: Type[BaseModel] = CalculatorInput
    
    def _run(self, expression: str) -> str:
        """Evaluate a mathematical expression."""
        try:
            # Add basic math functions to the locals
            local_dict = {
                'sqrt': math.sqrt,
                'pow': pow,
                'abs': abs,
                'round': round,
                'max': max,
                'min': min,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'pi': math.pi,
                'e': math.e,
                'log': math.log,
                'log10': math.log10,
                'floor': math.floor,
                'ceil': math.ceil
            }
            
            # Evaluate the expression with restricted globals and provided math functions
            result = eval(expression, {"__builtins__": {}}, local_dict)
            return str(result)
        except Exception as e:
            return f"Error evaluating expression: {str(e)}"

    async def _arun(self, expression: str) -> str:
        """Async version of _run."""
        return self._run(expression)
    

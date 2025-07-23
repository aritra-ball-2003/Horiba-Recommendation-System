from typing import Dict, Any
from .Base_agent import BaseAgent

class ScreenerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Screener",
            instructions = """Screen the customer needs Based on:
            - Requiremnt alignment
            - Relavent Solutions
            - Product Match as per requirement
            - Fitting Role of the product as per requirements
            - Provide instruction manual for installation and usage 
            Provide Comprehensive screening Reports """
        )

    async def run(self,messages:list)->Dict[str, Any]:
        """Screen the customer query"""
        print("Screen:Conduct initial Screening")

        workflow_context = eval(messages[-1]["Content"]) # LLm in conjection with the agent 
        screening_result = self._query_ollama(str(workflow_context)) # pass that into query ollama

        return {      # Returning the dictionary
            "screening_report": screening_result,
            "screening_timestamp":"2025-07-21",
            "screening_match_score": 85,

        }
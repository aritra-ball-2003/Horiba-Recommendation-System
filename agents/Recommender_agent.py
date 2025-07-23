from typing import Dict, Any
from .Base_agent import BaseAgent

class RecommenderAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Recommender",
            instructions= """Generate suitable recommendations considering:
            1. Extracted Requirement
            2. Requirement analysis
            3. product matches
            4. Screening results
            provide clear next steps and specific recommendations"""
        )
    async def run(self,messages:list)->Dict[str,Any]:
        """Generate suitable recommendations"""
        print("Recommender: Generating  recommendations")

        workflow_context = eval(messages[-1]["content"])   
        recommendation = self._query_ollama(str(workflow_context))

        return{
            "suitable_recommendation": recommendation,  # Dictionary
            "recommendation_timestamp": "2025-07-21",
            "confidence_level": "high",
        }
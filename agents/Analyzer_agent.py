from typing import Dict, Any
from .Base_agent import BaseAgent

class AnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Analyzer",
            instructions="""Analyze the customer's input for:
            - Specific technical or service-related requirements
            - Priority level (High/Medium/Low)
            - Potential product fit
            - Required support documents
            - Historical issue patterns (if any)
            Provide structured insights for customer personalization."""
        )

    async def run(self, messages: list) -> Dict[str, Any]:
        """Analyze the customer needs and context"""
        print("🔍 Analyzer: Analyzing customer request")

        workflow_context = eval(messages[-1]["content"])

        analysis_prompt = f"""
        Analyze this customer inquiry and return structured information:
        {{
            "requirements": ["requirement1", "requirement2"],
            "priority": "High/Medium/Low",
            "matching_products": ["ProductA", "ProductB"],
            "recommended_documents": ["Installation Guide", "Usage Manual"],
            "customer_patterns": ["frequent support", "connectivity issues"]
        }}

        Customer Input:
        {workflow_context}

        Return ONLY the JSON object, no extra text.
        """

        analysis_result = self._query_ollama(analysis_prompt)
        parsed_result = self._parse_json_safely(analysis_result)

        # Provide fallback defaults in case of parsing failure
        if "error" in parsed_result:
            parsed_result = {
                "requirements": [],
                "priority": "Low",
                "matching_products": [],
                "recommended_documents": [],
                "customer_patterns": [],
            }

        return {
            "screening_report": parsed_result,
            "Analysis_timestamp": "2025-07-21",
            "Analysis_match_score": 85 if "error" not in parsed_result else 50
        }

from typing import Dict, Any
from .Base_agent import BaseAgent

class MatcherAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name = "Matcher",
            instructions = """ Match customer requirement with suitable product 
            Consider : customer requirements, matching product details, pricing range, type of product and problem resolving solution 
            provide detailed reasoning as to why this will be the best product for the customer and compatibility scores
            Return matches in JSON format with title , match_scores and product fields """
        )
    async def run(self, messages:list) -> Dict[str,Any]:
        """ Match the customer requiremnts with the available products """
        print("Matcher: Finding suitable products")

        analysis_results = eval(messages[-1]["content"])

        sample_products = [
            {
                "title": "MicroSemi CRP LC-767g",
                "Description" : "Blood Sample Analysis",
                "Department": "Bio and HealthCare",
            },
            {
                "title": "OPSA 150",
                "Description": "Water testing",
                "Department": "Energy and environment",
            },
           
        ]   
        matching_response = self._query_ollama(
            f"""Analyze the customer requirement and provide the suitable product matches in valid JSON format: 
            Profile: {analysis_results['requirement_analysis']}
            Available Matches : {sample_products}

            Return ONLY a JSON object with this exact structure:
            {{
               "matched_products":[
                    {{
                       "title":"Solution title",
                       "match_score":"85%",
                       "type" : "Department"
                    }}
                ],
                "match_timestamp":"2025-07-21"
                "number_of_matches": 3
            }}"""    
        )

        # Parse the Response 

        parsed_response = self._parse_json_safely(matching_response)

        # Fall back to sample data if parsing fails 
        if "error" in parsed_response:
            return {
                "matched_products": [
                    {
                        "title": "MicroSemi CRP LC-767g",
                        "match_score":"85%",
                        "type": "Bio and HealthCare",

                    },
                    {
                        "title": "OPSA 150",
                        "match_score":"75%",
                        "type":"Energy and environment"
                    
                    }
                ],
                "match_timestamp": "2025-07-21",
                "number_of_matches": 3
            }
        return parsed_response 
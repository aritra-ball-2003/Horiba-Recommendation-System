from typing import Dict, Any
from .Base_agent import BaseAgent 
from .Extract_agent import ExtractAgent
from .Analyzer_agent import AnalyzerAgent
from .Matcher_agent import MatcherAgent
from .Screener_agent import ScreenerAgent
from .Recommender_agent import RecommenderAgent

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name = "Orchestrator",
            instructions = """Coordinate the requirement recommendation workflow and delegate tasks to specialized agents.
            Ensure proper flow of information between extraction, analysis, matching , screening, and recomendation phases
            Maintain context and agregate results from each stage.  """,
        )
        self._setup_agents()

    def _setup_agents(self):
        """Initialize all the specialized agents """
        self.extract = ExtractAgent()
        self.analyzer = AnalyzerAgent()
        self.matcher = MatcherAgent()
        self.screener = ScreenerAgent()
        self.recommender = RecommenderAgent()

    async def run(self,messages: list)-> Dict[str, Any]:
        """Process a single message through the agent"""
        prompt = messages[-1]["content"]
        response = self._query_ollama(prompt)
        return self._parse_json_safely(response)
    
    async def process_application(self, requirement_details: Dict[str,Any])->Dict[str,Any]:
        """Main workflow orchestrator for processing product requirement and support"""
        print ("Orchestrator: Starting application process")

        workflow_context = {
            "requirement_details" : requirement_details,
            "status": "initiated",
            "current_stage": "extraction",
        }  

        try: 
            # Extract the requirements Details 
            extracted_data = await self.extract.run(
                [{"role": "user", "content": str(requirement_details)}]
            )
            workflow_context.update(
                {"extracted_data": extracted_data, "current_stage": "analysis"}
            )

            # Analyze the customer requirement 
            analysis_results = await self.analyzer.run(
                [{"role":"user", "content": str(extracted_data)}]
            )
            workflow_context.update(
                {"analysis_result": analysis_results, "current_stage":"matching"}
            )

            # Match with products
            product_matches = await self.matcher.run(
                [{"role":"user","content":str(analysis_results)}]
            )
            workflow_context.update(
                {"product_matches":product_matches,"current_stage":"screening"}
            )
            
            # Screening Requirements
            screening_results = await self.screener.run(
                [{"role":"user","content": str(workflow_context)}]
            )
            workflow_context.update(
               {
                   "screening_results": screening_results,
                   "current_stage": "recommendation",
               } 
            )

            # Generate Recommendation
            suitable_recommendation = await self.recommender.run(
                [{"role":"user","content": str(workflow_context)}]
            )
            workflow_context.update(
                {"suitable_recommendation":suitable_recommendation,"status":"completed"}
            )

            return workflow_context
        
        except Exception as e:
            workflow_context.update({"status":"failed", "error": str(e)})
            raise
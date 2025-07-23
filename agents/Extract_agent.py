from typing import Dict, Any
from pdfminer.high_level import extract_text 
from .Base_agent import BaseAgent

# Needs Very consise information
class ExtractAgent (BaseAgent):
    def __init__(self):         
        super().__init__(
            name = "Extractor",
            instructions ="""Extract and structure information from the customer
            Focus on: Customer Requirement, product recommendation, suitable products , solutions, pricing comparison,personal assistant, installment process and help/Support
            Provide output in a clear structured format.  """
        )

    async def run(self, messages:list)-> Dict[str,Any]: 
        """Process the Given input and extract information""" 
        print("Extractor: Processing requirements")
        
        requirements_data = eval(messages[-1]["content"])

        #Extract text from borchure pdf
        if requirements_data.get("file_path"):
            raw_text= extract_text(requirements_data["file_path"])
        else:
            raw_text = requirements_data.get("text", "")    

        extracted_info = self._query_ollama(raw_text)

        return {
            "raw_text": raw_text,
            "structured_data": extracted_info,
            "extraction_status": "completed"
        }    

from typing import Dict, Any
import json 
from openai import OpenAI


class BaseAgent:
    def __init__(self,name:str,instructions: str):
        self.name = name
        self.instructions = instructions # we are using swarms with openAi but overriding it with ollama specifically llama models 
        self.ollama_client = OpenAI(         # Within the ollama client we are passing the openAi pipeline 
            base_url = "http://localhost:11434/v1",
            api_key = "ollama", # Required but unused 
        )
# for getting the messages 
    async def run(self,messages:list)-> Dict[str,Any]:
        """Default run method to be overridden by child classes"""
        raise NotImplementedError("subclasses must implement run ()")
    
    def _query_ollama(self, prompt:str)->str:
        """Query Ollama model with the given prompt"""
        try:
            response = self.ollama_client.chat.completions.create(
                model = "llama3.2:latest", # model updated to llama3.1:70b
                messages=[
                    {"role":"system","content":self.intructions},     # these are the messages system and role and contents
                    {"role":"user","content":prompt},
                ],
                temperature=0.7,
                max_tokens=2000,
            )
            return response.choices[0].message.content   # Return the response 
        except Exception as e:
            print(f"Error quering Ollama:{str(e)}")
            raise

    def _parse_json_safely(self,text:str)->Dict[str,Any]:
        """Safely parse JSON from text, handling potential errors"""
        try:
            # Try to find JSON-like content between curly brces
            start = text.find("{")
            end = text.rfind("}")
            if start !=-1 and end != -1:
                json_str = text[start: end + 1]
                return json.loads(json_str)   # for loading file json
            return {"error":"No JSON content found"}
        except json.JSONDecodeError:
            return {"error":"Invalid JSON content"}    
            
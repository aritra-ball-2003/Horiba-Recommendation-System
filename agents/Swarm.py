# Swarm.py
from openai import OpenAI

class Agent:
    def __init__(self, name, model, instructions, functions=None):
        self.name = name
        self.model = model
        self.instructions = instructions
        self.functions = functions or []

    @staticmethod
    def call_model(model: str, prompt: str, stream: bool = False):
        client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        )
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            stream=stream,
        )
        return {"response": response.choices[0].message.content}


class Swarm:
    def __init__(self, client):
        self.client = client

    def run(self, agent, messages, context_variables=None, stream=False, debug=False):
        response = self.client.chat.completions.create(
            model=agent.model,
            messages=[
                {"role": "system", "content": agent.instructions},
                *messages
            ],
            temperature=0.7,
            stream=stream,
        )
        return type("Response", (), {
            "messages": [{"role": "assistant", "content": response.choices[0].message.content}],
            "agent": agent  # assumes no agent switching
        })

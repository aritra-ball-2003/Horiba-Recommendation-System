from typing import Dict, Any
from Swarm import Agent

# Function that lets the LLM handle the full customer interaction
def customer_assistant_function(user_input: Dict[str, Any]) -> Dict[str, Any]:
    customer_query = user_input.get("query", "")
    product = user_input.get("product", "our product")

    # Construct prompt for LLM to act like a helpful support assistant
    prompt = (
        f"You are a friendly and professional customer support assistant for a product-based company.\n"
        f"The customer is asking about: {customer_query}\n"
        f"Product in question: {product}.\n\n"
        "Respond in simple, helpful language. Provide steps if it's a how-to or issue. "
        "If the problem needs escalation, kindly tell the customer a human agent will follow up."
    )

    return {
        "response": Agent.call_model(
            model="llama3.2",
            prompt=prompt,
            stream=False
        ).get("response", "I'm here to help! Could you please provide more details?")
    }


# Define the assistant agent
customer_assistant_agent = Agent(
    name="Customer Assistant Agent",
    model="llama3.2",
    instructions="Act as a personal customer support assistant for a product company. Respond directly to customer queries with helpful answers.",
    functions=[customer_assistant_function],
)

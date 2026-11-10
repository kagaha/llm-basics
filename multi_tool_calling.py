
import json
from datetime import datetime
from google import genai
from dotenv import load_dotenv
from tool_calling import get_current_temperature

load_dotenv()  # Load environment variables from .env file
client = genai.Client()




def calculate_sum(a: float, b: float):
    return {"result": a + b}


def get_current_time(location: str):
    return {
        "location": location,
        "time": datetime.now().strftime("%H:%M:%S")
    }


# Function registry
available_functions = {
    "get_current_temperature": get_current_temperature,
    "calculate_sum": calculate_sum,
    "get_current_time": get_current_time,
}


# Tool declarations
tools = [
    {
        "type": "function",
        "name": "get_current_temperature",
        "description": "Get the current temperature for a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    },
    {
        "type": "function",
        "name": "calculate_sum",
        "description": "Calculate the sum of two numbers.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["a", "b"]
        }
    },
    {
        "type": "function",
        "name": "get_current_time",
        "description": "Get the current time for a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }
]


# Runtime input
while True:

    user_prompt = input("\nYou: ")

    if user_prompt.lower() == "exit":
        break

    # First interaction
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=user_prompt,
        tools=tools
    )

    # Keep executing tools until Gemini produces
    # a final response without another function call.
    while True:

        function_results = []

        for step in interaction.steps or []:

            if step.type == "function_call":

                function_name = step.name
                arguments = step.arguments

                print(f"\nCalling tool: {function_name}")
                print(f"Arguments: {arguments}")

                # Find and execute Python function
                function = available_functions.get(function_name)

                if function is None:
                    result = {"error": "Unknown function"}
                else:
                    try:
                        result = function(**arguments)
                    except Exception as e:
                        result = {"error": str(e)}

                print(f"Tool Result: {result}")

                # Prepare result for Gemini
                function_results.append({
                    "type": "function_result",
                    "name": function_name,
                    "call_id": step.id,
                    "result": [
                        {
                            "type": "text",
                            "text": json.dumps(result)
                        }
                    ]
                })

        # No more function calls: final response received
        if not function_results:
            break

        # Send function results back to Gemini
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            previous_interaction_id=interaction.id,
            tools=tools,
            input=function_results
        )

    print("\nGemini:", interaction.output_text)

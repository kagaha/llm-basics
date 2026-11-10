import json
from google import genai
from dotenv import load_dotenv
import requests

load_dotenv()  # Load environment variables from .env file



# Tool Calling / Function Calling
weather_function = {
    "type": "function",
    "name": "get_current_temperature",
    "description": "Gets the current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name, e.g. San Francisco",
            },
        },
        "required": ["location"],
    },
}

# Define the function that will be called by the model - The Actual implementation of the function that fetches the current temperature
# for a given location using the Open-Meteo API.
def get_current_temperature(location):

    geo_url= "https://geocoding-api.open-meteo.com/v1/search"
    geo_response = requests.get(geo_url, params={"name": location,"count": 1},  timeout=10)
    geo_response.raise_for_status()
    geo_data = geo_response.json()

    if not geo_data.get("results"):
        raise ValueError(f"No geocoding results found for location: {location}")

    city_info = geo_data["results"][0]
    latitude = city_info["latitude"]
    longitude = city_info["longitude"]

    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_response = requests.get(weather_url, params={"latitude": latitude, "longitude": longitude, "current_weather": True}, timeout=10)
    weather_response.raise_for_status()
    weather_data = weather_response.json()

    temperature = weather_data.get("current_weather", {}).get("temperature")
    return {
        "location": location,
        "temperature": temperature,
        "unit": "Celsius"
    }

if __name__ == "__main__":

    client = genai.Client()
    # ---- The problem - model has no access to real-time data ----
    result = client.interactions.create(
        model = "gemini-3.6-flash",
        input="What is the temperature in London?"
    )

    print(result.output_text)
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input="What's the temperature in London?",
        tools=[weather_function],
    )

    # Process the interaction steps - To Print what function the model wants to call and the arguments it wants to pass
    for step in interaction.steps:
        if step.type == "function_call":
            print(f"Function to call: {step.name}")
            print(f"Arguments: {step.arguments}")

            if step.name == "get_current_temperature":
                # Call the actual function with the provided arguments
                weather_result =  get_current_temperature(step.arguments["location"])
                print(f"Weather Result: {weather_result}")
                # pass the result back to the model for final response generation
                final_interaction = client.interactions.create(
                    model="gemini-3.6-flash",
                    previous_interaction_id=interaction.id,
                    tools=[weather_function],
                    input=[
                        {
                            "type": "function_result",
                            "name": step.name,
                            "call_id": step.id,
                            "result": [
                                {
                                    "type": "text",
                                    "text": json.dumps(weather_result)
                                }
                            ]
                        }
                    ]
                )
            print(f"Final Response: {final_interaction.output_text}")
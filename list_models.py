
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing")

client = genai.Client(api_key=api_key)

print("\nAvailable Gemini Models:\n")

for model in client.models.list():
    print("Model:", model.name)
    print("Display Name:", model.display_name)
    print("Input Limit:", model.input_token_limit)
    print("Output Limit:", model.output_token_limit)
    print("-" * 50)

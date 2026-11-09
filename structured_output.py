from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()  # Load environment variables from .env file

client = genai.Client()

# Here's an example of the unstructured output from the model
response = client.interactions.create(
    model="gemini-3.6-flash",
    system_instruction="You are an helpful assistant",
    input="Give me the name, age and city of an random person"
)
print(response.output_text)
print(type(response.output_text))  # This will print the type of the output text

# Here is a randomly generated profile:

# * **Name:** Marcus Vance
# * **Age:** 32
# * **City:** Seattle, Washington
# <class 'str'>


# Naive Fix - Ask Agent to return structured output in JSON format
response = client.interactions.create(
    model="gemini-3.6-flash",
    system_instruction="You are an helpful assistant. Please provide the output in JSON format with keys: name, age, city.",
    input="Give me the name, age and city of a random person"
)
print(response.output_text)
print(type(response.output_text))  # This will print the type of the output text
# Sample Output:```json
# {
#   "name": "Elena Rostova",
#   "age": 28,
#   "city": "Prague"
# }
# ```
# <class 'str'>

# Sometimes works, but the model might wrap it in ```json ``` blocks
# or change the key names, or add extra fields
# Not reliable enough for production


class Person(BaseModel):
    name: str
    age: int
    city: str


response = client.interactions.create(
    model="gemini-3.6-flash",
    system_instruction="You are an helpful assistant.",
    input="Give me the name, age and city of a random person",
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": Person.model_json_schema()
    }
)

person = Person.model_validate_json(response.output_text)  # Validate and parse the JSON response into a Person object
print(person)
print(type(person))  # This will print the type of the person object
print(f"Name: {person.name}, Age: {person.age}, City: {person.city}")

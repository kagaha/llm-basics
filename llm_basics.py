from google import genai
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# ---- 1. Create a client ----
client = genai.Client()


# ---- 2. Generate content ----
response = client.models.generate_content(
    model='gemini-3.6-flash',
    contents='What is the square root of 25?'
)
# print the entire response object
print(response);


# ---- 3. Extract just the text ----
print(response.text)

# ---- 4. Multi-turn conversation (stateful conversation) Passing the previous interaction ID to the next interaction ----
# First Iteration
interaction1 = client.interactions.create(
    model="gemini-3.6-flash",
    input="My name is Ruthik"
);
print(interaction1.output_text)
## Second Iteration
result = client.interactions.create(
    model="gemini-3.6-flash",
    input="What is my name?",
    previous_interaction_id=interaction1.id
);
print(result.output_text)

# --- Stateless conversation (without passing the previous interaction ID)  Managing the
# conversation history by ourselves through DB and passing the history to the Model  ----
history = [
    {"role": "user", "content": "My name is Ruthik"},
    {"role": "assistant", "content": "Hello Ruthik! How can I assist you today?"}
];

# Get user input
user_input = input("You: ")

# Append the user input to the conversation history
history.append({"role": "user", "content": user_input})

# Convert history into a text prompt
conversation = "\n".join(
    f"{message['role']}: {message['content']}"
    for message in history
)

response = client.interactions.create(
    model="gemini-3.6-flash",
    input=conversation
);

print("Assistant:" , response.output_text)
# Append the assistant's response to the conversation history
history.append({"role": "assistant", "content": response.output_text})


# ---- 5. Now add system prompt, temperature, max_tokens ----
result = client.interactions.create(
    model="gemini-3.6-flash",
    system_instruction="You are a helpful assistant who makes jokes.",
    input="What is the square root of 49?",
    generation_config={
        "max_output_tokens": 500,
        "temperature":0.7
    }
)

print(result.output_text)

# ---- 6. Token usage ----
print(f"Input tokens: {result.usage.total_input_tokens}")
print(f"Output tokens: {result.usage.total_output_tokens}")
print(f"Total tokens: {result.usage.total_tokens}")


# # ---- 7. Streaming ----
stream = client.interactions.create(
    model="gemini-3.8-flash",
    system_instruction="You are a helpful assistant.",
    input="Tell me a short story about a robot.",
    stream=True
)

# Iterate through the Server-Sent Events (SSE) from the stream
for event in stream:
    # Safely extract text updates from the delta events
    if event.event_type == "step.delta" and event.delta.type == "text":
        print(event.delta.text, end="", flush=True)


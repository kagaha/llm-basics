# LLM Basics: Gemini API, Tool Calling and Structured Output

Small, runnable Python scripts that cover the core building blocks of working with a Large Language Model through its API. Each script is self-contained and commented, and the scripts build on each other from a first API call to a multi-tool agent loop.

Built with the Google Gemini API (`google-genai` SDK).

## What's covered

| Script | Concept | What it demonstrates |
|---|---|---|
| `list_models.py` | API access | Authenticating with an API key and listing the available models with their input/output token limits |
| `llm_basics.py` | LLM fundamentals | Creating a client, generating content, stateful vs. stateless multi-turn conversations, system prompts, `temperature` and `max_output_tokens`, token usage, and streaming responses |
| `structured_output.py` | Structured output | Moving from free text, to "please return JSON" prompting, to schema-enforced JSON validated with a Pydantic model |
| `tool_calling.py` | Tool / function calling | Declaring a function for the model, executing the call it requests (a live weather lookup through the Open-Meteo API), and returning the result for the final answer |
| `multi_tool_calling.py` | Multi-tool agent loop | An interactive loop with several tools (weather, current time, sum), a function registry, error handling for unknown tools, and repeated tool execution until the model gives a final answer |

## Key ideas shown

- **Stateful vs. stateless chat:** passing a previous interaction ID versus managing the conversation history yourself.
- **Why prompt-only JSON is fragile:** the model may wrap the JSON in code fences or change key names, so a response schema plus Pydantic validation is used instead.
- **The tool-calling cycle:** the model *requests* a function call, your code *executes* it, and the result is sent back for the model to turn into a natural-language answer.
- **Agent loop:** keep executing tool calls until a response contains no further function calls.
## Getting started

### Prerequisites
- Python 3.10+
- A Google AI (Gemini) API key
### Setup

```bash
git clone https://github.com/kagaha/llm-basics.git
cd llm-basics

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install google-genai python-dotenv pydantic requests
```

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_api_key_here
```

### Run

```bash
python list_models.py            # see which models your key can use
python llm_basics.py             # fundamentals: chat, system prompt, tokens, streaming
python structured_output.py      # free text vs. JSON vs. schema-validated output
python tool_calling.py           # single tool: live temperature lookup
python multi_tool_calling.py     # interactive multi-tool loop (type 'exit' to quit)
```

Example prompts for `multi_tool_calling.py`:
- `What's the temperature in Hyderabad?`
- `What is 1234.5 plus 678.9?`
- `What's the temperature in Paris and what is 12 + 30?`
## Notes

- The model name is set in each script (`gemini-3.6-flash`); change it if your account uses a different model. `list_models.py` shows what is available.
- Never commit your `.env` file. It is already in `.gitignore`.
- `get_current_time` in the multi-tool demo returns the local machine time and does not look up the city's time zone.
## Next step

These fundamentals are applied in [`basic-rag`](https://github.com/kagaha/basic-rag), a Retrieval-Augmented Generation app with ChromaDB and conversation memory.
 
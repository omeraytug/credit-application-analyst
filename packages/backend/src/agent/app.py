import os
from pathlib import Path

from dotenv import load_dotenv
from strands import Agent, tool
from strands.handlers.callback_handler import null_callback_handler
from strands.models import OpenAIModel
from strands_tools.calculator import calculator
from strands_tools.current_time import current_time

load_dotenv(Path(__file__).resolve().parents[4] / ".env")


@tool
def letter_counter(text: str) -> int:
    """Count alphabetic characters in the given text."""
    return sum(c.isalpha() for c in text)


agent = Agent(
    name="MyAgent",
    # Suppress "Tool #1: ..." and streamed tokens; tools still run internally.
    callback_handler=null_callback_handler,
    model=OpenAIModel(
        model_id="gpt-4o",
        client_args={"api_key": os.getenv("OPENAI_API_KEY")},
        params={"max_tokens": 1000, "temperature": 0.7},
    ),
    tools=[calculator, current_time, letter_counter],
)

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    response = agent(user_input)
    print(f"\nAgent:\n{response}\n")

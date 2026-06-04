import os
from strands import Agent
from strands.tools import CalculatorTool, TimeTool, LetterCounterTool
from strands.models import OpenAIModel  

agent = Agent(
    name="MyAgent",
    model=OpenAIModel(
        model_id="gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY"),
        max_tokens=1000,
        temperature=0.7
    ),
    tools=[CalculatorTool(), TimeTool(), LetterCounterTool()]
)

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    
    response = agent.run(user_input)
    print(f"\nAgent:\n{response.content}\n")
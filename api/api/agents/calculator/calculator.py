import os
import nest_asyncio
from utils.calculator_tool_spec import CalculatorToolSpec

from llama_index.llms.openai import OpenAI
from llama_index.agent.openai import OpenAIAgent


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

nest_asyncio.apply()

llm = OpenAI(model="gpt-4o")

tool_spec = CalculatorToolSpec()
agent = OpenAIAgent.from_tools(
    tool_spec.to_tool_list(), llm=llm, verbose=True)

response = agent.chat(
    "What is 10!", tool_choice="auto"
)

print(response.sources)

import nest_asyncio
import json
from typing import Sequence, List
from utils import add, multiply, divide, subtract


from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage
from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.agent.openai import OpenAIAgent

import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

nest_asyncio.apply()

llm = OpenAI(model="gpt-3.5-turbo-0613")

add_tool = FunctionTool.from_defaults(fn=add)
multiply_tool = FunctionTool.from_defaults(fn=multiply)
divide_tool = FunctionTool.from_defaults(fn=divide)
subtract_tool = FunctionTool.from_defaults(fn=subtract)


agent = OpenAIAgent.from_tools(
    [add_tool, multiply_tool, divide_tool, subtract_tool], llm=llm, verbose=True)

response = agent.chat(
    "What is (5 - 2) * 5", tool_choice="auto"
)

print(response)

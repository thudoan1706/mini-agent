from llama_index.vector_stores.pinecone import PineconeVectorStore
import os
import nest_asyncio
from utils.calculator_tool_spec import CalculatorToolSpec
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.agent.openai import OpenAIAgent
from pinecone import Pinecone, ServerlessSpec
from llama_index.core.objects import ObjectIndex
from llama_index.core import StorageContext
from llama_index.core.objects import SimpleToolNodeMapping
from llama_index.core import VectorStoreIndex
from llms.llama_index.vector_store.pinecone.client import PineconeClient


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

nest_asyncio.apply()

llm = OpenAI(model="gpt-4o")
calculator_spec = CalculatorToolSpec()
pc = PineconeClient("arithmetic-tools", calculator_spec.to_tool_list())
object_index = pc.load_func_tools_indices()
# object_index = pc.create_func_tools_indices()
agent = OpenAIAgent.from_tools(
    tool_retriever=object_index.as_retriever(similarity_top_k=2), verbose=True
)

response = agent.chat("What's the factorial of 10? Make sure to use Tools")
print(response)

import nest_asyncio
from utils.calculator_tool_spec import CalculatorToolSpec
from llama_index.llms.openai import OpenAI
from llama_index.agent.openai import OpenAIAgent
from llms.llama_index.vector_store.pinecone.client import PineconeClient
import os


class ArithmeticAgent:
    def __init__(self, collection_name, model_name="gpt-4o"):
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        nest_asyncio.apply()

        # Initialize LLM and tool specifications
        self.llm = OpenAI(model=model_name)
        self.calculator_spec = CalculatorToolSpec()
        self.pc = PineconeClient(collection_name)

    def create_indices(self):
        """Create vector index and upload onto Pinecone."""
        return self.pc.upsert_indices(self.calculator_spec.to_tool_list())

    def ask_question(self, question):
        """Ask a question to the agent."""
        object_index = self.pc.load_indices(
            self.calculator_spec.to_tool_list())
        agent = OpenAIAgent.from_tools(
            tool_retriever=object_index.as_retriever(similarity_top_k=2),
            verbose=True
        )
        return agent.chat(question)


if __name__ == "__main__":
    ai_agent = ArithmeticAgent("arithmetic-tools")

    # ai_agent.create_indices()

    response = ai_agent.ask_question(
        "What's the factorial of 10? Make sure to use Tools")
    print(response)

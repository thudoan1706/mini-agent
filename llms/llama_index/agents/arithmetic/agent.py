import pandas as pd
import os
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
import nest_asyncio
from utils.calculator_tool_spec import CalculatorToolSpec
from llama_index.llms.openai import OpenAI
from llms.llama_index.vector_store.pinecone.client import PineconeClient
from llama_index.packs.agents_coa import CoAAgentWorker
import phoenix as px
import llama_index.core
from llms.llama_index.output_parser.arithmetic.output_parser import CustomChainOfAbstractionParser
from llama_index.postprocessor.colbert_rerank import ColbertRerank
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.postprocessor.cohere_rerank import CohereRerank


api_key = os.environ["COHERE_API_KEY"]

pd.set_option("display.max_colwidth", 1000)

# Setup the OTLP exporter and tracing provider
endpoint = "http://127.0.0.1:6006/v1/traces"  # Phoenix receiver address

tracer_provider = trace_sdk.TracerProvider()
tracer_provider.add_span_processor(
    SimpleSpanProcessor(OTLPSpanExporter(endpoint)))
LlamaIndexInstrumentor().instrument(
    tracer_provider=tracer_provider,
    use_legacy_callback_handler=True,
)

llama_index.core.set_global_handler("arize_phoenix")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
nest_asyncio.apply()


class ArithmeticAgent:
    def __init__(self, collection_name, model_name="gpt-4o"):
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
        cohere_rerank = CohereRerank(
            model="rerank-english-v3.0", api_key=api_key, top_n=5)

        worker = CoAAgentWorker.from_tools(
            tool_retriever=object_index.as_retriever(
                similarity_top_k=7, node_postprocessors=[cohere_rerank]
            ),
            output_parser=CustomChainOfAbstractionParser(verbose=True),
            llm=self.llm,
            verbose=True,
        )

        agent = worker.as_agent()

        return agent.chat(question)


if __name__ == "__main__":
    ai_agent = ArithmeticAgent("arithmetic-tools")

    # ai_agent.create_indices()
    # response = ai_agent.ask_question("what is (1 + 1) + (1 + 1)")

    response = ai_agent.ask_question(
        """
        A 65-year-old male patient is being assessed for the risk of major bleeding using the HEMORR2HAGES score. The patient has the following medical history and characteristics:

        1. Hepatic or renal disease: Yes (1 point)
        2. Ethanol abuse: No (0 points)
        3. Malignancy: Yes (1 point)
        4. Older age (≥75 years): No (0 points)
        5. Reduced platelet count or function: Yes (1 point)
        6. Rebleeding risk: Yes (2 points)
        7. Hypertension (uncontrolled, >160 mmHg systolic): Yes (1 point)
        8. Anemia: No (0 points)
        9. Genetic factors (e.g., CYP2C9 variants): No (0 points)
        10. Excessive fall risk: Yes (1 point)
        11. Stroke: Yes (1 point)

        Using the HEMORR2HAGES criteria, calculate the patient's total score to determine their risk of major bleeding.
        """
    )
    print(response)
    px.active_session()

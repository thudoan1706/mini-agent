from llama_index.vector_stores.pinecone import PineconeVectorStore
import os
from typing import List
from utils.calculator_tool_spec import CalculatorToolSpec
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.agent.openai import OpenAIAgent
from pinecone import Pinecone, ServerlessSpec
from llama_index.core.objects import ObjectIndex
from llama_index.core import StorageContext
from llama_index.core.objects import SimpleToolNodeMapping

from llama_index.core import VectorStoreIndex

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "")

PINECONE_CLIENT = Pinecone(PINECONE_API_KEY)


class PineconeClient:
    """
    Upload indices of tools and documents into Pinecone
    """

    def __init__(self, collection_name, tool_lists):
        """
        Initialize the PineconeClient.

        :param collection_name: Name of the Pinecone collection.
        :param tool_lists: List of tools to be indexed.
        """
        self.collection_name = collection_name
        self.tool_lists = tool_lists

        self.vector_store = PineconeVectorStore(
            pinecone_index=PINECONE_CLIENT.Index(collection_name))
        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store)
        self.index = VectorStoreIndex.from_vector_store(
            vector_store=self.vector_store)

    def load_func_tools_indices(self):
        """
        Load function tools indices from the existing index.

        :return: ObjectIndex created from tool_lists and the index.
        """
        object_index = ObjectIndex.from_objects_and_index(
            self.tool_lists, self.index)
        return object_index

    def create_func_tools_indices(self):
        """
        Create vector index and upload onto Pinecone.

        :return: ObjectIndex created from tool_lists, mapping, and storage context.
        """
        object_mapping = SimpleToolNodeMapping.from_objects(self.tool_lists)
        object_index = ObjectIndex.from_objects(
            self.tool_lists,
            object_mapping=object_mapping,
            index_cls=VectorStoreIndex,
            storage_context=self.storage_context,
        )
        return object_index

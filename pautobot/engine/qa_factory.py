from chromadb.config import Settings
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

from pautobot.engine.bot_context import BotContext


class QAFactory:
    """Factory for instantiating QAs."""

    @staticmethod
    def create_qa(
        context: BotContext,
        llm,
    ):
        chroma_settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=context.search_db_directory,
            anonymized_telemetry=False,
        )
        embeddings = HuggingFaceEmbeddings(
            model_name=context.embeddings_model_name
        )
        database = Chroma(
            persist_directory=context.search_db_directory,
            embedding_function=embeddings,
            client_settings=chroma_settings,
        )
        retriever = database.as_retriever(search_kwargs={"k": 4})
        qa_instance = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
        )
        return qa_instance

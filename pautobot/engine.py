import os

from chromadb.config import Settings

from pautobot.bot_enums import BotMode, BotStatus
from pautobot.llm_factory import LLMFactory, QAFactory
from pautobot.ingest import ingest_documents
from pautobot.utils import intialize_model


class PautoBotEngine:
    """PautoBot engine for answering questions."""

    def __init__(self, mode, model_type="GPT4All") -> None:
        self.mode = mode
        self.model_type = model_type
        self.current_answer = {
            "status": BotStatus.READY,
            "answer": "",
            "docs": [],
        }

        self.data_root_directory = os.path.abspath(
            os.path.join(os.path.expanduser("~"), "pautobot-data")
        )
        self.documents_directory = os.path.join(
            self.data_root_directory, "documents"
        )
        self.persist_directory = os.path.join(
            self.data_root_directory, "database"
        )
        self.model_path = os.path.join(
            self.data_root_directory,
            "models",
            "ggml-gpt4all-j-v1.3-groovy.bin",
        )
        intialize_model(self.model_path)
        self.model_n_ctx = 1000
        self.embeddings_model_name = "all-MiniLM-L6-v2"

        # Prepare the LLM
        self.llm = LLMFactory.create_llm(
            model_type=self.model_type,
            model_path=self.model_path,
            model_n_ctx=self.model_n_ctx,
            streaming=False,
            verbose=False,
        )

        # Prepare the retriever
        self.qa_instance = None
        self.qa_instance_error = None
        if mode == BotMode.CHAT:
            return

        # Define the Chroma settings
        self.chroma_settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=self.persist_directory,
            anonymized_telemetry=False,
        )

        # Prepare the QA
        try:
            self.qa_instance = QAFactory.create_qa(
                chroma_settings=self.chroma_settings,
                persist_directory=self.persist_directory,
                llm=self.llm,
                embeddings_model_name=self.embeddings_model_name,
            )
        except Exception as e:
            print(f"Error while initializing retriever: {e}")
            print("Switching to chat mode...")
            self.qa_instance_error = "Error while initializing retriever!"

    def ingest_documents(self):
        ingest_documents(
            self.documents_directory,
            self.persist_directory,
            self.chroma_settings,
            self.embeddings_model_name,
        )

    def check_query(self, mode, query):
        if mode == BotMode.QA and self.mode == BotMode.CHAT:
            raise Exception(
                "PautobotEngine was initialized in chat mode! "
                "Please restart in QA mode."
            )
        elif mode == BotMode.QA and self.qa_instance is None:
            raise Exception(self.qa_instance_error)

    def query(self, mode, query):
        self.check_query(mode, query)
        if mode is None:
            mode = self.mode
        if mode == BotMode.QA and self.qa_instance is None:
            print(self.qa_instance_error)
            mode = BotMode.CHAT
        self.current_answer = {
            "status": BotStatus.THINKING,
            "answer": "",
            "docs": [],
        }
        if mode == BotMode.QA:
            try:
                print("Received query: ", query)
                print("Thinking...")
                res = self.qa_instance(query)
                answer, docs = (
                    res["result"],
                    res["source_documents"],
                )
                doc_json = []
                for document in docs:
                    doc_json.append(
                        {
                            "source": document.metadata["source"],
                            "content": document.page_content,
                        }
                    )
                self.current_answer = {
                    "status": BotStatus.READY,
                    "answer": answer,
                    "docs": doc_json,
                }
            except Exception as e:
                print("Error during thinking: ", e)
                answer = "Error during thinking! Please try again."
                if "Index not found" in str(e):
                    answer = "Index not found! Please ingest documents first."
                self.current_answer = {
                    "status": BotStatus.READY,
                    "answer": answer,
                    "docs": None,
                }
        else:
            try:
                print("Received query: ", query)
                print("Thinking...")
                answer = self.llm(query)
                self.current_answer = {
                    "status": BotStatus.READY,
                    "answer": answer,
                    "docs": None,
                }
            except Exception as e:
                print("Error during thinking: ", e)
                self.current_answer = {
                    "status": BotStatus.READY,
                    "answer": "Error during thinking! Please try again.",
                    "docs": None,
                }

    def get_answer(self):
        return self.current_answer

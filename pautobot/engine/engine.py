import logging
import os
import traceback

from pautobot import db_models
from pautobot.config import DATA_ROOT
from pautobot.database import session
from pautobot.engine.bot_enums import BotMode, BotStatus
from pautobot.engine.chatbot_factory import ChatbotFactory
from pautobot.engine.context_manager import ContextManager
from pautobot.engine.ingest import ingest_documents
from pautobot.engine.llm_factory import LLMFactory
from pautobot.engine.qa_factory import QAFactory


class PautoBotEngine:
    """PautoBot engine for answering questions."""

    def __init__(
        self, mode, context_manager: ContextManager, model_type="GPT4All"
    ) -> None:
        self.mode = mode
        self.model_type = model_type
        self.model_path = os.path.join(
            DATA_ROOT,
            "models",
            "ggml-gpt4all-j-v1.3-groovy.bin",
        )
        self.context_manager = context_manager
        if not self.context_manager.get_contexts():
            raise ValueError(
                "No contexts found! Please create  at least one context first."
            )
        self.context = self.context_manager.get_current_context()

        # Prepare the LLM
        self.model_n_ctx = 1000
        self.llm = LLMFactory.create_llm(
            model_type=self.model_type,
            model_path=self.model_path,
            model_n_ctx=self.model_n_ctx,
            streaming=False,
            verbose=False,
        )
        self.chatbot_instance = ChatbotFactory.create_chatbot(self.llm)

        # Prepare the retriever
        self.qa_instance = None
        self.qa_instance_error = None
        if mode == BotMode.CHAT.value:
            return
        try:
            self.ingest_documents()
        except Exception as e:
            logging.info(f"Error while initializing retriever: {e}")
            logging.info("Switching to chat mode...")
            self.qa_instance_error = "Error while initializing retriever!"

    def ingest_documents(self, context_id=None) -> None:
        """Ingest the bot's documents."""
        if context_id is not None:
            self.switch_context(context_id)
        ingest_documents(
            self.context.documents_directory,
            self.context.search_db_directory,
            self.context.embeddings_model_name,
        )
        # Reload QA
        self.qa_instance = QAFactory.create_qa(
            context=self.context,
            llm=self.llm,
        )

    def switch_context(self, context_id: int) -> None:
        """Switch the bot context if needed."""
        if self.context.id != context_id:
            self.context = self.context_manager.get_context(context_id)
            self.qa_instance = QAFactory.create_qa(
                context=self.context,
                llm=self.llm,
            )

    def check_query(self, mode, query, context_id=None) -> None:
        """
        Check if the query is valid.
        Raises an exception on invalid query.
        """
        if context_id is not None:
            self.switch_context(context_id)
        if not query:
            raise ValueError("Query cannot be empty!")
        if mode == BotMode.QA.value and self.mode == BotMode.CHAT.value:
            raise ValueError(
                "PautobotEngine was initialized in chat mode! "
                "Please restart in QA mode."
            )
        elif mode == BotMode.QA.value and self.qa_instance is None:
            raise ValueError(self.qa_instance_error)

    def query(self, mode, query, context_id=None) -> None:
        """Query the bot."""
        if context_id is not None:
            self.switch_context(context_id)
        self.check_query(mode, query)
        if mode is None:
            mode = self.mode
        if mode == BotMode.QA.value and self.qa_instance is None:
            logging.info(self.qa_instance_error)
            mode = BotMode.CHAT
        self.context.current_answer = {
            "status": BotStatus.THINKING,
            "answer": "",
            "docs": [],
        }
        self.context.write_chat_history(
            {
                "query": query,
                "mode": mode,
            }
        )
        if mode == BotMode.QA.value:
            try:
                logging.info("Received query: ", query)
                logging.info("Searching...")
                res = self.qa_instance(query)
                answer, docs = (
                    res["result"],
                    res["source_documents"],
                )
                doc_json = []
                for document in docs:
                    document_file = document.metadata["source"]
                    document_id = os.path.basename(document_file).split(".")[0]
                    document_id = int(document_id)
                    db_document = (
                        session.query(db_models.Document)
                        .filter(db_models.Document.id == document_id)
                        .first()
                    )
                    doc_json.append(
                        {
                            "source": db_document.name,
                            "content": document.page_content,
                        }
                    )
                self.context.current_answer = {
                    "status": BotStatus.READY,
                    "answer": answer,
                    "docs": doc_json,
                }
                self.context.write_chat_history(self.context.current_answer)
            except Exception as e:
                logging.error("Error during thinking: ", e)
                traceback.print_exc()
                answer = "Error during thinking! Please try again."
                if "Index not found" in str(e):
                    answer = "Index not found! Please ingest documents first."
                self.context.current_answer = {
                    "status": BotStatus.READY,
                    "answer": answer,
                    "docs": None,
                }
                self.context.write_chat_history(self.context.current_answer)
        else:
            try:
                logging.info("Received query: ", query)
                logging.info("Thinking...")
                answer = self.chatbot_instance.predict(human_input=query)
                logging.info("Answer: ", answer)
                self.context.current_answer = {
                    "status": BotStatus.READY,
                    "answer": answer,
                    "docs": None,
                }
                self.context.write_chat_history(self.context.current_answer)
            except Exception as e:
                logging.error("Error during thinking: ", e)
                traceback.print_exc()
                self.context.current_answer = {
                    "status": BotStatus.READY,
                    "answer": "Error during thinking! Please try again.",
                    "docs": None,
                }
                self.context.write_chat_history(self.context.current_answer)

    def get_answer(self, context_id=None) -> dict:
        """Get the bot's answer."""
        if context_id is not None:
            self.switch_context(context_id)
        return self.context.current_answer

import os

from pautobot.bot_enums import BotMode, BotStatus
from pautobot.llm_factory import LLMFactory, ChatbotFactory, QAFactory
from pautobot.ingest import ingest_documents
from pautobot.utils import open_file
from pautobot.bot_context import BotContext
from pautobot.app_info import DATA_ROOT


class PautoBotEngine:
    """PautoBot engine for answering questions."""

    def __init__(self, mode, model_type="GPT4All") -> None:
        self.mode = mode
        self.model_type = model_type
        self.model_path = os.path.join(
            DATA_ROOT,
            "models",
            "ggml-gpt4all-j-v1.3-groovy.bin",
        )

        # Prepare the bot context
        self.context = BotContext.get_default_bot_context()

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
            self.qa_instance = QAFactory.create_qa(
                context=self.context,
                llm=self.llm,
            )
        except Exception as e:
            print(f"Error while initializing retriever: {e}")
            print("Switching to chat mode...")
            self.qa_instance_error = "Error while initializing retriever!"

    def add_document(self, file: bytes):
        """Add a document to the bot's knowledge base."""
        self.context.add_document(file)

    def get_documents(self):
        """Get the bot's documents."""
        return self.context.get_documents()

    def get_chat_history(self):
        """Get the bot's chat history."""
        return self.context.get_chat_history()

    def clear_chat_history(self):
        """Clear the bot's chat history."""
        self.context.clear_chat_history()

    def ingest_documents(self):
        """Ingest the bot's documents."""
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

    def open_in_file_explorer(self):
        """Open the bot's documents directory in the file explorer."""
        open_file(self.context.documents_directory)

    def check_query(self, mode, query):
        """Check if the query is valid.
        Raises an exception on invalid query.
        """
        if not query:
            raise ValueError("Query cannot be empty!")
        if mode == BotMode.QA.value and self.mode == BotMode.CHAT.value:
            raise ValueError(
                "PautobotEngine was initialized in chat mode! "
                "Please restart in QA mode."
            )
        elif mode == BotMode.QA.value and self.qa_instance is None:
            raise ValueError(self.qa_instance_error)

    def query(self, mode, query):
        """Query the bot."""
        self.check_query(mode, query)
        if mode is None:
            mode = self.mode
        if mode == BotMode.QA.value and self.qa_instance is None:
            print(self.qa_instance_error)
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
                print("Received query: ", query)
                print("Searching...")
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
                self.context.current_answer = {
                    "status": BotStatus.READY,
                    "answer": answer,
                    "docs": doc_json,
                }
                self.context.write_chat_history(self.context.current_answer)
            except Exception as e:
                print("Error during thinking: ", e)
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
                print("Received query: ", query)
                print("Thinking...")
                answer = self.chatbot_instance.predict(human_input=query)
                print("Answer: ", answer)
                self.context.current_answer = {
                    "status": BotStatus.READY,
                    "answer": answer,
                    "docs": None,
                }
                self.context.write_chat_history(self.context.current_answer)
            except Exception as e:
                print("Error during thinking: ", e)
                self.context.current_answer = {
                    "status": BotStatus.READY,
                    "answer": "Error during thinking! Please try again.",
                    "docs": None,
                }
                self.context.write_chat_history(self.context.current_answer)

    def get_answer(self):
        return self.context.current_answer

import os
import queue
from enum import Enum

from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All, LlamaCpp
from pautobot.constants import CHROMA_SETTINGS


class BotStatus(str, Enum):
    """Bot status."""

    READY = "READY"
    THINKING = "THINKING"
    ERROR = "ERROR"


class BotMode(str, Enum):
    """Bot mode."""

    QA = "QA"
    CHAT = "CHAT"


class PautoBotEngine:
    """PautoBot engine for answering questions."""

    def __init__(
        self, mode=BotMode.QA, model_type=os.environ.get("MODEL_TYPE")
    ) -> None:
        self.mode = mode
        self.model_type = model_type
        self.hide_source = False
        self.mute_stream = False
        self.is_thinking = False
        self.current_answer = {
            "status": BotStatus.READY,
            "answer": "",
            "docs": [],
        }
        self.answer_q = queue.Queue()

        embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")
        persist_directory = os.environ.get("PERSIST_DIRECTORY")
        model_path = os.environ.get("MODEL_PATH")
        model_n_ctx = os.environ.get("MODEL_N_CTX")
        target_source_chunks = int(os.environ.get("TARGET_SOURCE_CHUNKS", 4))

        # Prepare the LLM
        if self.model_type == "LlamaCpp":
            self.llm = LlamaCpp(
                model_path=model_path,
                n_ctx=model_n_ctx,
                streaming=False,
                verbose=False,
            )
        elif self.model_type == "GPT4All":
            self.llm = GPT4All(
                model=model_path,
                n_ctx=model_n_ctx,
                backend="gptj",
                streaming=False,
                verbose=False,
            )
        else:
            print(f"Model {model_type} not supported!")
            exit(1)

        # Prepare the retriever
        self.qa_instance = None
        if mode == BotMode.CHAT:
            return
        try:
            embeddings = HuggingFaceEmbeddings(
                model_name=embeddings_model_name
            )
            db = Chroma(
                persist_directory=persist_directory,
                embedding_function=embeddings,
                client_settings=CHROMA_SETTINGS,
            )
            retriever = db.as_retriever(
                search_kwargs={"k": target_source_chunks}
            )
            self.qa_instance = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True,
            )
            self.mode = BotMode.QA
        except Exception as e:
            print(f"Error while initializing retriever: {e}")
            print("Switching to chat mode...")
            self.mode = BotMode.CHAT

    def query(self, query):
        self.current_answer = {
            "status": BotStatus.THINKING,
            "answer": "",
            "docs": [],
        }
        if self.mode == BotMode.QA:
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
                self.current_answer = {
                    "status": BotStatus.READY,
                    "answer": "Error during thinking! Please try again.",
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
        if self.current_answer["status"] == BotStatus.THINKING:
            # Stream from the queue
            while not self.answer_q.empty():
                self.current_answer["answer"] += self.answer_q.get()
        return self.current_answer

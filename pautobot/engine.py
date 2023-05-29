import os
from typing import Any

from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All, LlamaCpp
from pautobot.constants import CHROMA_SETTINGS
from pautobot import global_state

load_dotenv()


embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")
persist_directory = os.environ.get("PERSIST_DIRECTORY")
model_type = os.environ.get("MODEL_TYPE")
model_path = os.environ.get("MODEL_PATH")
model_n_ctx = os.environ.get("MODEL_N_CTX")
target_source_chunks = int(os.environ.get("TARGET_SOURCE_CHUNKS", 4))
hide_source = False
mute_stream = False

embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
db = Chroma(
    persist_directory=persist_directory,
    embedding_function=embeddings,
    client_settings=CHROMA_SETTINGS,
)
retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})


# activate/deactivate the streaming StdOut callback for LLMs
class StreamingHandler(StreamingStdOutCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        if global_state.global_answer["answer"] is None:
            global_state.global_answer["answer"] = token
        else:
            global_state.global_answer["answer"] += token


callbacks = [] if mute_stream else [StreamingHandler()]

# Prepare the LLM
match model_type:
    case "LlamaCpp":
        llm = LlamaCpp(
            model_path=model_path,
            n_ctx=model_n_ctx,
            callbacks=callbacks,
            verbose=False,
        )
    case "GPT4All":
        llm = GPT4All(
            model=model_path,
            n_ctx=model_n_ctx,
            backend="gptj",
            callbacks=callbacks,
            verbose=False,
        )
    case _:
        print(f"Model {model_type} not supported!")
        exit(1)

qa_instance = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
)

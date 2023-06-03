from langchain.llms import GPT4All, LlamaCpp
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from chromadb.config import Settings
from langchain import LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

from pautobot.utils import download_model
from pautobot.bot_context import BotContext


class LLMFactory:
    """Factory for instantiating LLMs."""

    @staticmethod
    def create_llm(
        model_type, model_path, model_n_ctx, streaming=False, verbose=False
    ):
        # Download the model
        download_model(model_type, model_path)

        # Prepare the LLM
        if model_type == "LlamaCpp":
            return LlamaCpp(
                model_path=model_path,
                n_ctx=model_n_ctx,
                streaming=streaming,
                verbose=verbose,
            )
        elif model_type == "GPT4All":
            return GPT4All(
                model=model_path,
                n_ctx=model_n_ctx,
                backend="gptj",
                streaming=streaming,
                verbose=verbose,
            )


class ChatbotFactory:
    """Factory for instantiating chatbots."""

    @staticmethod
    def create_chatbot(
        llm,
    ):
        template = """Assistant is a large language model train by human.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

{history}
Human: {human_input}
Assistant:"""

        prompt = PromptTemplate(
            input_variables=["history", "human_input"], template=template
        )
        chatbot_instance = LLMChain(
            llm=llm,
            prompt=prompt,
            verbose=True,
            memory=ConversationBufferWindowMemory(k=2),
        )
        return chatbot_instance


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

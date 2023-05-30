from langchain.llms import GPT4All, LlamaCpp
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma


class LLMFactory:
    """Factory for instantiating LLMs."""

    @staticmethod
    def create_llm(
        model_type, model_path, model_n_ctx, streaming=False, verbose=False
    ):
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


class QAFactory:
    """Factory for instantiating QAs."""

    @staticmethod
    def create_qa(
        chroma_settings,
        persist_directory,
        llm,
        embeddings_model_name,
    ):
        embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
        database = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings,
            client_settings=chroma_settings,
        )
        retriever = database.as_retriever(
            search_kwargs={"k": 4}
        )
        qa_instance = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
        )
        return qa_instance

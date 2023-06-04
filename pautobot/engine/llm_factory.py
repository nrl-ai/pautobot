from langchain.llms import GPT4All, LlamaCpp

from pautobot.utils import download_model


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

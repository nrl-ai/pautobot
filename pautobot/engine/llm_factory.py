from langchain.llms import GPT4All

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
        if model_type == "GPT4All":
            return GPT4All(
                model=model_path,
                n_ctx=model_n_ctx,
                backend="gptj",
                streaming=streaming,
                verbose=verbose,
            )
        else:
            raise ValueError(f"Invalid model type: {model_type}")

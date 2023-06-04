import os
import shutil

from pautobot.app_info import DATA_ROOT
from pautobot.engine.bot_context import BotContext


class ContextManager:
    """
    Context manager. Handle logics related to PautoBot contexts.
    """

    def __init__(self):
        self._contexts = {}
        self._current_context = None

    def load_from_disk(self) -> None:
        """
        Load all contexts from disk.
        """
        for context_id in os.listdir(os.path.join(DATA_ROOT, "contexts")):
            path = os.path.join(DATA_ROOT, "contexts", context_id)
            if os.path.isdir(path):
                context = BotContext.load_from_folder(path)
                self._contexts[context.id] = context
        if self._contexts:
            self._current_context = list(self._contexts.values())[0]

    def register(self, context: BotContext) -> None:
        """
        Register a new context.
        """
        if context.id in self._contexts:
            raise ValueError(f"Context {context.id} already exists!")
        self._contexts[context.id] = context
        if self._current_context is None:
            self._current_context = context

    def rename_context(self, context_id: str, new_name: str) -> None:
        """
        Rename a context.
        """
        if context_id not in self._contexts:
            raise ValueError(f"Context {context_id} not found!")
        self._contexts[context_id].rename(new_name)

    def delete_context(self, context_id: str) -> None:
        """
        Completely delete a context.
        """
        if context_id not in self._contexts:
            raise ValueError(f"Context {context_id} not found!")

        # Delete the context
        to_be_deleted = self._contexts[context_id]
        del self._contexts[context_id]
        shutil.rmtree(to_be_deleted.storage_path)

        if not self._contexts:
            self._current_context = None
        else:
            self._current_context = list(self._contexts.values())[0]

    def get_context(self, context_id: str) -> BotContext:
        """
        Get a context by its ID.
        """
        if context_id not in self._contexts:
            raise ValueError(f"Context {context_id} not found!")
        return self._contexts[context_id]

    def get_contexts(self) -> dict:
        """
        Get all contexts.
        """
        return self._contexts

    def set_current_context(self, context_id: str) -> None:
        """
        Set the current context.
        """
        if context_id not in self._contexts:
            raise ValueError(f"Context {context_id} not found!")
        self._current_context = self._contexts[context_id]

    def get_current_context(self) -> BotContext:
        """
        Get the current context.
        """
        return self._current_context

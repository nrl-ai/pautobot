import logging
import os
import shutil

from pautobot import db_models
from pautobot.config import DATA_ROOT
from pautobot.database import session
from pautobot.engine.bot_context import BotContext


class ContextManager:
    """
    Context manager. Handle logics related to PautoBot contexts.
    """

    def __init__(self):
        self._current_context = None
        self._contexts = {}

    def load_contexts(self) -> None:
        """
        Load all contexts from the database.
        """
        self._contexts = {0: BotContext(id=0, name="Default")}
        self._current_context = self._contexts[0]
        for context in session.query(db_models.BotContext).all():
            self._contexts[context.id] = BotContext(id=context.id)

    def rename_context(self, context_id: int, new_name: str) -> None:
        """
        Rename a context.
        """
        if context_id not in self._contexts:
            raise ValueError(f"Context {context_id} not found!")
        session.query(db_models.BotContext).filter_by(id=context_id).update(
            {"name": new_name}
        )
        session.commit()

    def delete_context(self, context_id: int) -> None:
        """
        Completely delete a context.
        """
        if context_id not in self._contexts:
            raise ValueError(f"Context {context_id} not found!")
        if context_id in self._contexts:
            del self._contexts[context_id]
        try:
            session.query(db_models.BotContext).filter_by(
                id=context_id
            ).delete()
            session.commit()
            shutil.rmtree(os.path.join(DATA_ROOT, "contexts", str(context_id)))
        except Exception as e:
            logging.error(f"Error while deleting context {context_id}: {e}")

    def get_context(self, context_id: int) -> BotContext:
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

    def set_current_context(self, context_id: int) -> None:
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

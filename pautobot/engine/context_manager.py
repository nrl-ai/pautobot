from .bot_context import BotContext


class ContextManager:
    def __init__(self):
        self._contexts = {}
        self._current_context = None

    def register(self, context: BotContext) -> None:
        self._contexts[context.id] = context
        if self._current_context is None:
            self._current_context = context

    def get_context(self, context_id: str) -> BotContext:
        if context_id not in self._contexts:
            raise ValueError(f"Context {context_id} not found!")
        return self._contexts[context_id]

    def get_contexts(self) -> dict:
        return self._contexts

    def set_current_context(self, context_id: str) -> None:
        if context_id not in self._contexts:
            raise ValueError(f"Context {context_id} not found!")
        self._current_context = self._contexts[context_id]

    def get_current_context(self) -> BotContext:
        return self._current_context

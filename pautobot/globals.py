from pautobot.engine import PautoBotEngine
from pautobot.engine.bot_enums import BotMode
from pautobot.engine.context_manager import ContextManager

engine = None
context_manager = None


def init():
    """Initialize the global engine."""
    global context_manager
    global engine

    context_manager = ContextManager()
    context_manager.load_contexts()

    engine = PautoBotEngine(mode=BotMode.QA, context_manager=context_manager)

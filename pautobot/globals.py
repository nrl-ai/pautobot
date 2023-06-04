from pautobot.engine import PautoBotEngine
from pautobot.engine.bot_context import BotContext
from pautobot.engine.bot_enums import BotMode
from pautobot.engine.context_manager import ContextManager

engine = None
context_manager = None


def init():
    """Initialize the global engine."""
    global context_manager
    global engine

    context_manager = ContextManager()
    context_manager.register(BotContext.get_default_bot_context())
    context_manager.load_from_disk()

    engine = PautoBotEngine(mode=BotMode.QA, context_manager=context_manager)

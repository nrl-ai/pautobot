from fastapi import APIRouter

from pautobot import globals
from pautobot.engine.bot_context import BotContext

router = APIRouter(
    prefix="/api",
    tags=["Bot Context"],
)


@router.get("/contexts")
async def get_contexts():
    """
    Get all chat contexts
    Each context is a separate chat session
    """
    contexts = globals.context_manager.get_contexts()
    context_list = []
    for context in contexts:
        context_list.append(contexts[context].dict())
    return context_list


@router.get("/current_context")
async def get_current_context():
    """
    Get the current chat context
    """
    return globals.context_manager.get_current_context().dict()


@router.post("/contexts")
async def create_context():
    """
    Create a new chat context
    """
    context = BotContext()
    globals.context_manager.register(context)
    return {
        "message": "Context created",
        "data": context.dict(),
    }


@router.delete("/contexts/{context_id}")
async def delete_context(context_id: int):
    """
    Delete a chat context
    """
    globals.context_manager.delete_context(context_id)
    return {"message": "Context deleted"}


@router.put("/contexts/{context_id}")
async def rename_context(context_id: int, new_name: str):
    """
    Rename a chat context
    """
    globals.context_manager.rename_context(context_id, new_name)
    return {"message": "Context renamed"}


@router.post("/set_context")
async def set_context(context_id: int):
    """
    Set the current context
    """
    globals.context_manager.set_current_context(context_id)
    globals.engine.set_context(globals.context_manager.get_current_context())
    return {"message": "Context set"}


@router.get("/{context_id}/chat_history")
async def get_chat_history(context_id: int):
    """
    Get the bot's chat history
    """
    return globals.context_manager.get_context(context_id).get_chat_history()


@router.delete("/{context_id}/chat_history")
async def clear_chat_history(context_id: int):
    """
    Clear the bot's chat history
    """
    globals.context_manager.get_context(context_id).clear_chat_history()
    return {"message": "Chat history cleared"}

from fastapi import APIRouter

from pautobot import globals

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


@router.post("/set_context")
async def set_context(context_id: str):
    """
    Set the current context
    """
    globals.context_manager.set_current_context(context_id)
    globals.engine.set_context(globals.context_manager.get_current_context())
    return {"message": "Context set"}


@router.get("/{context_id}/chat_history")
async def get_chat_history(context_id: str):
    """
    Get the bot's chat history
    """
    return globals.context_manager.get_context(context_id).get_chat_history()


@router.delete("/{context_id}/chat_history")
async def clear_chat_history(context_id: str):
    """
    Clear the bot's chat history
    """
    globals.context_manager.get_context(context_id).clear_chat_history()
    return {"message": "Chat history cleared"}

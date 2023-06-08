from fastapi import APIRouter, BackgroundTasks

from pautobot import globals
from pautobot.engine.bot_enums import BotStatus
from pautobot.models import Query

router = APIRouter(
    prefix="/api",
    tags=["Ask Bot"],
)


@router.post("/{context_id}/ask")
async def ask(
    context_id: int, query: Query, background_tasks: BackgroundTasks
):
    globals.engine.check_query(query.mode, query.query, context_id=context_id)
    if globals.engine.context.current_answer["status"] == BotStatus.THINKING:
        raise SystemError("I am still thinking! Please wait.")
    globals.engine.context.current_answer = {
        "status": BotStatus.THINKING,
        "answer": "",
        "docs": [],
    }
    background_tasks.add_task(globals.engine.query, query.mode, query.query)
    return {"message": "Query received"}


@router.get("/{context_id}/get_answer")
async def get_answer(context_id: int):
    return globals.engine.get_answer(context_id=context_id)

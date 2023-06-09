import logging
import traceback

from fastapi import APIRouter, BackgroundTasks, status
from fastapi.responses import JSONResponse

from pautobot import globals
from pautobot.engine.bot_enums import BotStatus
from pautobot.models import Query

router = APIRouter(
    prefix="/api",
    tags=["Ask Bot"],
)


@router.get("/bot_info")
async def get_bot_info():
    return globals.engine.get_bot_info()


@router.post("/{context_id}/ask")
async def ask(
    context_id: int, query: Query, background_tasks: BackgroundTasks
):
    try:
        globals.engine.check_query(
            query.mode, query.query, context_id=context_id
        )
    except ValueError as e:
        logging.error(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(e)},
        )
    if globals.engine.context.current_answer["status"] == BotStatus.THINKING:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Bot is already thinking"},
        )
    globals.engine.context.current_answer = {
        "answer": "",
        "docs": [],
    }
    background_tasks.add_task(globals.engine.query, query.mode, query.query)
    return {"message": "Query received"}


@router.get("/{context_id}/get_answer")
async def get_answer(context_id: int):
    return globals.engine.get_answer(context_id=context_id)

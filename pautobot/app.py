import os

import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from pautobot.models import Query
from pautobot.utils import extract_frontend_dist
from pautobot.bot_enums import BotMode, BotStatus
from pautobot.engine import PautoBotEngine


def main():
    static_folder = os.path.abspath(
        os.path.join(os.path.expanduser("~"), "pautobot-data", "frontend-dist")
    )
    print(static_folder)
    extract_frontend_dist(static_folder)

    # PautoBot engine
    engine = PautoBotEngine(mode=BotMode.QA)

    # Backend app
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.post("/api/ask")
    async def ask(query: Query, background_tasks: BackgroundTasks):
        engine.check_query(query.mode, query.query)
        if engine.current_answer["status"] == BotStatus.THINKING:
            raise Exception("I am still thinking! Please wait.")
        engine.current_answer = {
            "status": BotStatus.THINKING,
            "answer": "",
            "docs": [],
        }
        background_tasks.add_task(engine.query, query.mode, query.query)
        return {"message": "Query received"}

    @app.get("/api/get_answer")
    async def get_answer():
        return engine.get_answer()

    app.mount(
        "/", StaticFiles(directory=static_folder, html=True), name="static"
    )

    uvicorn.run(app, host="0.0.0.0", port=5678)


if __name__ == "__main__":
    main()

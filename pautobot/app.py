import os

import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, BackgroundTasks, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from pautobot.models import Query
from pautobot.utils import extract_frontend_dist
from pautobot.bot_enums import BotMode, BotStatus
from pautobot.engine import PautoBotEngine
from pautobot.app_info import __appname__, __version__, DATA_ROOT


def main():
    print(f"Starting {__appname__}...")
    print(f"Version: {__version__}")
    static_folder = os.path.abspath(os.path.join(DATA_ROOT, "frontend-dist"))
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

    @app.post("/api/upload")
    async def upload(file: UploadFile = File(...)):
        if not file:
            return {"message": "No file sent"}
        else:
            engine.add_document(file)
            return {"message": "File uploaded"}

    @app.post("/api/ingest")
    async def ingest():
        engine.ingest_documents()
        return {"message": "Ingestion finished!"}

    @app.get("/api/get_documents")
    async def get_documents():
        return engine.get_documents()

    @app.post("/api/open_in_file_explorer")
    async def open_in_file_explorer():
        engine.open_in_file_explorer()

    @app.post("/api/ask")
    async def ask(query: Query, background_tasks: BackgroundTasks):
        engine.check_query(query.mode, query.query)
        if engine.context.current_answer["status"] == BotStatus.THINKING:
            raise SystemError("I am still thinking! Please wait.")
        engine.context.current_answer = {
            "status": BotStatus.THINKING,
            "answer": "",
            "docs": [],
        }
        background_tasks.add_task(engine.query, query.mode, query.query)
        return {"message": "Query received"}

    @app.get("/api/get_answer")
    async def get_answer():
        return engine.get_answer()

    @app.get("/api/chat_history")
    async def get_chat_history():
        return engine.get_chat_history()

    @app.delete("/api/chat_history")
    async def clear_chat_history():
        engine.clear_chat_history()
        return {"message": "Chat history cleared"}

    app.mount(
        "/", StaticFiles(directory=static_folder, html=True), name="static"
    )

    uvicorn.run(app, host="0.0.0.0", port=5678)


if __name__ == "__main__":
    main()

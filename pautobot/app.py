import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from pautobot.engine import PautoBotEngine, BotStatus, BotMode
from pautobot.models import Query
from pautobot.utils import extract_frontend_dist

static_folder = "pautobot-data/frontend-dist"

engine = PautoBotEngine(mode=BotMode.CHAT)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/ask")
async def ask(query: Query, background_tasks: BackgroundTasks):
    global engine
    if engine.current_answer["status"] == BotStatus.THINKING:
        raise Exception("I am still thinking! Please wait.")
    engine.current_answer = {
        "status": BotStatus.THINKING,
        "answer": "",
        "docs": [],
    }
    background_tasks.add_task(engine.query, query.query)
    return {"message": "Query received"}


@app.get("/api/get_answer")
async def get_answer():
    global engine
    return engine.get_answer()


app.mount("/", StaticFiles(directory=static_folder, html=True), name="static")


def main():
    extract_frontend_dist(static_folder)
    uvicorn.run(app, host="0.0.0.0", port=5678)


if __name__ == "__main__":
    main()

import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pautobot import globals
from pautobot.app_info import DATA_ROOT, __appname__, __description__, __version__
from pautobot.routers import bot, contexts, documents
from pautobot.utils import extract_frontend_dist

print(f"Starting {__appname__}...")
print(f"Version: {__version__}")
static_folder = os.path.abspath(os.path.join(DATA_ROOT, "frontend-dist"))
extract_frontend_dist(static_folder)

# Backend app
app = FastAPI(
    title=__appname__,
    description=__description__,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bot.router)
app.include_router(contexts.router)
app.include_router(documents.router)
app.mount("/", StaticFiles(directory=static_folder, html=True), name="static")


if __name__ == "__main__":
    globals.init()
    uvicorn.run(app, host="0.0.0.0", port=5678, reload=False, workers=1)

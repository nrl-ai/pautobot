import logging
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pautobot import db_models as models
from pautobot import globals
from pautobot.app_info import __appname__, __description__, __version__
from pautobot.config import DATA_ROOT
from pautobot.database import engine
from pautobot.routers import bot, contexts, documents
from pautobot.utils import extract_frontend_dist


def main():
    logging.info(f"Starting {__appname__}...")
    logging.info(f"Version: {__version__}")

    logging.info("Extracting frontend distribution...")
    static_folder = os.path.abspath(os.path.join(DATA_ROOT, "frontend-dist"))
    extract_frontend_dist(static_folder)

    logging.info("Creating database tables...")
    models.Base.metadata.create_all(bind=engine)

    logging.info("Starting FastAPI server...")
    globals.init()

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
    app.mount(
        "/", StaticFiles(directory=static_folder, html=True), name="static"
    )

    uvicorn.run(app, host="0.0.0.0", port=5678, reload=False, workers=1)


if __name__ == "__main__":
    main()

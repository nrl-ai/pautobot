import os
import pathlib
from dotenv import load_dotenv
from chromadb.config import Settings
from pautobot.utils import init_env_file

init_env_file()
load_dotenv()

# Define the folder for storing database
PERSIST_DIRECTORY = os.environ.get("PERSIST_DIRECTORY")
pathlib.Path(PERSIST_DIRECTORY).mkdir(parents=True, exist_ok=True)

# Define the Chroma settings
CHROMA_SETTINGS = Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=PERSIST_DIRECTORY,
    anonymized_telemetry=False,
)

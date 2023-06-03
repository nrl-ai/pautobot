import os
import pathlib
import json
import copy
import uuid
import shutil

import datetime

from pautobot.bot_enums import BotMode, BotStatus
from pautobot.app_info import DATA_ROOT

DEFAULT_ANSWER = {
    "status": BotStatus.READY,
    "answer": "",
    "docs": [],
}


class BotContext:
    def __init__(self, storage_path) -> None:
        pathlib.Path(storage_path).mkdir(parents=True, exist_ok=True)
        self.storage_path = storage_path
        self.embeddings_model_name = "all-MiniLM-L6-v2"
        self.documents_directory = os.path.join(storage_path, "documents")
        self.search_db_directory = os.path.join(storage_path, "search_db")
        self.chat_history_file = os.path.join(
            storage_path, "chat_history.json"
        )
        self.chat_files_directory = os.path.join(storage_path, "chat_files")
        self.info_file = os.path.join(storage_path, "info.json")
        if not os.path.exists(self.info_file):
            self.initialize_bot_context()
        self.current_answer = copy.deepcopy(DEFAULT_ANSWER)

    @staticmethod
    def get_default_bot_context():
        """Get the default bot context."""
        return BotContext(os.path.join(DATA_ROOT, "contexts", "default"))

    def get_info(self):
        """Get the bot info."""
        with open(self.info_file, "r") as info_file:
            return json.load(info_file)

    def initialize_bot_context(self):
        """Initialize the bot context."""
        for directory in [
            self.documents_directory,
            self.search_db_directory,
            self.chat_files_directory,
        ]:
            pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        with open(self.chat_history_file, "w") as chat_history_file:
            json.dump([], chat_history_file)
        with open(self.info_file, "w") as info_file:
            json.dump(
                {
                    "title": "Untitled",
                    "created_date": datetime.datetime.now().isoformat(),
                    "current_mode": BotMode.CHAT.value,
                },
                info_file,
            )

    def add_document(self, file: bytes):
        """Add a document to the bot's knowledge base."""
        pathlib.Path(self.documents_directory).mkdir(
            parents=True, exist_ok=True
        )
        file_extension = os.path.splitext(file.filename)[1]
        unique_file_id = uuid.uuid4()
        new_filename = f"{unique_file_id}.{file_extension}"
        with open(
            os.path.join(self.documents_directory, new_filename), "wb+"
        ) as destination:
            shutil.copyfileobj(file.file, destination)
        metadata_filename = f"{unique_file_id}.json"
        with open(
            os.path.join(self.documents_directory, metadata_filename), "w"
        ) as metadata_file:
            metadata_file.write(
                f'{{"source": "{file.filename}", "id": "{unique_file_id}"}}'
            )

    def get_documents(self):
        """List all documents."""
        documents = []
        for filename in os.listdir(self.documents_directory):
            if filename.endswith(".json"):
                with open(
                    os.path.join(self.documents_directory, filename), "r"
                ) as metadata_file:
                    metadata = json.load(metadata_file)
                    documents.append(metadata)
        return documents

    def write_chat_history(self, chat_history: dict):
        """Write a message to the bot's chat history."""
        with open(self.chat_history_file, "r") as chat_history_file:
            chat_history_list = json.load(chat_history_file)
        chat_history_list.append(chat_history)
        with open(self.chat_history_file, "w") as chat_history_file:
            json.dump(chat_history_list, chat_history_file)

    def get_chat_history(self):
        """Get the bot's chat history."""
        with open(self.chat_history_file, "r") as chat_history_file:
            return json.load(chat_history_file)

    def clear_chat_history(self):
        """Clear the bot's chat history."""
        with open(self.chat_history_file, "w") as chat_history_file:
            json.dump([], chat_history_file)

    def __str__(self) -> str:
        return f"ChatContext(storage_path={self.storage_path})"

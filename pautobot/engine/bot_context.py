import copy
import json
import os
import pathlib
import shutil
import uuid

from pautobot.app_info import DATA_ROOT
from pautobot.engine.bot_enums import BotStatus
from pautobot.utils import open_file

DEFAULT_ANSWER = {
    "status": BotStatus.READY,
    "answer": "",
    "docs": [],
}


class BotContext:
    def __init__(
        self, id=None, name=None, storage_path=None, *args, **kwargs
    ) -> None:
        if id is None:
            id = str(uuid.uuid4())
        if name is None:
            name = id
        if storage_path is None:
            storage_path = os.path.join(DATA_ROOT, "contexts", id)
        pathlib.Path(storage_path).mkdir(parents=True, exist_ok=True)
        self.id = id
        self.name = name
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

    def save(self) -> None:
        """Save the bot context."""
        with open(self.info_file, "w") as info_file:
            json.dump(
                self.dict(),
                info_file,
            )

    @staticmethod
    def load_from_file(info_file: str) -> "BotContext":
        """Load a bot context from a file."""
        with open(info_file, "r") as info_file:
            info = json.load(info_file)
        return BotContext(**info)

    @staticmethod
    def load_from_folder(context_folder: str) -> "BotContext":
        """Load a bot context from a folder."""
        return BotContext.load_from_file(
            os.path.join(context_folder, "info.json")
        )

    @staticmethod
    def get_default_bot_context():
        """Get the default bot context."""
        return BotContext(id="default", name="Default")

    def get_info(self) -> dict:
        """Get the bot info."""
        with open(self.info_file, "r") as info_file:
            return json.load(info_file)

    def initialize_bot_context(self) -> None:
        """Initialize the bot context."""
        for directory in [
            self.documents_directory,
            self.search_db_directory,
            self.chat_files_directory,
        ]:
            pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        with open(self.chat_history_file, "w") as chat_history_file:
            json.dump([], chat_history_file)
        self.save()

    def rename(self, new_name: str) -> None:
        """Rename the bot context."""
        self.name = new_name
        self.save()

    def add_document(self, file: bytes) -> None:
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

    def delete_document(self, document_id: str) -> None:
        """Delete a document from the bot's knowledge base."""
        for filename in os.listdir(self.documents_directory):
            if filename.startswith(document_id):
                os.remove(os.path.join(self.documents_directory, filename))

    def get_documents(self) -> list:
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

    def open_documents_folder(self) -> None:
        """Open the documents folder."""
        open_file(self.documents_directory)

    def write_chat_history(self, chat_history: dict) -> None:
        """Write a message to the bot's chat history."""
        with open(self.chat_history_file, "r") as chat_history_file:
            chat_history_list = json.load(chat_history_file)
        chat_history_list.append(chat_history)
        with open(self.chat_history_file, "w") as chat_history_file:
            json.dump(chat_history_list, chat_history_file)

    def get_chat_history(self) -> list:
        """Get the bot's chat history."""
        with open(self.chat_history_file, "r") as chat_history_file:
            return json.load(chat_history_file)

    def clear_chat_history(self) -> None:
        """Clear the bot's chat history."""
        with open(self.chat_history_file, "w") as chat_history_file:
            json.dump([], chat_history_file)

    def __str__(self) -> str:
        return f"ChatContext(storage_path={self.storage_path})"

    def dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "storage_path": self.storage_path,
            "embeddings_model_name": self.embeddings_model_name,
            "documents_directory": self.documents_directory,
            "search_db_directory": self.search_db_directory,
            "chat_history_file": self.chat_history_file,
            "chat_files_directory": self.chat_files_directory,
            "info_file": self.info_file,
        }

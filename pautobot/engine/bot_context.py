import copy
import json
import os
import pathlib
import shutil
import uuid

from pautobot import db_models
from pautobot.config import DATA_ROOT
from pautobot.database import session
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
            id = 0
        db_bot_context = (
            session.query(db_models.BotContext).filter_by(id=id).first()
        )
        if db_bot_context is None:
            if name is None:
                name = str(uuid.uuid4())
            db_bot_context = db_models.BotContext(id=id, name=name)
            session.add(db_bot_context)
            session.commit()
        name = db_bot_context.name
        if storage_path is None:
            storage_path = os.path.join(DATA_ROOT, "contexts", str(id))
        pathlib.Path(storage_path).mkdir(parents=True, exist_ok=True)
        self.id = id
        self.name = name
        self.storage_path = storage_path
        self.embeddings_model_name = "all-MiniLM-L6-v2"
        self.documents_directory = os.path.join(storage_path, "documents")
        self.search_db_directory = os.path.join(storage_path, "search_db")
        self.chat_files_directory = os.path.join(storage_path, "chat_files")
        self.info_file = os.path.join(storage_path, "info.json")
        if not os.path.exists(self.info_file):
            self.initialize_bot_context()
        self.current_answer = copy.deepcopy(DEFAULT_ANSWER)

    @staticmethod
    def get_default_bot_context():
        """Get the default bot context."""
        return BotContext(id=0, name="Default")

    def get_info(self) -> dict:
        """Get the bot info."""
        return {
            "id": self.id,
            "name": self.name,
        }

    def initialize_bot_context(self) -> None:
        """Initialize the bot context."""
        for directory in [
            self.documents_directory,
            self.search_db_directory,
            self.chat_files_directory,
        ]:
            pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

    def rename(self, new_name: str) -> None:
        """Rename the bot context."""
        db_bot_context = (
            session.query(db_models.BotContext).filter_by(id=self.id).first()
        )
        db_bot_context.name = new_name
        session.commit()

    def add_document(self, file, filename) -> None:
        """Add a document to the bot's knowledge base."""
        pathlib.Path(self.documents_directory).mkdir(
            parents=True, exist_ok=True
        )
        file_extension = os.path.splitext(filename)[1]

        # Create a new document in the database
        db_document = db_models.Document(bot_context_id=self.id, name=filename)
        session.add(db_document)
        session.commit()
        document_id = db_document.id

        new_filename = f"{document_id}{file_extension}"
        with open(
            os.path.join(self.documents_directory, new_filename), "wb+"
        ) as destination:
            shutil.copyfileobj(file, destination)

        db_document.storage_name = new_filename
        session.commit()

    def delete_document(self, document_id: int) -> None:
        """Delete a document from the bot's knowledge base."""
        db_document = (
            session.query(db_models.Document)
            .filter_by(bot_context_id=self.id, id=document_id)
            .first()
        )
        if db_document is None:
            raise ValueError(f"Document with id {document_id} not found.")
        os.remove(
            os.path.join(self.documents_directory, db_document.storage_name)
        )
        session.delete(db_document)
        session.commit()

    def get_documents(self) -> list:
        """List all documents."""
        documents = []
        for db_document in (
            session.query(db_models.Document)
            .filter_by(bot_context_id=self.id)
            .all()
        ):
            documents.append(
                {
                    "id": db_document.id,
                    "name": db_document.name,
                    "storage_name": db_document.storage_name,
                }
            )
        return documents

    def open_documents_folder(self) -> None:
        """Open the documents folder."""
        open_file(self.documents_directory)

    def open_document(self, document_id: int) -> None:
        """Open a document."""
        db_document = (
            session.query(db_models.Document)
            .filter_by(bot_context_id=self.id, id=document_id)
            .first()
        )
        if db_document is None:
            raise ValueError(f"Document with id {document_id} not found.")
        open_file(
            os.path.join(self.documents_directory, db_document.storage_name)
        )

    def write_chat_history(self, chat_history: dict) -> None:
        """Write a message to the bot's chat history."""
        chat_history_text = json.dumps(chat_history)
        db_chat_chunk = db_models.ChatChunk(
            bot_context_id=self.id, text=chat_history_text
        )
        session.add(db_chat_chunk)
        session.commit()

    def get_chat_history(self) -> list:
        """Get the bot's chat history."""
        chat_history = []
        for db_chat_chunk in (
            session.query(db_models.ChatChunk)
            .filter_by(bot_context_id=self.id)
            .all()
        ):
            chat_history.append(json.loads(db_chat_chunk.text))
        return chat_history

    def clear_chat_history(self) -> None:
        """Clear the bot's chat history."""
        session.query(db_models.ChatChunk).filter_by(
            bot_context_id=self.id
        ).delete()
        session.commit()

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

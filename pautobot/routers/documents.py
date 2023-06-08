import os
import tempfile
import zipfile

from fastapi import APIRouter, File, UploadFile

from pautobot import globals
from pautobot.utils import SUPPORTED_DOCUMENT_TYPES

router = APIRouter(
    prefix="/api",
    tags=["Documents"],
)


@router.get("/{context_id}/documents")
async def get_documents(context_id: int):
    """
    Get all documents in the bot's context
    """
    return globals.context_manager.get_context(context_id).get_documents()


@router.post("/{context_id}/documents")
async def upload_document(context_id: int, file: UploadFile = File(...)):
    """
    Upload a document to the bot's context
    """
    if not file:
        return {"message": "No file sent"}

    file_extension = os.path.splitext(file.filename)[1]
    if file_extension == ".zip":
        tmp_dir = tempfile.mkdtemp()
        tmp_zip_file = os.path.join(tmp_dir, file.filename)
        with open(tmp_zip_file, "wb") as tmp_zip:
            tmp_zip.write(file.file.read())
        with zipfile.ZipFile(tmp_zip_file, "r") as zip_ref:
            zip_ref.extractall(tmp_dir)
        for filename in os.listdir(tmp_dir):
            if os.path.splitext(filename)[1] in SUPPORTED_DOCUMENT_TYPES:
                with open(os.path.join(tmp_dir, filename), "rb") as file:
                    globals.context_manager.get_context(
                        context_id
                    ).add_document(file, filename)
        return {"message": "File uploaded"}
    elif file_extension in SUPPORTED_DOCUMENT_TYPES:
        globals.context_manager.get_context(context_id).add_document(
            file.file, file.filename
        )
        return {"message": "File uploaded"}
    raise Exception("Unsupported file type")


@router.delete("/{context_id}/documents/{document_id}")
async def delete_document(context_id: int, document_id: int):
    """
    Delete a document from the bot's context
    """
    globals.context_manager.get_context(context_id).delete_document(
        document_id
    )
    globals.engine.ingest_documents(context_id=context_id)
    return {"message": "Document deleted"}


@router.post("/{context_id}/documents/ingest")
async def ingest_documents(context_id: int):
    """
    Ingest all documents in the bot's context
    """
    globals.engine.ingest_documents(context_id=context_id)
    return {"message": "Ingestion finished!"}


@router.post("/{context_id}/documents/open_in_file_explorer")
async def open_in_file_explorer(context_id: int, document_id: int):
    """
    Open the bot's context in the file explorer
    """
    globals.context_manager.get_context(context_id).open_document(document_id)
    return {"message": "Documents folder opened"}

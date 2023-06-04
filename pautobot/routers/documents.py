from fastapi import APIRouter, File, UploadFile

from pautobot import globals

router = APIRouter(
    prefix="/api",
    tags=["Documents"],
)


@router.get("/{context_id}/documents")
async def get_documents(context_id: str):
    """
    Get all documents in the bot's context
    """
    return globals.context_manager.get_context(context_id).get_documents()


@router.post("/{context_id}/documents")
async def upload_document(context_id: str, file: UploadFile = File(...)):
    """
    Upload a document to the bot's context
    """
    if not file:
        return {"message": "No file sent"}
    else:
        globals.context_manager.get_context(context_id).add_document(file)
        return {"message": "File uploaded"}


@router.delete("/{context_id}/documents/{document_id}")
async def delete_document(context_id: str, document_id: str):
    """
    Delete a document from the bot's context
    """
    globals.context_manager.get_context(context_id).delete_document(
        document_id
    )
    globals.engine.ingest_documents(context_id=context_id)
    return {"message": "Document deleted"}


@router.post("/{context_id}/documents/ingest")
async def ingest_documents(context_id: str):
    """
    Ingest all documents in the bot's context
    """
    globals.engine.ingest_documents(context_id=context_id)
    return {"message": "Ingestion finished!"}


@router.post("/{context_id}/documents/open_in_file_explorer")
async def open_in_file_explorer(context_id: str):
    """
    Open the bot's context in the file explorer
    """
    globals.context_manager.get_context(context_id).open_documents_folder()
    return {"message": "Documents folder opened"}

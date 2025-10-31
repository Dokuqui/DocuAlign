import uuid
import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlmodel import Session

from db import crud
from services import storage
from db.database import get_session

router = APIRouter()


@router.post("/upload", tags=["Documents"])
async def upload_document(
    file: UploadFile = File(...), session: Session = Depends(get_session)
):
    """
    Handles uploading a new document.
    1. Saves the file to disk with a unique name.
    2. Creates a corresponding entry in the database.
    """
    if not file or not file.filename:
        raise HTTPException(
            status_code=400, detail="No file uploaded or file has no name."
        )

    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"

    stored_path = storage.save_file_to_disk(file, unique_filename)

    document = crud.create_document(
        session=session,
        original_file_name=file.filename,
        stored_path=stored_path,
        content_type=file.content_type or "application/octet-stream",
    )

    return {"documentId": document.id}


@router.get("/{id}", tags=["Documents"])
async def get_document(id: uuid.UUID, session: Session = Depends(get_session)):
    """
    Retrieves a document file by its ID.
    1. Fetches the document's metadata from the database.
    2. Serves the actual file from disk.
    """
    document = crud.get_document_by_id(session, id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found in database")

    file_path = storage.get_file_from_disk_path(document.stored_path)

    return FileResponse(
        path=file_path,
        media_type=document.content_type,
        filename=document.original_file_name,
    )

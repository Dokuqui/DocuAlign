import uuid
import os
from fastapi import APIRouter, Response, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlmodel import Session

from db import crud
from services import storage
from db.database import get_session
from services import pdf_processor
from models.schemas import DocumentEditRequest, DocumentText, DocumentTextBlocks

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


@router.get("/{id}/text", response_model=DocumentText, tags=["PDF Processing"])
async def get_document_text(id: uuid.UUID, session: Session = Depends(get_session)):
    """
    Extracts all plain text from an uploaded document.
    """
    document = crud.get_document_by_id(session, id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = storage.get_file_from_disk_path(document.stored_path)

    text = pdf_processor.extract_text_from_pdf(file_path)

    return DocumentText(document_id=str(id), text=text)


@router.get("/{id}/ocr", response_model=DocumentText, tags=["PDF Processing"])
async def ocr_document_text(id: uuid.UUID, session: Session = Depends(get_session)):
    """
    Extracts text from a document using OCR. This is slower but
    works for scanned images.
    """
    document = crud.get_document_by_id(session, id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = storage.get_file_from_disk_path(document.stored_path)

    text = pdf_processor.extract_text_with_ocr(file_path)

    if "TESSERACT_NOT_FOUND_ERROR" in text:
        raise HTTPException(status_code=500, detail=text)

    return DocumentText(document_id=str(id), text=text)


@router.get(
    "/{id}/text-blocks", response_model=DocumentTextBlocks, tags=["PDF Processing"]
)
async def get_document_text_blocks(
    id: uuid.UUID, session: Session = Depends(get_session)
):
    """
    Extracts all text blocks with their coordinates from a document.
    """
    document = crud.get_document_by_id(session, id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = storage.get_file_from_disk_path(document.stored_path)

    blocks = pdf_processor.extract_text_blocks_from_pdf(file_path)

    return DocumentTextBlocks(document_id=str(id), blocks=blocks)


@router.get(
    "/{id}/ocr-blocks", response_model=DocumentTextBlocks, tags=["PDF Processing"]
)
async def get_document_ocr_blocks(
    id: uuid.UUID, session: Session = Depends(get_session)
):
    """
    Extracts all text blocks from a scanned document using OCR
    and returns them with their coordinates.
    """
    document = crud.get_document_by_id(session, id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = storage.get_file_from_disk_path(document.stored_path)

    try:
        blocks = pdf_processor.extract_ocr_blocks_from_pdf(file_path)
    except Exception as e:
        if "TESSERACT_NOT_FOUND_ERROR" in str(e):
            raise HTTPException(status_code=500, detail=str(e))
        raise HTTPException(
            status_code=500, detail=f"An error occurred during OCR processing: {e}"
        )

    return DocumentTextBlocks(document_id=str(id), blocks=blocks)


@router.post("/{id}/edit", tags=["PDF Processing"])
async def edit_document(
    id: uuid.UUID,
    edit_request: DocumentEditRequest,
    session: Session = Depends(get_session),
):
    """
    Applies text edits to a document and returns the modified PDF.
    This triggers a file download in the browser.
    """
    document = crud.get_document_by_id(session, id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = storage.get_file_from_disk_path(document.stored_path)

    try:
        modified_pdf_bytes = pdf_processor.edit_pdf_text(file_path, edit_request.edits)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to edit PDF: {e}")

    headers = {
        "Content-Disposition": f"attachment; filename=edited_{document.original_file_name}"
    }

    return Response(
        content=modified_pdf_bytes, media_type="application/pdf", headers=headers
    )

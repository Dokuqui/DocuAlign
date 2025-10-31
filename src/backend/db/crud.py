import uuid
from datetime import datetime
from sqlmodel import Session
from models.models import Document

def create_document(
    session: Session, 
    original_file_name: str, 
    stored_path: str, 
    content_type: str
) -> Document:
    """
    Creates and saves a new Document record in the database.
    """
    document = Document(
        original_file_name=original_file_name,
        stored_path=stored_path,
        content_type=content_type,
        uploaded_at=str(datetime.utcnow())
    )
    
    session.add(document)
    session.commit()
    session.refresh(document)
    
    return document

def get_document_by_id(session: Session, document_id: uuid.UUID) -> Document | None:
    """
    Retrieves a single Document by its primary key (ID).
    """
    document = session.get(Document, document_id)
    return document
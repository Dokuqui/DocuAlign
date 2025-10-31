import uuid
from typing import Optional
from sqlmodel import Field, SQLModel


class Document(SQLModel, table=True):
    """
    Represents a single uploaded document in the database.
    """

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    original_file_name: str
    stored_path: str
    content_type: str
    uploaded_at: str

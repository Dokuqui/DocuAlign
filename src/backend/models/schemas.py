from pydantic import BaseModel
from typing import List


class DocumentText(BaseModel):
    """
    Response model for simple text extraction.
    """

    document_id: str
    text: str


class TextBlock(BaseModel):
    """
    Represents a single block of text with its coordinates.
    Coordinates are in PDF points (72 points = 1 inch).
    (x0, y0) is the bottom-left corner.
    (x1, y1) is the top-right corner.
    """

    x0: float
    y0: float
    x1: float
    y1: float
    text: str
    page_num: int


class DocumentTextBlocks(BaseModel):
    """
    Response model for structured text block extraction.
    """

    document_id: str
    blocks: List[TextBlock]


class TextEdit(BaseModel):
    """
    Represents a single edit operation.
    """

    page_num: int
    redact_coords: List[float]
    new_text: str
    insert_coords: List[float]
    fontsize: float = 11
    fontname: str = "helv"


class DocumentEditRequest(BaseModel):
    """
    The request body for the /edit endpoint.
    """

    edits: List[TextEdit]

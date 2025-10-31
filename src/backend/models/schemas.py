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

from typing import List
import fitz
import pytesseract
from PIL import Image
import io
from models.schemas import TextBlock
from pytesseract import Output


def extract_text_from_pdf(file_path: str) -> str:
    """
    Opens a PDF from a given file path and extracts all text.
    """
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return ""

    full_text = ""
    for page in doc:
        full_text += page.get_text()

    doc.close()
    return full_text


def extract_text_with_ocr(file_path: str) -> str:
    """
    Opens a PDF, converts each page to an image, and uses Tesseract OCR
    to extract text. This is for scanned or image-based documents.
    """
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return ""

    full_text = ""
    zoom = 300 / 72
    matrix = fitz.Matrix(zoom, zoom)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        pix = page.get_pixmap(matrix=matrix)
        image_bytes = pix.tobytes("png")

        pil_image = Image.open(io.BytesIO(image_bytes))

        try:
            page_text = pytesseract.image_to_string(pil_image, lang="eng")
            full_text += f"--- Page {page_num + 1} ---\n{page_text}\n\n"
        except pytesseract.TesseractNotFoundError:
            doc.close()
            return "TESSERACT_NOT_FOUND_ERROR: 'tesseract' command not found. Please install Tesseract OCR engine and ensure it's in your system's PATH."
        except Exception as ocr_error:
            print(f"Error during Tesseract processing: {ocr_error}")
            full_text += f"--- Page {page_num + 1} (Error) ---\n"

    doc.close()
    return full_text


def extract_text_blocks_from_pdf(file_path: str) -> List[TextBlock]:
    """
    Opens a PDF and extracts all text blocks with their coordinates.
    This uses the *digital* text, not OCR.
    """
    all_blocks: List[TextBlock] = []
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return all_blocks

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        blocks = page.get_text("blocks")

        for b in blocks:
            x0, y0, x1, y1, text, block_no, block_type = b

            if block_type == 0:
                all_blocks.append(
                    TextBlock(
                        x0=x0,
                        y0=y0,
                        x1=x1,
                        y1=y1,
                        text=text.strip(),
                        page_num=page_num + 1,
                    )
                )

    doc.close()
    return all_blocks


def extract_ocr_blocks_from_pdf(file_path: str) -> List[TextBlock]:
    """
    Opens a PDF, renders it as images, and uses Tesseract OCR
    to extract text blocks *with coordinates*.
    """
    all_blocks: List[TextBlock] = []
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return all_blocks

    zoom = 300 / 72
    matrix = fitz.Matrix(zoom, zoom)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        pix = page.get_pixmap(matrix=matrix)
        image_bytes = pix.tobytes("png")
        pil_image = Image.open(io.BytesIO(image_bytes))

        try:
            data = pytesseract.image_to_data(
                pil_image, lang="eng", output_type=Output.DICT
            )
        except pytesseract.TesseractNotFoundError:
            doc.close()
            raise Exception(
                "TESSERACT_NOT_FOUND_ERROR: 'tesseract' command not found. Please install Tesseract OCR engine and ensure it's in your system's PATH."
            )
        except Exception as ocr_error:
            print(f"Error during Tesseract data processing: {ocr_error}")
            continue

        n_boxes = len(data["level"])
        for i in range(n_boxes):
            if data["level"][i] == 5:
                text = data["text"][i].strip()
                if not text:
                    continue

                left_px = data["left"][i]
                top_px = data["top"][i]
                width_px = data["width"][i]
                height_px = data["height"][i]

                x0 = left_px / zoom
                x1 = (left_px + width_px) / zoom

                y0 = page.rect.height - ((top_px + height_px) / zoom)
                y1 = page.rect.height - (top_px / zoom)

                all_blocks.append(
                    TextBlock(
                        x0=x0, y0=y0, x1=x1, y1=y1, text=text, page_num=page_num + 1
                    )
                )

    doc.close()
    return all_blocks

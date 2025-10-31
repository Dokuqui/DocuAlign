import os
import shutil
from fastapi import UploadFile, HTTPException
from core.config import UPLOAD_DIRECTORY


def save_file_to_disk(file: UploadFile, unique_filename: str) -> str:
    """
    Saves an uploaded file to the UPLOAD_DIRECTORY.
    Returns the stored path (which is just the unique filename).
    """
    file_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")

    return unique_filename


def get_file_from_disk_path(stored_path: str) -> str:
    """
    Gets the full, absolute file path from the stored_path.
    Raises a 404 error if the file doesn't exist.
    """
    file_path = os.path.join(UPLOAD_DIRECTORY, stored_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")

    return file_path

import os

DATABASE_FILE = "docualign.db"
UPLOAD_DIRECTORY = "Uploads"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

ALLOWED_ORIGINS = ["http://localhost:5173"]

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

import os
from fastapi import APIRouter, File, UploadFile, HTTPException
from controllers.statement_controller import *
from services.transactions_service import *

router = APIRouter()

# Define directory to store uploaded files
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/file")
async def upload_file(files: list[UploadFile] = File(...)):
    """
    Handles the upload of PDF files via a POST request.
    Endpoint:
        POST /upload/file
    Args:
        files (list[UploadFile]): A list of files to be uploaded. Each file must be a PDF.
    Returns:
        dict: A dictionary containing:
            - "uploaded_files" (list[dict]): A list of successfully uploaded files with their filenames and statuses.
            - "failed_files" (list[dict]): A list of files that failed to upload with their filenames and error messages.
    Raises:
        Exception: If an error occurs while saving a file to the upload directory.
    Notes:
        - Files that are not PDFs will be rejected.
        - Duplicate files (files with the same name as an existing file in the upload directory) will be rejected.
        - Successfully uploaded files are saved to the specified upload directory.
    """
    # Clear the upload directory before processing new files
    clear_upload_dir()

    # Maintain the uploaded files
    uploaded_files = []
    failed_files = []
    
    for file in files:
        # Check if the file is a PDF
        if not file.filename.endswith(".pdf"):
            failed_files.append({"filename": file.filename, "error": "File must be a PDF"})
            continue
        
        # Check if the file already exists
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        if os.path.exists(file_path):
            failed_files.append({"filename": file.filename, "error": "Duplicate file. File already exists."})
            continue

        try:
            # Save the file to the upload directory
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as f:
                f.write(await file.read())

            # Save the file content to memory or storage (if needed)
            # For now, we just append the filename to the uploaded list
            uploaded_files.append({"filename": file.filename, "status": "Uploaded successfully"})
        except Exception as e:
            failed_files.append({"filename": file.filename, "error": str(e)})

    return {
        "uploaded_files": uploaded_files,
        "failed_files": failed_files
    }

def clear_upload_dir():
    """
    Clears all files in the upload directory.
    """
    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
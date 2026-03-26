import os

from app.core.config import settings
from fastapi import UploadFile

# Define directory to store uploaded files
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


async def upload_files(files: list[UploadFile]) -> dict:
    """
    Handles uploading a list of statement files.

    Args:
        files (list[UploadFile]): list of statement files to be uploaded

    Raises:
        Exception: If an error occurs while processing the files.

    Returns:
        dict: A dictionary with two keys: "successful_files" and "failed_files".
        "successful_files" is a list of dictionaries, each containing the filename
        and status of successfully uploaded files. "failed_files" is a list of
        dictionaries, each containing the filename and error message for files that
        failed to upload.
    """

    processed_files = {"successful_files": [], "failed_files": []}

    for file in files:
        # Validate file format
        if not file.content_type == "application/pdf":
            processed_files["failed_files"].append(
                {
                    "filename": file.filename,
                    "error": "Unsupported file format. Only PDF files are allowed.",
                }
            )
            continue

        # Check if the file already exists
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        if os.path.exists(file_path):
            processed_files["failed_files"].append(
                {
                    "filename": file.filename,
                    "error": "Duplicate file. File already exists.",
                }
            )
            continue

        try:
            # Save the file to the upload directory
            file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as f:
                f.write(await file.read())

            # Save the file content to memory or storage (if needed)
            # For now, we just append the filename to the uploaded list
            processed_files["successful_files"].append(
                {"filename": file.filename, "status": "Uploaded successfully"}
            )
        except Exception as e:
            processed_files["failed_files"].append(
                {"filename": file.filename, "error": str(e)}
            )

    return processed_files

import os
import pdfplumber

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


async def parse_statements(files_path: str) -> dict:
    """
    Placeholder function for parsing statement files.

    Args:
        files_path (str): The directory containing the statement files to be parsed

    Returns:
        dict: A dictionary containing the parsed financial data from the statement files.
    """
    
    processed_files = {"successful_files": [], "failed_files": []}
    
    for filename in os.listdir(files_path):
        file_path = os.path.join(files_path, filename)
        try:
            # Open the file and call process_statement
            with open(file_path, "rb") as f:
                file_content = UploadFile(filename=filename, file=f)
                extracted_transactions = await process_statement(file_content)
                transactions.extend(extracted_transactions)
        except Exception as e:
            failed_files.append({"filename": filename, "error": str(e)})



async def process_statement(file: UploadFile) -> list[dict]:
    """
    Placeholder function for processing a single statement file.

    Args:
        file (UploadFile): The statement file to be
        processed
        """
        
    with pdfplumber.open(file_stream) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    # Split the text into lines
    lines = text.split("\n")

    # Extract transactions
    transactions = []
    for line in lines:
        for pattern in TRANSACTION_PATTERNS:
            match = pattern.match(line)
            if match:
                transactions.append(
                    {
                        "transaction_date": match.group("transaction_date"),
                        "posting_date": (
                            match.group("posting_date")
                            if "posting_date" in match.groupdict()
                            else None
                        ),
                        "description": match.group("description").strip(),
                        "amount": (
                            -float(match.group("amount")[:-1])
                            if match.group("amount").endswith("-")
                            else float(match.group("amount"))
                        ),
                    }
                )
                break  # Stop checking other patterns once a match is found

    return transactions

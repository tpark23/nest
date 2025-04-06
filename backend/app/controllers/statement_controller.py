from io import BytesIO
from fastapi import UploadFile
from services.transactions_service import extract_transactions_from_statement

async def process_statement(file: UploadFile) -> list:
    """
    Process the uploaded bank statement and extract transactions.
    """
    # Read the file content into memory
    content = await file.read()
    file_stream = BytesIO(content)

    # Call the service to extract transactions
    transactions = extract_transactions_from_statement(file_stream)

    return transactions
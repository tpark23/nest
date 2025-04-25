from fastapi import APIRouter, File, UploadFile, HTTPException
from controllers.statement_controller import *
from services.transactions_service import *

router = APIRouter()

@router.post("/upload/statement")
async def upload_bank_statement_and_get_transactions(file: UploadFile = File(...)):
    """
    Extract transactions from an uploaded PDF file.
    """

    # Allow PDF files only
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Statement must be a PDF")

    # # Read the file content and read into memory
    # content = await file.read()
    # file_stream = BytesIO(content)

    # # Pass file content to extract_transactions function
    # transactions = extract_transactions_from_statement(file_stream)
    transactions = await process_statement(file)
    #
    if not transactions:
        raise HTTPException(status_code=400, detail="No transactions found in the statement")

    return {"total_transactions": len(transactions), "transactions": transactions}
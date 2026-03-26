from fastapi import APIRouter, HTTPException, File, UploadFile, status
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.services.statements import upload_files

router = APIRouter(prefix="/statements", tags=["upload"])


@router.post("/upload")
async def upload_statements(files: list[UploadFile] = File(...)):
    """
    Uploads one or more bank statements for later processing.

    Args:
        files (list[UploadFile]): A list of statement files to be uploaded. Each file must be in PDF format.

    Raises:
        HTTPException: If no files are uploaded or if the number of files exceeds the limit.
        HTTPException: If an error occurs while processing the files.

    Returns:
        JSONResponse: A JSON response indicating the status of the upload operation.

    """

    # Validate request input
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    if len(files) > settings.MAX_FILES_PER_UPLOAD:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum {settings.MAX_FILES_PER_UPLOAD} files per upload",
        )

    # Process the uploaded files
    try:
        result = await upload_files(files)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error occurred while processing files: {str(e)}"
        )

    # File counts
    total_files_count = len(result["successful_files"]) + len(result["failed_files"])
    successful_files_count = len(result["successful_files"])
    failed_files_count = len(result["failed_files"])

    # 400 Bad Request
    if not result["successful_files"]:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status_desc": "Bad Request",
                "message": "All files failed to upload. Please check the details for each file.",
                "total_files_count": total_files_count,
                "successful_files_count": successful_files_count,
                "failed_files_count": failed_files_count,
                "files": result,
            },
        )

    # 207 Partial Success
    if result["failed_files"]:
        return JSONResponse(
            status_code=status.HTTP_207_MULTI_STATUS,
            content={
                "status_desc": "Partial Success",
                "message": "Some files failed to upload. Please check the details for each file.",
                "total_files_count": total_files_count,
                "successful_files_count": successful_files_count,
                "failed_files_count": failed_files_count,
                "files": result,
            },
        )

    # 200 Success
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status_desc": "Success",
            "message": "All files processed successfully",
            "total_files_count": total_files_count,
            "successful_files_count": successful_files_count,
            "failed_files_count": failed_files_count,
            "files": result,
        },
    )

from fastapi import APIRouter
from controllers.root_controller import home_message

router = APIRouter()

@router.get("/")
def root():
    return home_message()
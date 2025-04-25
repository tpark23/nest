import uvicorn
from fastapi import FastAPI
from routes import root, upload_file, upload_statement

app = FastAPI()

app.include_router(root.router)
app.include_router(upload_file.router)
app.include_router(upload_statement.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
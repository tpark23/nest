import uvicorn
from fastapi import FastAPI
from routes import root

app = FastAPI()

app.include_router(root.router)



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
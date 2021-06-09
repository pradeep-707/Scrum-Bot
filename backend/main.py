import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

from app.database import connectDb
from routes.members import router as member_router

load_dotenv()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

app = FastAPI()

app.include_router(member_router, tags=["member"], prefix="/student")

def setup():
	connectDb(os.environ.get("MONGO_URI"))

setup()

@app.get("/", tags=["Root"], response_description="Hello World")
async def read_root():
    return {"message": "Hello World"}

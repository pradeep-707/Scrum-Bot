import os
from fastapi.param_functions import Depends
import uvicorn
from fastapi import FastAPI, Header, Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dotenv import load_dotenv

from app.events import createStartAppHandler, createStopAppHandler
from app.utils import AuthorizationHeader
from routes.auth import router as member_router

load_dotenv()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

app = FastAPI()


app.include_router(member_router, tags=["auth"], prefix="/auth")

app.add_event_handler("startup", createStartAppHandler(app))
app.add_event_handler("shutdown", createStopAppHandler(app))


def callMe(name: str):
    def funcc(req: Request):
        print("Headers : ", req.headers)
    return funcc

@app.get("/", tags=["Root"], response_description="Hello World")
async def read_root():

    return {"message": "Hello World"}

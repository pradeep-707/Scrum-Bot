import os
from fastapi.param_functions import Depends
import uvicorn
from fastapi import FastAPI, Header, Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.events import createStartAppHandler, createStopAppHandler
from routes.auth import router as member_router
from routes.bot import router as bot_router

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, debug=True)

app = FastAPI(debug=True)


app.include_router(member_router, tags=["auth"], prefix="/auth")
app.include_router(bot_router, tags=["bot"], prefix="/bot")

app.add_event_handler("startup", createStartAppHandler(app))
app.add_event_handler("shutdown", createStopAppHandler(app))


@app.get("/", tags=["Root"], response_description="Hello World")
async def read_root():
    return {"message": "Hello World"}

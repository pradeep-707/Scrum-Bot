from pydantic import BaseModel, Field

class StartScrumResponse(BaseModel):
    scrumId: str = Field(...)
    scrumName: str = Field(...)

class EndScrumResponse(BaseModel):
    scrumName: str = Field(...)

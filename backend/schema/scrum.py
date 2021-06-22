from pydantic import BaseModel, Field

# API Response Models
class StartScrumResponse(BaseModel):
    scrumId: str = Field(...)
    scrumName: str = Field(...)

class EndScrumResponse(BaseModel):
    scrumName: str = Field(...)

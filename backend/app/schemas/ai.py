from pydantic import BaseModel, Field


class AIChatRequest(BaseModel):
    message: str = Field(min_length=1)
    language: str | None = None


class AIChatResponse(BaseModel):
    reply: str
    model: str
    used_fallback: bool = False

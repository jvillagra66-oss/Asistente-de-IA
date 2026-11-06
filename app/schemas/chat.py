from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    user_id: str = Field(..., description="ID único del usuario")
    channel: str = Field(..., description="Canal: telegram, whatsapp, instagram, onlyfans")
    message: str = Field(..., description="Mensaje del usuario")

class ChatResponse(BaseModel):
    user_id: str
    channel: str
    reply: str
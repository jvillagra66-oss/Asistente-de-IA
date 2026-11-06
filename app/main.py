from fastapi import FastAPI, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.langchain_agent import agent_service

app = FastAPI(title="Agente de IA Multicanal")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Servidor de Agente IA listo"}

@app.post("/api/chat", response_model=ChatResponse)
def handle_chat(payload: ChatRequest):
    try:
        reply_text = agent_service.process_message(
            user_id=payload.user_id,
            channel=payload.channel,
            message=payload.message
        )
        return ChatResponse(
            user_id=payload.user_id,
            channel=payload.channel,
            reply=reply_text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
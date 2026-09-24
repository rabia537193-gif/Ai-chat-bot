from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Any
import os
import groq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    mode: Optional[str] = "basic"
    language: Optional[str] = "en"
    messages: Optional[List[Any]] = None

@app.post("/chat")
@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": "GROQ_API_KEY is missing in Vercel settings."
                }
            )

        client = groq.Groq(api_key=api_key)

        models_page = client.models.list()
        active_models = [m.id for m in models_page.data if getattr(m, "active", True)]

        preferred_order = [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768"
        ]

        ordered_models = [m for m in preferred_order if m in active_models]
        ordered_models += [m for m in active_models if m not in ordered_models]

        if not ordered_models:
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": "No active models available for this GROQ API key."
                }
            )

        response = None
        used_model = ""
        last_err = None

        # Build message context
        messages_to_send = []
        if req.messages:
            for msg in req.messages:
                if isinstance(msg, dict) and "role" in msg and "content" in msg:
                    messages_to_send.append({"role": msg["role"], "content": msg["content"]})
        
        if not messages_to_send:
            messages_to_send = [{"role": "user", "content": req.message}]

        for model_id in ordered_models:
            try:
                response = client.chat.completions.create(
                    messages=messages_to_send,
                    model=model_id
                )
                if response:
                    used_model = model_id
                    break
            except Exception as e:
                last_err = e
                continue

        if not response:
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": f"Failed across models. Last error: {str(last_err)}"
                }
            )

        reply_text = response.choices[0].message.content
        
        # Matches frontend `data.success`, `data.reply`, and `data.model`
        return JSONResponse(
            status_code=200, 
            content={
                "success": True,
                "reply": reply_text,
                "model": used_model
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )

@app.get("/")
async def root():
    return {"message": "Backend is running"}
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

@app.post("/chat")
@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return JSONResponse(
                status_code=500,
                content={"error": "GROQ_API_KEY is missing in Vercel settings."}
            )

        client = groq.Groq(api_key=api_key)

        # 1. Groq ki account-active models ki list dynamically fetch karein
        models_page = client.models.list()
        active_models = [m.id for m in models_page.data if getattr(m, "active", True)]

        # Soft preferences if available in active list
        preferred_order = [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768"
        ]

        # Order active models: preferred first, then remaining active ones
        ordered_models = [m for m in preferred_order if m in active_models]
        ordered_models += [m for m in active_models if m not in ordered_models]

        if not ordered_models:
            return JSONResponse(
                status_code=500,
                content={"error": "No active models available for this GROQ API key."}
            )

        # 2. Try against available active models dynamically
        response = None
        last_err = None

        for model_id in ordered_models:
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": req.message}],
                    model=model_id
                )
                if response:
                    break
            except Exception as e:
                last_err = e
                continue

        if not response:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed across active models. Last error: {str(last_err)}"}
            )

        reply_text = response.choices[0].message.content
        return JSONResponse(status_code=200, content={"reply": reply_text, "response": reply_text})

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.get("/")
async def root():
    return {"message": "Backend is running"}
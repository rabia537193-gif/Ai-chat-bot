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
                content={"error": "No active models available for this GROQ API key."}
            )

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
        
        # Standardize keys to match all common frontend response formats
        return JSONResponse(
            status_code=200, 
            content={
                "reply": reply_text, 
                "response": reply_text,
                "message": reply_text,
                "text": reply_text,
                "bot": reply_text
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.get("/")
async def root():
    return {"message": "Backend is running"}
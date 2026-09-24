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

# List of models to try in order of priority
MODELS_TO_TRY = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "llama3-8b-8192",
    "llama3-70b-8192",
    "mixtral-8x7b-32768",
    "gemma2-9b-it"
]

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
        
        response = None
        last_error = None

        # Try models one by one until one works
        for model_name in MODELS_TO_TRY:
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": req.message}],
                    model=model_name
                )
                if response:
                    break
            except Exception as err:
                last_error = err
                continue

        if not response:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed with all models. Last error: {str(last_error)}"}
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
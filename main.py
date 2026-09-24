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
        
        # Working & Tested Groq Model Name
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": req.message}],
            model="llama3-70b-8192"
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
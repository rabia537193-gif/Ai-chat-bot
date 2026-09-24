from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import groq

# FastAPI instance
app = FastAPI()

# Enable CORS taake frontend aur backend aapas mein communicate kar sakein
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema definition
class ChatRequest(BaseModel):
    message: str

# Combined route handler for /chat and /api/chat
@app.post("/chat")
@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="GROQ_API_KEY environment variable is not set")

        client = groq.Groq(api_key=api_key)
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": req.message}],
            model="llama3-8b-8192"
        )
        
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"status": "Backend is running fine"}
# 🤖 Groq AI Studio Chatbot

A fast and interactive AI Chatbot built with **FastAPI** backend and **HTML/CSS/JS** frontend, deployed on Vercel. It uses **Groq API** to provide rapid responses using active Llama 3 models.

---

## ✨ Features

- ⚡ **Super Fast Responses**: Powered by Groq's high-speed Llama 3 models (`llama-3.3-70b-versatile`, `llama-3.1-8b-instant`).
- 🌐 **Multi-Language Support**: Supports both **English** and **Roman Urdu / Urdu**.
- 💬 **Multiple Modes**: 
  - **Basic Chat**: General conversational AI.
  - **Document RAG Chat**: Context-aware queries.
- 🔄 **Smart Dynamic Model Selection**: Automatically filters out non-chat models (like `prompt-guard` or audio models) and picks the best available active LLM.
- 🎯 **CORS Enabled**: Ready for frontend-backend API interaction.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python), Groq SDK, Pydantic
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Deployment**: Vercel

---

## 🚀 Setup & Environment Variables

Make sure to add your Groq API Key in your Vercel Environment Variables:

| Key | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API Key from [Groq Console](https://console.groq.com/) |

---

## 📝 API Endpoints

### `POST /chat` or `/api/chat`
Sends a message to the AI model.

**Request Body:**
```json
{
  "message": "Hello!",
  "mode": "basic",
  "language": "en",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ]
}
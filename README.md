# 🤖 Dual-Mode AI Chatbot & RAG Assistant

A modern, responsive, dark-themed AI web interface powered by **Flask** and the **Groq API**. This application seamlessly toggles between a standard conversational AI chatbot and a Document-based Retrieval-Augmented Generation (RAG) system with full dynamic language support (English / Roman Urdu).

---

## 📹 Project Demo Video

Click the button below to watch the live application demonstration:

[![Watch Demo Video](https://img.shields.io/badge/▶️_Watch_Demo_Video-Google_Drive-0078D4?style=for-the-badge&logo=googledrive&logoColor=white)](https://drive.google.com/file/d/1Mhs7q3u4-8vOooREpWEo6vDtCCEHdeTg/view?usp=sharing)

---

## ✨ Features

- **Dual Interaction Modes**:
  - **Option 1 (Basic Chat)**: Real-time conversational AI assistant powered by high-speed Llama models via Groq.
  - **Option 2 (RAG Chat)**: Document-grounded assistant that retrieves and answers queries specifically based on knowledge files (`sample_docs/knowledge.txt`).
- **Dynamic Language Support (i18n)**: Instant switching between **English** and **Roman Urdu** for UI controls, prompts, and system instructions.
- **Automated Fallback Model Selection**: Automatically selects active, high-limit Llama models (`llama-3.1-8b-instant`) to eliminate API rate limits (429/404 errors).
- **Sleek UI/UX**: Custom dark-mode, ChatGPT-inspired UI with instant badge updates and responsive layouts.
- **Privacy & Security**: `.env` configuration ensures zero exposure of sensitive API credentials.

---

## 📁 Project Structure

```text
Ai chat bot/
├── .env                  # Private API keys (Excluded from Git)
├── .gitignore            # Git exclusion rules
├── app.py                # Main Flask Server & Groq API Integration
├── main.py               # Terminal-based CLI interface
├── chatbot.py            # Basic standalone chat module
├── README.md             # Project documentation
├── sample_docs/
│   └── knowledge.txt     # RAG knowledge base document
└── templates/
    └── index.html        # Modern Dark-Mode Web Dashboard
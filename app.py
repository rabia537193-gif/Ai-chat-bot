import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from groq import Groq

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("GROQ_API_KEY")
KNOWLEDGE_FILE = "sample_docs/knowledge.txt"

if not API_KEY or not API_KEY.startswith("gsk_"):
    print("[Error] GROQ_API_KEY .env file mein nahi mili ya invalid hai!")
    exit()

client = Groq(api_key=API_KEY)


def get_active_model():
    try:
        models_list = client.models.list()
        for m in models_list.data:
            model_id = m.id.lower()
            if "llama" in model_id and not any(x in model_id for x in ["vision", "guard"]):
                return m.id
        for m in models_list.data:
            model_id = m.id.lower()
            if not any(x in model_id for x in ["whisper", "guard", "vision", "audio", "embed"]):
                return m.id
    except Exception:
        pass
    return "llama-3.1-8b-instant"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    mode = data.get("mode", "basic")
    language = data.get("language", "en")
    messages = data.get("messages", [])
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"success": False, "error": "Message body empty hai."}), 400

    model = get_active_model()
    
    # System Instruction according to selected language
    if language == "ur":
        sys_instruction = "You are a helpful AI assistant. Always respond in Roman Urdu or Urdu language."
    else:
        sys_instruction = "You are a helpful AI assistant. Always respond in clear English."

    try:
        if mode == "rag":
            folder_path = os.path.dirname(KNOWLEDGE_FILE)
            if folder_path and not os.path.exists(folder_path):
                os.makedirs(folder_path)

            if not os.path.exists(KNOWLEDGE_FILE):
                with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
                    f.write("Sample Knowledge Document: AI Travel Planner helps users organize itineraries, book tickets, and manage travel details.")

            with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
                document = f.read()

            rag_messages = [
                {"role": "system", "content": f"{sys_instruction} Answer using only the provided document below."},
                {"role": "user", "content": f"Document:\n{document}\n\nQuestion: {user_message}"}
            ]

            response = client.chat.completions.create(
                messages=rag_messages,
                model=model,
                max_tokens=500
            )
        else:
            api_messages = [{"role": "system", "content": sys_instruction}]
            api_messages.extend(messages)

            response = client.chat.completions.create(
                messages=api_messages,
                model=model,
                max_tokens=500
            )

        reply = response.choices[0].message.content
        return jsonify({"success": True, "reply": reply, "model": model})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
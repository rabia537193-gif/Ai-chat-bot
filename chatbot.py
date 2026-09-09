import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY or not API_KEY.startswith("gsk_"):
    print("\n[Error] GROQ_API_KEY .env file mein nahi mili ya invalid hai!")
    print("Barae meharbani apni .env file check karein.")
    exit()

client = Groq(api_key=API_KEY)


def get_active_model():
    """Dynamically fetches the first active text model available for the API key."""
    try:
        models_list = client.models.list()
        for m in models_list.data:
            model_id = m.id.lower()
            if not any(x in model_id for x in ["whisper", "guard", "vision", "audio", "embed"]):
                return m.id
    except Exception:
        pass
    return "llama-3.1-8b-instant"


def start_chatbot():
    model = get_active_model()
    conversation_history = [
        {"role": "system", "content": "You are a helpful, smart, and friendly AI chatbot."}
    ]

    print("=" * 50)
    print(f"          🤖 AI CHATBOT READY! (Model: {model})")
    print("          Type 'exit' or 'quit' to end chat.")
    print("=" * 50 + "\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("\nAI Chatbot: Goodbye! Have a great day!\n")
            break

        conversation_history.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                messages=conversation_history,
                model=model
            )
            bot_reply = response.choices[0].message.content

            conversation_history.append({"role": "assistant", "content": bot_reply})
            print(f"\nAI Chatbot: {bot_reply}\n")
            print("-" * 50)

        except Exception as e:
            print(f"\n[API Error]: {e}\n")
            break


if __name__ == "__main__":
    start_chatbot()
    
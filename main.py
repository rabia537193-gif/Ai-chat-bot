import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
KNOWLEDGE_FILE = "sample_docs/knowledge.txt"


def get_client():
    if not API_KEY or not API_KEY.startswith("gsk_"):
        print("\n[Error] GROQ_API_KEY .env file mein nahi mili ya invalid hai!")
        print("Barae meharbani apni .env file check karein.")
        exit()
    return Groq(api_key=API_KEY)


def get_active_model(client):
    """Prefers lightweight, high-limit Llama models to avoid rate limit issues."""
    try:
        models_list = client.models.list()
        # Prefer llama models for free tier stability
        for m in models_list.data:
            if "llama" in m.id.lower() and not any(x in m.id.lower() for x in ["vision", "guard"]):
                return m.id

        # Fallback to any valid non-specialized model
        for m in models_list.data:
            if not any(x in m.id.lower() for x in ["whisper", "guard", "vision", "audio", "embed"]):
                return m.id
    except Exception:
        pass
    
    return "llama-3.1-8b-instant"


def basic_chat():
    client = get_client()
    model = get_active_model(client)

    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    print(f"\nBasic Groq Chat (Using Model: {model})")
    print("Type 'exit' to stop.\n")

    while True:
        prompt = input("You: ").strip()

        if not prompt or prompt.lower() in ("exit", "quit"):
            break

        messages.append({"role": "user", "content": prompt})

        try:
            # Set max_tokens=500 to satisfy Groq free tier limits
            response = client.chat.completions.create(
                messages=messages,
                model=model,
                max_tokens=500
            )

            reply = response.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})
            print(f"Assistant: {reply}\n")
        except Exception as e:
            print(f"\nAPI Error: {e}\n")
            break


def rag_chat():
    client = get_client()
    model = get_active_model(client)

    folder_path = os.path.dirname(KNOWLEDGE_FILE)
    if folder_path and not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if not os.path.exists(KNOWLEDGE_FILE):
        with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as file:
            file.write("Sample Knowledge Document: AI Travel Planner helps users organize itineraries, book tickets, and manage travel details.")
        print(f"Note: '{KNOWLEDGE_FILE}' auto-create kar diya gaya hai.")

    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
        document = file.read()

    print(f"\nGroq RAG Chat (Using Model: {model})")
    print(f"Using: {KNOWLEDGE_FILE}")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("You: ").strip()

        if not question or question.lower() in ("exit", "quit"):
            break

        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Answer using only the document below."},
                    {"role": "user", "content": f"Document:\n{document}\n\nQuestion: {question}"}
                ],
                model=model,
                max_tokens=500
            )

            print(f"Groq: {response.choices[0].message.content}\n")
        except Exception as e:
            print(f"\nAPI Error: {e}\n")
            break


def main():
    print("Groq API Demos")
    print("1. Basic Chat")
    print("2. RAG Chat")

    choice = input("Select an option (1 or 2): ").strip()

    if choice == "1":
        basic_chat()
    elif choice == "2":
        rag_chat()
    else:
        print("Invalid choice. Please select 1 or 2.")


if __name__ == "__main__":
    main()
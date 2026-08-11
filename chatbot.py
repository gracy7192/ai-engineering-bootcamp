from config import client


def chat():
    system_instruction = """
    You are an AI engineering tutor.Explain concepts clearly and practically.
    Use examples when helpful.
    Do not assume the user already knows advanced concepts."""
    history = []

    while True:
        question = input("You: ")

        if question.lower() == "exit":
            break

        history.append({
            "role": "user",
            "parts": [{"text": question}]
        })

        response = client.models.generate_content_stream(
        model="gemini-2.5-flash-lite",
        contents=history,
        config={
        "system_instruction": system_instruction
        }
)

        print("AI: ", end="")
        full_response = ""

        for chunk in response:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                full_response += chunk.text

        print()

        history.append({
            "role": "model",
            "parts": [{"text": full_response}]
        })
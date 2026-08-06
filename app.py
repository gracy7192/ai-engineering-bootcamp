from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
history = []
while True:
    question = input("You: ")
    
    if question.lower() == "exit":
        break

    history.append({
        "role": "user",
        "parts": [{"text": question}]
        })
    
    print(history)

    response = client.models.generate_content_stream(
        model="gemini-2.5-flash-lite",
        contents=history
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
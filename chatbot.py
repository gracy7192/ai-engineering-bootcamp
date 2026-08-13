from config import client

from retriever import get_embedding
from vector_store import search

def chat():
    system_instruction = """
    You are an AI engineering tutor.Use the provided context when answering questions about NovaTech.
    If the answer is not contained in the context, say you don't know based on the available information.
    Explain concepts clearly and practically.
    Use examples when helpful."""

    history = []

    while True:
        question = input("You: ")

        if question.lower() == "exit":
            break

        history.append({
            "role": "user",
            "parts": [{"text": question}]
        })

        question_embedding = get_embedding(question)

        search_results = search(question_embedding)

        print("\n--- RETRIEVAL DEBUG ---")

        for document, distance in zip(
        search_results["documents"][0],
        search_results["distances"][0]
        ):
           print(f"Distance: {distance}")
           print(document)
           print("-------------------------")

        relevant_chunks = search_results["documents"][0]
        context = "\n\n".join(relevant_chunks)

        response = client.models.generate_content_stream(
        model="gemini-2.5-flash-lite",
        contents=history + [
        {
            "role": "user",
            "parts": [{
                "text": f"Relevant context:\n{context}"
            }]
        }
    ],
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
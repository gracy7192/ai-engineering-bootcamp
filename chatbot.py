from config import client
from retriever import load_knowledge, chunk_text, retrieve_chunks

def chat():
    system_instruction = """
    You are an AI engineering tutor.Use the provided context when answering questions about NovaTech.
    If the answer is not contained in the context, say you don't know based on the available information.
    Explain concepts clearly and practically.
    Use examples when helpful."""

    knowledge = load_knowledge()
    chunks = chunk_text(knowledge)

    

    history = []

    while True:
        question = input("You: ")

        if question.lower() == "exit":
            break

        history.append({
            "role": "user",
            "parts": [{"text": question}]
        })

        relevant_chunks = retrieve_chunks(question, chunks)
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
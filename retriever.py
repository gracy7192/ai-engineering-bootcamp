from config import client
import numpy as np


def load_knowledge():
    with open("knowledge/company.txt", "r", encoding="utf-8") as file:
        return file.read()


def chunk_text(text):
    chunks = text.split("\n\n")
    return chunks


def get_embedding(text):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values


def cosine_similarity(vector_a, vector_b):
    a = np.array(vector_a)
    b = np.array(vector_b)

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve_chunks(question, chunks):
    question_embedding = get_embedding(question)

    scored_chunks = []

    for chunk in chunks:
        chunk_embedding = get_embedding(chunk)

        score = cosine_similarity(
            question_embedding,
            chunk_embedding
        )

        scored_chunks.append((score, chunk))

    scored_chunks.sort(reverse=True)

    return [chunk for score, chunk in scored_chunks[:2]]

knowledge = load_knowledge()
chunks = chunk_text(knowledge)

question = "How much annual leave do employees get?"

results = retrieve_chunks(question, chunks)

for result in results:
    print("\n--- Relevant chunk ---")
    print(result)
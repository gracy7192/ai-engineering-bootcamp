from config import client
import numpy as np


def load_knowledge():
    with open("knowledge/company.txt", "r", encoding="utf-8") as file:
        return file.read()


def chunk_text(text, chunk_size=3, overlap=1):
    paragraphs = text.split("\n\n")

    chunks = []

    start = 0

    while start < len(paragraphs):
        end = start + chunk_size

        chunk = "\n\n".join(paragraphs[start:end])
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def get_embedding(text):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values


def embed_chunks(chunks):
    embedded_chunks = []

    for chunk in chunks:
        embedding = get_embedding(chunk)

        embedded_chunks.append({
            "text": chunk,
            "embedding": embedding
        })

    return embedded_chunks
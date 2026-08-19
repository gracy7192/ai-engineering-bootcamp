from retriever import (
    load_knowledge,
    chunk_text,
    get_embedding
)

from vector_store import search
from keyword_search import keyword_search


def hybrid_search(question, chunks, top_k=4):
    # Semantic search
    question_embedding = get_embedding(question)

    semantic_results = search(
        question_embedding,
        top_k=len(chunks)
    )

    semantic_chunks = semantic_results["documents"][0]

    # Keyword search
    keyword_chunks = keyword_search(
        question,
        chunks,
        top_k=len(chunks)
    )

    scores = {}

    # Reciprocal Rank Fusion
    for rank, chunk in enumerate(semantic_chunks):
        scores[chunk] = scores.get(chunk, 0) + 1 / (60 + rank + 1)

    for rank, chunk in enumerate(keyword_chunks):
        scores[chunk] = scores.get(chunk, 0) + 1 / (60 + rank + 1)

    ranked_chunks = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return [chunk for chunk, score in ranked_chunks[:top_k]]

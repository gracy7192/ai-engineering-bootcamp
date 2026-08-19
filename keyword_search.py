import re


def keyword_search(question, chunks, top_k=4):
    question_words = set(
        re.findall(r"\b\w+\b", question.lower())
    )

    scored_chunks = []

    for chunk in chunks:
        chunk_words = set(
            re.findall(r"\b\w+\b", chunk.lower())
        )

        matches = question_words & chunk_words

        score = len(matches)

        scored_chunks.append((score, chunk))

    scored_chunks.sort(reverse=True)

    return [chunk for score, chunk in scored_chunks[:top_k]]


from retriever import load_knowledge, chunk_text


knowledge = load_knowledge()
chunks = chunk_text(knowledge)

question = "Where is NovaTech headquartered?"

results = keyword_search(question, chunks)

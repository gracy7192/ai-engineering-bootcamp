def load_knowledge():
    with open("knowledge/company.txt", "r", encoding="utf-8") as file:
        return file.read()


def chunk_text(text):
    chunks = text.split("\n\n")
    return chunks

def retrieve_chunks(question, chunks):
    question_words = question.lower().split()

    relevant_chunks = []

    for chunk in chunks:
        chunk_lower = chunk.lower()

        for word in question_words:
            if word in chunk_lower:
                relevant_chunks.append(chunk)
                break

    return relevant_chunks
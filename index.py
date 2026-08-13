from retriever import load_knowledge, chunk_text, embed_chunks
from vector_store import add_chunks


knowledge = load_knowledge()
chunks = chunk_text(knowledge)

print("Chunks being indexed:")

for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i} ---")
    print(chunk)

embedded_chunks = embed_chunks(chunks)

add_chunks(embedded_chunks)

print(f"\nIndexed {len(chunks)} chunks.")
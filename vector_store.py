import chromadb


client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="company_knowledge",
    metadata={"hnsw:space": "cosine"}
)


def add_chunks(embedded_chunks):
    for i, item in enumerate(embedded_chunks):
        collection.upsert(
            ids=[str(i)],
            documents=[item["text"]],
            embeddings=[item["embedding"]]
        )


def search(query_embedding, top_k=4):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "distances"]
    )

    return results
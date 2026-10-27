import chromadb
from openai import OpenAI

from config import API_KEY, EMBEDDING_MODEL, VECTOR_DB_PATH, VECTOR_COLLECTION_NAME
from steps.logger import log

client = OpenAI(base_url="https://api.gapgpt.app/v1", api_key=API_KEY)



def get_embedding(text):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding[:10]


def retrieve(indexed_records, retrieval_query, top_k):
    log("retrieve")
    query_embedding=get_embedding(retrieval_query)

    results = indexed_records.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    scored_chunks=[]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    for text,metadata,distance in zip(documents,metadatas,distances):
        score=1 - distance
        scored_chunk = {
            "id": metadata["id"],
            "source": metadata["source"],
            "text": text,
            "score": score
        }
        scored_chunks.append(scored_chunk)


    return scored_chunks


def get_vector_collection():
    log("get_vector_collection")
    client= chromadb.PersistentClient(path=VECTOR_DB_PATH)
    return client.get_or_create_collection(
        name=VECTOR_COLLECTION_NAME,
        metadata={"hnsw":"cosine"}
    )
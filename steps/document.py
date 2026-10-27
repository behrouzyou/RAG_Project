import collections

from config import RULES_FILE, CHUNK_SIZE
from steps.logger import log
from steps.retrieval import get_embedding, get_vector_collection


def load_documents():
    log("load_documents")
    file=open(RULES_FILE,"r",encoding="utf-8")
    text=file.read()
    file.close()
    return [text]


def clean(documents):
    log("clean_documents")
    cleaned_documents=[]
    for text in documents:
        text = text.replace("\r\n", "\n")
        text = text.strip()

        while "  " in text:
            text = text.replace("  ", " ")

        while "\n\n\n" in text:
            text = text.replace("\n\n\n", "\n\n")

        cleaned_documents.append(text)
    return cleaned_documents

def chunk_documents(clean_docs):
    log("chunk_documents")
    chunks = []

    for text in clean_docs:
        for start in range(0, len(text), CHUNK_SIZE):
            end = start + CHUNK_SIZE
            chunks.append(text[start:end])

    return chunks


def attach_metadata(chunks):
    log("attach_metadata_documents")
    chunk_records = []

    for index, chunk in enumerate(chunks):
        record = {
            "id": index + 1,
            "source": RULES_FILE,
            "text": chunk
        }
        chunk_records.append(record)

    return chunk_records

def embed_and_index(chunk_records):
    log("embedding_documents")
    collection = get_vector_collection()
    for record in chunk_records:
        embedding = get_embedding(record["text"])

        collection.upsert(
            ids=[str(record["id"])],
            documents=[record['text']],
            embeddings=[embedding],
            metadatas=[{
                "id": record["id"],
                "source": record["source"]
            }]
        )

    return collection
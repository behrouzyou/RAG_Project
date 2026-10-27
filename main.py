from steps.document import load_documents, clean, chunk_documents, attach_metadata, embed_and_index
from steps.generation import build_rag_prompt, generate_answer, validate_or_format
from steps.query import get_user_query, rewrite_query_if_needed
from steps.retrieval import retrieve, get_vector_collection


def run_rag_pipeline():
    # ingestion phase
    indexed_records=get_vector_collection()
    if indexed_records.count() == 0:
        documents = load_documents()
        clean_docs = clean(documents)
        chunks = chunk_documents(clean_docs)
        chunk_records = attach_metadata(chunks)
        indexed_records = embed_and_index(chunk_records)

    # query-time phase
    query = get_user_query()
    retrieval_query = rewrite_query_if_needed(query)
    retrieved_chunks = retrieve(indexed_records, retrieval_query, top_k=5)
    prompt = build_rag_prompt(query, retrieved_chunks)
    answer = generate_answer(prompt)
    final_answer = validate_or_format(answer)

    return final_answer


final_result = run_rag_pipeline()
print("the final result is:")
print(final_result)

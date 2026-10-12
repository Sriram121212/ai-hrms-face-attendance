import os
import uuid
import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

# Persistent storage - data survives server restarts, no re-upload needed
CHROMA_DIR = "chroma_data"
os.makedirs(CHROMA_DIR, exist_ok=True)

chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chroma_client.get_or_create_collection(name="hr_policy")

# Loaded once at startup, reused for every request (loading it per-request is slow)
embedder = SentenceTransformer("all-MiniLM-L6-v2")


def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Simple sliding-window chunker on words. Overlap keeps context from being cut mid-idea."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk)
        start = end - overlap
    return chunks


def store_chunks(chunks: list[str], doc_id: int, filename: str) -> int:
    """Embeds and stores chunks in ChromaDB, tagged with doc_id so they can be found/deleted later."""
    if not chunks:
        return 0

    embeddings = embedder.encode(chunks).tolist()
    ids = [str(uuid.uuid4()) for _ in chunks]
    metadatas = [{"doc_id": doc_id, "filename": filename, "chunk_index": i} for i in range(len(chunks))]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )
    return len(chunks)


def delete_doc_chunks(doc_id: int):
    """Used when re-uploading a new version of the same policy doc."""
    collection.delete(where={"doc_id": doc_id})


def retrieve_relevant_chunks(query: str, top_k: int = 3) -> list[str]:
    """Given a question, returns the most relevant stored chunks."""
    if collection.count() == 0:
        return []

    query_embedding = embedder.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)
    return results["documents"][0] if results["documents"] else []

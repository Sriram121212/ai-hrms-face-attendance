import os
import valkey
import hashlib
import json

VALKEY_HOST = os.getenv("VALKEY_HOST", "localhost")
client = valkey.Valkey(host=VALKEY_HOST, port=6379, decode_responses=True)
client = valkey.Valkey(host="localhost", port=6379, decode_responses=True)

# CACHE_TTL_SECONDS = 3600  # 1 hour
CACHE_TTL_SECONDS = 86400  # 24 hours instead of 1 hour

def get_cached_answer(question: str):
    key = f"rag:{hashlib.md5(question.lower().strip().encode()).hexdigest()}"
    cached = client.get(key)
    return json.loads(cached) if cached else None

def set_cached_answer(question: str, answer: dict):
    key = f"rag:{hashlib.md5(question.lower().strip().encode()).hexdigest()}"
    client.setex(key, CACHE_TTL_SECONDS, json.dumps(answer))
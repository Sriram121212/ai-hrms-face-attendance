# from groq import Groq
# from app.config import GROQ_API_KEY

# client = Groq(api_key=GROQ_API_KEY)

# MODEL = "llama-3.3-70b-versatile"

# # Groq pricing for llama-3.3-70b-versatile (per million tokens) - update if Groq changes pricing
# PRICE_PER_MILLION_INPUT = 0.59
# PRICE_PER_MILLION_OUTPUT = 0.79


# def answer_from_context(question: str, context_chunks: list[str]) -> dict:
#     """Sends retrieved context + question to Groq, returns answer plus token/cost info for logging."""
#     context_text = "\n\n".join(context_chunks) if context_chunks else "No relevant policy content found."

#     prompt = (
#         f"You are an HR policy assistant. Answer the employee's question using ONLY the context below. "
#         f"If the answer isn't in the context, say you don't have that information and suggest contacting HR.\n\n"
#         f"Context:\n{context_text}\n\n"
#         f"Question: {question}"
#     )

#     response = client.chat.completions.create(
#         model=MODEL,
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=400,
#     )

#     answer = response.choices[0].message.content
#     input_tokens = response.usage.prompt_tokens
#     output_tokens = response.usage.completion_tokens
#     total_tokens = response.usage.total_tokens

#     cost = (
#         (input_tokens / 1_000_000) * PRICE_PER_MILLION_INPUT
#         + (output_tokens / 1_000_000) * PRICE_PER_MILLION_OUTPUT
#     )

#     return {
#         "answer": answer,
#         "tokens_used": total_tokens,
#         "cost_usd": round(cost, 6),
#     }


from groq import Groq
from app.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

MODEL = "openai/gpt-oss-120b"  # llama-3.3-70b-versatile shuts down Aug 16, 2026

PRICE_PER_MILLION_INPUT = 0.15
PRICE_PER_MILLION_OUTPUT = 0.75


def answer_from_context(question: str, context_chunks: list[str]) -> dict:
    context_text = "\n\n".join(context_chunks) if context_chunks else "No relevant policy content found."

    # prompt = (
    #     f"You are an HR policy assistant. Answer the employee's question using ONLY the context below. "
    #     f"If the answer isn't in the context, say you don't have that information and suggest contacting HR.\n\n"
    #     f"Context:\n{context_text}\n\n"
    #     f"Question: {question}"
    # )

    
    prompt = (
    f"You are an HR policy assistant. Answer the employee's question using ONLY the context below. "
    f"Keep your answer to 2-3 sentences maximum, direct and to the point. "
    f"If the answer isn't in the context, say you don't have that information and suggest contacting HR.\n\n"
    f"Context:\n{context_text}\n\n"
    f"Question: {question}"
)
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150, #400,
    )

    answer = response.choices[0].message.content
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens
    total_tokens = response.usage.total_tokens

    cost = (
        (input_tokens / 1_000_000) * PRICE_PER_MILLION_INPUT
        + (output_tokens / 1_000_000) * PRICE_PER_MILLION_OUTPUT
    )

    return {"answer": answer, "tokens_used": total_tokens, "cost_usd": round(cost, 6)}
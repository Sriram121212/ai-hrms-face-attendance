# import json
# from groq import Groq
# from sqlalchemy.orm import Session

# from app.config import GROQ_API_KEY
# from app.admin_agent_tools import (
#     get_attendance_summary,
#     get_employee_attendance,
#     get_pending_leaves,
#     get_salary_info,
# )

# client = Groq(api_key=GROQ_API_KEY)
# MODEL = "openai/gpt-oss-120b"  # llama-3.3-70b-versatile shuts down Aug 16, 2026

# PRICE_PER_MILLION_INPUT = 0.15
# PRICE_PER_MILLION_OUTPUT = 0.75

# TOOLS = [
#     {
#         "type": "function",
#         "function": {
#             "name": "get_attendance_summary",
#             "description": "Get present/absent counts and names for a specific date. Use for questions like 'who was absent today' or 'how many people came in on 28th July'.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "date_str": {
#                         "type": "string",
#                         "description": "Date in YYYY-MM-DD format. Omit to default to today.",
#                     }
#                 },
#             },
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "get_employee_attendance",
#             "description": "Get attendance history for one specific employee by name, optionally filtered to one date.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "employee_name": {"type": "string", "description": "Employee's name (partial match ok)"},
#                     "date_str": {"type": "string", "description": "Optional specific date in YYYY-MM-DD format"},
#                 },
#                 "required": ["employee_name"],
#             },
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "get_pending_leaves",
#             "description": "Get all leave requests currently awaiting admin approval.",
#             "parameters": {"type": "object", "properties": {}},
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "get_salary_info",
#             "description": "Get a specific employee's salary slip for a given month and year.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "employee_name": {"type": "string"},
#                     "month": {"type": "integer", "description": "Month as a number, 1-12"},
#                     "year": {"type": "integer"},
#                 },
#                 "required": ["employee_name", "month", "year"],
#             },
#         },
#     },
# ]

# TOOL_FUNCTIONS = {
#     "get_attendance_summary": get_attendance_summary,
#     "get_employee_attendance": get_employee_attendance,
#     "get_pending_leaves": get_pending_leaves,
#     "get_salary_info": get_salary_info,
# }


# def run_admin_agent(question: str, db: Session) -> dict:
#     """
#     ReAct-style loop: model reasons about the question, calls a tool if it needs data,
#     we execute the tool against the real DB, feed the result back, model gives final answer.
#     """
#     messages = [
#         {
#             "role": "system",
#             "content": (
#                 "You are an HR admin assistant. Answer questions about employee attendance, "
#                 "leave requests, and salary using the available tools. Always call a tool to get "
#                 "real data before answering - never guess numbers. Keep answers concise and factual."
#             ),
#         },
#         {"role": "user", "content": question},
#     ]

#     total_input_tokens = 0
#     total_output_tokens = 0

#     response = client.chat.completions.create(
#         model=MODEL,
#         messages=messages,
#         tools=TOOLS,
#         max_tokens=500,
#     )
#     total_input_tokens += response.usage.prompt_tokens
#     total_output_tokens += response.usage.completion_tokens

#     response_message = response.choices[0].message

#     if response_message.tool_calls:
#         messages.append(response_message)

#         for tool_call in response_message.tool_calls:
#             func_name = tool_call.function.name
#             func_args = json.loads(tool_call.function.arguments or "{}")

#             tool_func = TOOL_FUNCTIONS.get(func_name)
#             result = tool_func(db, **func_args) if tool_func else {"error": "Unknown tool"}

#             messages.append({
#                 "role": "tool",
#                 "tool_call_id": tool_call.id,
#                 "content": json.dumps(result),
#             })

#         final_response = client.chat.completions.create(
#             model=MODEL,
#             messages=messages,
#             max_tokens=500,
#         )
#         total_input_tokens += final_response.usage.prompt_tokens
#         total_output_tokens += final_response.usage.completion_tokens
#         answer = final_response.choices[0].message.content
#     else:
#         answer = response_message.content

#     total_tokens = total_input_tokens + total_output_tokens
#     cost = (
#         (total_input_tokens / 1_000_000) * PRICE_PER_MILLION_INPUT
#         + (total_output_tokens / 1_000_000) * PRICE_PER_MILLION_OUTPUT
#     )

#     return {"answer": answer, "tokens_used": total_tokens, "cost_usd": round(cost, 6)}




import json
from groq import Groq
from sqlalchemy.orm import Session

from app.config import GROQ_API_KEY
from app.admin_agent_tools import (
    get_attendance_summary,
    get_employee_attendance,
    get_pending_leaves,
    get_salary_info,
)

client = Groq(api_key=GROQ_API_KEY)
MODEL = "openai/gpt-oss-120b"  # llama-3.3-70b-versatile shuts down Aug 16, 2026

PRICE_PER_MILLION_INPUT = 0.15
PRICE_PER_MILLION_OUTPUT = 0.75

# Tool schemas the model sees - it decides which one(s) to call based on the question
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_attendance_summary",
            "description": "Get present/absent counts and names for a specific date. Use for questions like 'who was absent today' or 'how many people came in on 28th July'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date_str": {
                        "type": ["string", "null"],
                        "description": "Date in YYYY-MM-DD format. Pass null or omit to default to today.",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_employee_attendance",
            "description": "Get attendance history for one specific employee by name, optionally filtered to one date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_name": {"type": "string", "description": "Employee's name (partial match ok)"},
                    "date_str": {"type": ["string", "null"], "description": "Optional specific date in YYYY-MM-DD format"},
                },
                "required": ["employee_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pending_leaves",
            "description": "Get all leave requests currently awaiting admin approval.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_salary_info",
            "description": "Get a specific employee's salary slip for a given month and year.",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_name": {"type": "string"},
                    "month": {"type": "integer", "description": "Month as a number, 1-12"},
                    "year": {"type": "integer"},
                },
                "required": ["employee_name", "month", "year"],
            },
        },
    },
]

TOOL_FUNCTIONS = {
    "get_attendance_summary": get_attendance_summary,
    "get_employee_attendance": get_employee_attendance,
    "get_pending_leaves": get_pending_leaves,
    "get_salary_info": get_salary_info,
}


def run_admin_agent(question: str, db: Session) -> dict:
    """
    ReAct-style loop: model reasons about the question, calls a tool if it needs data,
    we execute the tool against the real DB, feed the result back, model gives final answer.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are an HR admin assistant. Answer questions about employee attendance, "
                "leave requests, and salary using the available tools. Always call a tool to get "
                "real data before answering - never guess numbers. Keep answers concise and factual."
            ),
        },
        {"role": "user", "content": question},
    ]

    total_input_tokens = 0
    total_output_tokens = 0

    # First call - model decides whether to use a tool
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        max_tokens=500,
    )
    total_input_tokens += response.usage.prompt_tokens
    total_output_tokens += response.usage.completion_tokens

    response_message = response.choices[0].message

    if response_message.tool_calls:
        messages.append(response_message)

        for tool_call in response_message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments or "{}")

            tool_func = TOOL_FUNCTIONS.get(func_name)
            result = tool_func(db, **func_args) if tool_func else {"error": "Unknown tool"}

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result),
            })

        # Second call - model formulates the final natural-language answer using tool results
        final_response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=500,
        )
        total_input_tokens += final_response.usage.prompt_tokens
        total_output_tokens += final_response.usage.completion_tokens
        answer = final_response.choices[0].message.content
    else:
        answer = response_message.content

    total_tokens = total_input_tokens + total_output_tokens
    cost = (
        (total_input_tokens / 1_000_000) * PRICE_PER_MILLION_INPUT
        + (total_output_tokens / 1_000_000) * PRICE_PER_MILLION_OUTPUT
    )

    return {
        "answer": answer,
        "tokens_used": total_tokens,
        "cost_usd": round(cost, 6),
    }
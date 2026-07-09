"""
agent.py
--------
Core agent loop: send conversation to Gemini, execute any tool calls
it requests, feed results back, repeat until the model gives a final
text answer.
"""

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from tools import AVAILABLE_TOOLS
from tool_schemas import GEMINI_TOOLS

load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not found. Copy .env.example to .env and add your key."
    )

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

SYSTEM_PROMPT = """You are a helpful travel planning agent.
You can check weather, search flights, and search hotels using the tools available.
Always use tools to get real information rather than guessing.
Once you have enough information, produce a clear day-by-day itinerary
with estimated costs. Ask the user clarifying questions if key details
(dates, budget, origin city) are missing."""


def run_agent(user_message: str, history: list[types.Content]) -> list[types.Content]:
    """
    Sends the user's message plus prior history to Gemini, executes any
    tool calls the model requests, and loops until a final text answer
    is produced. Returns the updated history.
    """
    history.append(types.Content(role="user", parts=[types.Part(text=user_message)]))

    while True:
        response = client.models.generate_content(
            model=MODEL,
            contents=history,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[GEMINI_TOOLS],
            ),
        )

        candidate = response.candidates[0]
        history.append(candidate.content)

        function_calls = [
            part.function_call
            for part in candidate.content.parts
            if part.function_call
        ]

        if not function_calls:
            print("\nAgent:", response.text)
            return history

        tool_response_parts = []
        for fc in function_calls:
            fn_name = fc.name
            args = dict(fc.args)
            print(f"\n[Agent is calling tool: {fn_name}({args})]")

            if fn_name in AVAILABLE_TOOLS:
                result = AVAILABLE_TOOLS[fn_name](**args)
            else:
                result = {"error": f"Unknown tool {fn_name}"}

            tool_response_parts.append(
                types.Part.from_function_response(
                    name=fn_name,
                    response={"result": result},
                )
            )

        history.append(types.Content(role="user", parts=tool_response_parts))
        # Loop again so the model can use the tool results

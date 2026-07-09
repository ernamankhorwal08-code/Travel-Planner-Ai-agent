"""
tool_schemas.py
----------------
Describes each tool to Gemini so the model knows what it can call,
and with what arguments. Keep these in sync with the function
signatures in tools.py.
"""

from google.genai import types

GEMINI_TOOLS = types.Tool(function_declarations=[
    types.FunctionDeclaration(
        name="get_weather",
        description="Get current weather for a given city",
        parameters={
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name, e.g. Tokyo"}
            },
            "required": ["city"],
        },
    ),
    types.FunctionDeclaration(
        name="search_flights",
        description="Search flights between two cities on a specific date",
        parameters={
            "type": "object",
            "properties": {
                "origin": {"type": "string", "description": "Origin city"},
                "destination": {"type": "string", "description": "Destination city"},
                "date": {"type": "string", "description": "Travel date, YYYY-MM-DD"},
            },
            "required": ["origin", "destination", "date"],
        },
    ),
    types.FunctionDeclaration(
        name="search_hotels",
        description="Search hotels in a city for given check-in/check-out dates",
        parameters={
            "type": "object",
            "properties": {
                "city": {"type": "string"},
                "checkin": {"type": "string", "description": "YYYY-MM-DD"},
                "checkout": {"type": "string", "description": "YYYY-MM-DD"},
                "budget": {
                    "type": "string",
                    "enum": ["budget", "mid-range", "luxury"],
                },
            },
            "required": ["city", "checkin", "checkout"],
        },
    ),
])

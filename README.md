# ✈️ Travel Planner AI Agent

A simple, extensible AI agent built with the **Gemini API** that plans trips by
calling tools for weather, flights, and hotels — then assembles a day-by-day
itinerary with cost estimates.

Built as a beginner-friendly example of the core agent pattern:

```
User message → LLM decides which tool(s) to call → tool executes →
result fed back to LLM → LLM reasons again → ... → final answer
```

## Features

- 🌤️ **Real weather data** via the free [Open-Meteo](https://open-meteo.com/) API (no key needed)
- ✈️ **Flight search** (mock data — swap in a real API like Amadeus)
- 🏨 **Hotel search** (mock data — swap in a real API like Booking.com)
- 🔁 Full agentic tool-use loop using Gemini function calling
- 💬 Simple CLI chat interface

## Project structure

```
travel-planner-agent/
├── main.py           # CLI entry point
├── agent.py           # Core agent loop (LLM + tool execution)
├── tools.py            # Tool functions (weather, flights, hotels)
├── tool_schemas.py     # Tool definitions Gemini uses to decide what to call
├── requirements.txt
├── .env.example         # Template for your API key (copy to .env)
└── .gitignore
```

## Setup

### 1. Clone this repo
```bash
git clone https://github.com/YOUR_USERNAME/travel-planner-agent.git
cd travel-planner-agent
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Gemini API key
Get a free key at [Google AI Studio](https://aistudio.google.com/apikey).

```bash
cp .env.example .env
```
Then open `.env` and paste your key:
```
GEMINI_API_KEY=your_real_key_here
```

⚠️ **Never commit `.env` to GitHub.** It's already in `.gitignore`.

### 5. Run it
```bash
python main.py
```

## Example

```
You: Plan a 4-day trip from Delhi to Bangkok in December, mid-range budget

[Agent is calling tool: search_flights({'origin': 'Delhi', 'destination': 'Bangkok', 'date': '2026-12-01'})]
[Agent is calling tool: search_hotels({'city': 'Bangkok', 'checkin': '2026-12-01', 'checkout': '2026-12-05', 'budget': 'mid-range'})]
[Agent is calling tool: get_weather({'city': 'Bangkok'})]

Agent: Here's your 4-day Bangkok itinerary...
```

## Next steps / ideas to extend

- Replace mock `search_flights` / `search_hotels` with real APIs (Amadeus, Booking.com, Skyscanner)
- Add a database (SQLite) to remember user preferences across sessions
- Add a `check_visa_requirements` tool
- Build a web UI with Streamlit or a React frontend
- Add budget-tracking / currency conversion tools

## Security note

If you ever accidentally paste or commit a real API key anywhere public,
**revoke it immediately** in Google AI Studio and generate a new one.

## License

MIT — free to use and modify.

"""
tools.py
--------
All "tool" functions the agent can call. Each function is plain Python;
the agent (in agent.py) decides when to call them based on the user's request.

Weather uses a real, free, no-key API (Open-Meteo).
Flights and hotels are MOCK data — swap these out for a real API
(e.g. Amadeus, Booking.com) when you're ready. The agent loop doesn't
need to change, only the body of these two functions.
"""

import requests


def get_weather(city: str) -> dict:
    """Get current weather for a city using the free Open-Meteo API."""
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1},
        timeout=10,
    ).json()

    if not geo.get("results"):
        return {"error": f"Could not find location: {city}"}

    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]

    weather = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": lat, "longitude": lon, "current_weather": True},
        timeout=10,
    ).json()

    current = weather.get("current_weather", {})
    return {
        "city": city,
        "temperature_c": current.get("temperature"),
        "windspeed_kmh": current.get("windspeed"),
    }


def search_flights(origin: str, destination: str, date: str) -> dict:
    """Search flights between two cities on a given date (MOCK DATA)."""
    return {
        "origin": origin,
        "destination": destination,
        "date": date,
        "options": [
            {"airline": "IndiGo", "price_usd": 210, "duration": "3h 15m"},
            {"airline": "Air India", "price_usd": 250, "duration": "3h 40m"},
            {"airline": "Vistara", "price_usd": 275, "duration": "3h 05m"},
        ],
        "note": "MOCK DATA — replace with a real flight API (e.g. Amadeus).",
    }


def search_hotels(city: str, checkin: str, checkout: str, budget: str = "mid-range") -> dict:
    """Search hotels in a city for given dates and budget level (MOCK DATA)."""
    hotels = {
        "budget": [{"name": "City Hostel", "price_per_night_usd": 25}],
        "mid-range": [{"name": "Comfort Inn Central", "price_per_night_usd": 90}],
        "luxury": [{"name": "Grand Palace Hotel", "price_per_night_usd": 300}],
    }
    return {
        "city": city,
        "checkin": checkin,
        "checkout": checkout,
        "budget": budget,
        "options": hotels.get(budget, hotels["mid-range"]),
        "note": "MOCK DATA — replace with a real hotel API (e.g. Booking.com).",
    }


# Registry mapping tool name -> python function.
# agent.py uses this to actually execute a tool the model asked for.
AVAILABLE_TOOLS = {
    "get_weather": get_weather,
    "search_flights": search_flights,
    "search_hotels": search_hotels,
}

"""
main.py
-------
CLI entry point. Run this file to chat with the travel planner agent.
"""

from google.genai import types
from agent import run_agent


def main():
    print("=" * 50)
    print(" Travel Planner Agent  (type 'quit' to exit)")
    print("=" * 50)

    conversation_history: list[types.Content] = []

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        if not user_input:
            continue

        conversation_history = run_agent(user_input, conversation_history)


if __name__ == "__main__":
    main()

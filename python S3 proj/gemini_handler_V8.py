# gemini_handler_V8.py
# This file handles all communication with the Gemini API. (V8)

import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Tuple, Optional

# Load environment variables from a .env file
load_dotenv()

# --- Configuration ---
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
    genai.configure(api_key=api_key)

    # --- System Prompt ---
    system_prompt = (
        "You are a friendly and helpful recipe assistant named 'Chef Tony'. "
        "Your only purpose is to provide recipes, cooking tips, and information related to food and cooking. "
        "Format your recipes clearly with Markdown for bolding and lists. "
        "After providing the full recipe, on a completely new line, "
        "add 'SEARCH_TERM:' followed by a simple, effective search query for a picture of the finished dish. "
        "For example: 'SEARCH_TERM: homemade margherita pizza close up' or 'SEARCH_TERM: classic chicken biryani'. "
        "Do not provide a URL. "
        "Do not answer any questions unrelated to this topic. "
        "If a user asks about something else, politely decline and steer the conversation back to recipes."
    )

    # --- Model Initialization ---
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash',
        system_instruction=system_prompt
    )
except Exception as e:
    print(f"Error during Gemini setup: {e}")
    model = None

def get_gemini_response(user_query: str, chat_history: list) -> Tuple[str, Optional[str]]:
    """
    Gets a recipe and an image search term from the Gemini API.
    """
    if not model:
        return "Error: Gemini model not initialized. Check your API key.", None

    try:
        chat_session = model.start_chat(history=chat_history)
        print("Sending query to Gemini API...")
        response = chat_session.send_message(user_query)
        print("Response received.")

        full_text = response.text
        recipe_text = full_text
        search_term = None

        if "SEARCH_TERM:" in full_text:
            parts = full_text.split("SEARCH_TERM:")
            recipe_text = parts[0].strip()
            search_term = parts[1].strip()

        return recipe_text, search_term

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Oops! 🥺 Something went wrong while talking to the chef. Please try again.", None

if __name__ == '__main__':
    pass

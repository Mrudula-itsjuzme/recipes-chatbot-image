# gemini_handler.py
# This file handles all the communication with the Gemini API.

import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from a .env file
load_dotenv()
def _resolve_api_key() -> Optional[str]:
    """Fetch Gemini API key from environment."""
    return os.getenv("GEMINI_API_KEY")

def get_gemini_response(user_query: str) -> str:
    """
    Gets a recipe-focused response from the Gemini API.

    Args:
        user_query: The user's message.

    Returns:
        The model's response as a string.
    """
    try:
        # --- Configuration ---
        # It's best practice to keep your API key in a .env file
        api_key = _resolve_api_key()
        if not api_key:
            return "Error: GEMINI_API_KEY not found. Please set it in your .env file."

        genai.configure(api_key=api_key)

        # --- System Prompt ---
        # This is the secret sauce! We give the model instructions on how to behave.
        # This makes it a specialized recipe bot.
        system_prompt = (
            "You are a friendly and helpful recipe assistant named 'Chef Tony'. "
            "Your only purpose is to provide recipes, cooking tips, and information related to food and cooking. "
            "Do not answer any questions unrelated to this topic. "
            "If a user asks about something else, politely decline and steer the conversation back to recipes. "
            "Format your recipes clearly with ingredients and step-by-step instructions."
            "give pic of the dish too."
        )

        # --- Model Initialization ---
        # We are using the gemini-1.5-flash model here.
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=system_prompt
        )

        # --- Generate Content ---
        # Send the user's query to the model
        print("Sending query to Gemini API...")
        response = model.generate_content(user_query)
        print("Response received.")

        return response.text

    except Exception as e:
        # Basic error handling
        print(f"An error occurred: {e}")
        return "Oops! 🥺 Something went wrong while talking to the chef. Please try again."

if __name__ == '__main__':
    # This is for testing the handler directly
    print("--- Testing Gemini Handler ---")
    # Test Case 1: A valid recipe query
    test_query_1 = "How do I make chocolate chip cookies?"
    print(f"User: {test_query_1}")
    response_1 = get_gemini_response(test_query_1)
    print(f"Chef Gemini:\n{response_1}")

    print("\n" + "="*20 + "\n")

    # Test Case 2: An off-topic query
    test_query_2 = "What's the weather like today?"
    print(f"User: {test_query_2}")
    response_2 = get_gemini_response(test_query_2)
    print(f"Chef Gemini:\n{response_2}")

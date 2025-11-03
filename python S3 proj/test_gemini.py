# test_gemini.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the .env file to get your API key
load_dotenv()

print("--- Minimal Gemini Test ---")
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file!")
    
    print("API Key loaded successfully.")
    genai.configure(api_key=api_key)
    
    print("Initializing model: gemini-1.5-flash...")
    # This is the simplest way to initialize the model
    model = genai.GenerativeModel('gemini-1.5-flash') 
    
    print("Sending a test prompt to Gemini...")
    response = model.generate_content("Briefly explain what a prime number is.")
    
    print("\nSUCCESS! ✅")
    print("Response received from Gemini:")
    print("-" * 20)
    print(response.text)
    print("-" * 20)

except Exception as e:
    print(f"\nFAILURE! ❌")
    print(f"The test failed with an error: {e}")

print("--- Test Complete ---")
# main_V8.py
# This file connects the UI and the Gemini handler to run the application. (V8 with robust image search)

from chatbot_ui_V8 import ChatApplication
from gemini_handler_V8 import get_gemini_response
import threading
import requests
import time 
from typing import Optional
from ddgs import DDGS

class RecipeBotApp:
    def __init__(self):
        self.app = ChatApplication()
        self.app.set_send_message_callback(self.handle_user_message)
        self.chat_history = []

    def handle_user_message(self, message: str):
        """Handles the user sending a message."""
        self.app.add_message("You", message)
        self.app.show_typing_indicator()

        thread = threading.Thread(target=self._get_bot_response, args=(message,))
        thread.start()

    def _get_bot_response(self, message: str):
        """
        Calls Gemini, then finds a working image by trying multiple search results.
        """
        response_text, search_term = get_gemini_response(message, self.chat_history)
        
        image_data = None
        if search_term:
            print(f"Searching for image with term: '{search_term}'")
            try:
                time.sleep(2) # Prevent rate-limiting

                with DDGS() as ddgs:
                    # Get the top 5 image results to have fallback options
                    search_results = list(ddgs.images(
                        search_term,
                        max_results=5
                    ))
                
                if search_results:
                    # Loop through the results until we find a working link
                    for result in search_results:
                        image_url = result['image']
                        try:
                            print(f"Attempting to download image from: {image_url}")
                            headers = {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                            }
                            image_response = requests.get(image_url, headers=headers, stream=True, timeout=15)
                            image_response.raise_for_status() # Check for errors like 404
                            image_data = image_response.content
                            print("Image downloaded successfully.")
                            break # If successful, stop trying other images
                        except requests.exceptions.RequestException as e:
                            print(f"Download failed for {image_url}: {e}. Trying next image.")
                            continue # Try the next image in the loop
                
                if not image_data:
                    print("All image download attempts failed.")

            except Exception as e:
                print(f"An error occurred during image search: {e}")
                response_text += "\n\n[Chef Tony tried to find an image, but couldn't!]"


        self.app.after(0, self._update_chat_with_response, response_text, image_data)

        self.chat_history.append({"role": "user", "parts": [message]})
        self.chat_history.append({"role": "model", "parts": [response_text]})

    def _update_chat_with_response(self, response: str, image_data: Optional[bytes]):
        """Updates the chat window with the bot's response and image."""
        self.app.hide_typing_indicator()
        self.app.add_message("Chef Tony", response)
        
        if image_data:
            self.app.add_image(image_data) # Fixed typo here (was add__image)

    def run(self):
        """Starts the main loop of the application."""
        self.app.mainloop()

if __name__ == "__main__":
    recipe_app = RecipeBotApp()
    recipe_app.run()

# --- IMPORTANT ---
# You need to install the ddgs library:
# pip install ddgs Pillow requests

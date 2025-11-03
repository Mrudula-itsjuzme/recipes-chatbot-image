# main.py
# This file connects the UI and the Gemini handler to run the application. (V2)

from chatbot_ui import ChatApplication
from gemini_handler import get_gemini_response
import threading

class RecipeBotApp:
    def __init__(self):
        # Initialize the UI
        self.app = ChatApplication()
        # Set the callback function for when a user sends a message
        self.app.set_send_message_callback(self.handle_user_message)

    def handle_user_message(self, message: str):
        """
        This function is called when the user clicks 'Send' or presses Enter.
        It handles getting the response from Gemini in a non-blocking way.
        """
        # 1. Display the user's message immediately in the chat window
        self.app.add_message("You", message)

        # 2. Display the new animated typing indicator
        self.app.show_typing_indicator()

        # 3. Start a new thread to call the Gemini API.
        # This prevents the UI from freezing while waiting for the API response.
        thread = threading.Thread(target=self._get_bot_response, args=(message,))
        thread.start()

    def _get_bot_response(self, message: str):
        """
        Calls the Gemini API and updates the chat.
        This runs in a separate thread.
        """
        # Get the response from our Gemini handler
        response = get_gemini_response(message)

        # The UI needs to be updated from the main thread.
        # `after()` schedules a function to be called safely from the main event loop.
        self.app.after(0, self._update_chat_with_response, response)

    def _update_chat_with_response(self, response: str):
        """Updates the chat window with the bot's final response."""
        # 1. Hide the typing indicator
        self.app.hide_typing_indicator()
        
        # 2. Now, add the actual response from the bot
        self.app.add_message("Chef Tony", response)

    def run(self):
        """Starts the main loop of the application."""
        self.app.mainloop()

if __name__ == "__main__":
    # Create an instance of our app and run it
    recipe_app = RecipeBotApp()
    recipe_app.run()

# --- IMPORTANT ---
# You also need to create a file named .env in the same directory.
# It should contain just one line:
#
# GEMINI_API_KEY="YOUR_API_KEY_HERE"
#
# Replace "YOUR_API_KEY_HERE" with the actual key you got from Google AI Studio.

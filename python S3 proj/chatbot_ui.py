# chatbot_ui.py
# This file creates the user interface for our chatbot. (V2 - Gemini Style)

import tkinter as tk
from tkinter import scrolledtext

# --- Color Palette ---
BG_COLOR = "#131314"
TEXT_COLOR = "#E0E0E0"
INPUT_BG_COLOR = "#1E1F22"
BUTTON_COLOR = "#89B4FA"
BUTTON_TEXT_COLOR = "#131314"
USER_COLOR = "#89B4FA"
BOT_COLOR = "#FDB663"


class ChatApplication(tk.Tk):
    """A simple chat application UI using tkinter."""

    def __init__(self):
        super().__init__()
        self.title("Chef Tony")
        self.geometry("600x750")

        self.on_send_message = None  # Callback function
        self.typing_animation_id = None # To control the animation

        self._setup_ui()

    def _setup_ui(self):
        """Builds the widgets for the chat window."""
        self.configure(bg=BG_COLOR)

        # --- Main Frame ---
        main_frame = tk.Frame(self, bg=BG_COLOR)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # --- Chat History Display ---
        self.chat_history = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            state='disabled',
            font=("Arial", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            padx=15,
            pady=15,
            bd=0,
            relief="flat"
        )
        self.chat_history.grid(row=0, column=0, sticky="nsew")

        # --- Input Frame ---
        input_frame = tk.Frame(main_frame, bg=BG_COLOR)
        input_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        input_frame.grid_columnconfigure(0, weight=1)

        # --- Message Entry Box ---
        self.message_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            bg=INPUT_BG_COLOR,
            fg=TEXT_COLOR,
            bd=0,
            relief="flat",
            insertbackground=TEXT_COLOR # Cursor color
        )
        # Add some internal padding
        self.message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=12, padx=(0, 10))
        self.message_entry.bind("<Return>", self._on_enter_key)

        # --- Send Button ---
        self.send_button = tk.Button(
            input_frame,
            text="➤",
            command=self._send_message_from_ui,
            font=("Arial", 16, "bold"),
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            activebackground="#A3C7FF",
            activeforeground=BUTTON_TEXT_COLOR,
            bd=0,
            relief="flat",
            width=3
        )
        self.send_button.pack(side=tk.RIGHT)

    def _on_enter_key(self, event):
        """Handles when the user presses the Enter key."""
        self._send_message_from_ui()

    def _send_message_from_ui(self):
        """Gets text from the entry box and calls the main send function."""
        message = self.message_entry.get().strip()
        if message and self.on_send_message:
            self.on_send_message(message)
            self.message_entry.delete(0, tk.END)

    def add_message(self, sender: str, message: str):
        """
        Adds a message to the chat history display, preserving whitespace.
        """
        self.chat_history.config(state='normal')
        
        sender_tag = "user_style" if sender == "You" else "bot_style"
        self.chat_history.insert(tk.END, f"{sender}:\n", sender_tag)
        self.chat_history.insert(tk.END, f"{message}\n\n")

        self.chat_history.config(state='disabled')
        self.chat_history.yview(tk.END)

        # --- Tag configurations for styling ---
        self.chat_history.tag_config('user_style', font=('Arial', 13, 'bold'), foreground=USER_COLOR)
        self.chat_history.tag_config('bot_style', font=('Arial', 13, 'bold'), foreground=BOT_COLOR)
        self.chat_history.tag_config('typing_style', font=('Arial', 12, 'italic'), foreground=BOT_COLOR)

    def show_typing_indicator(self):
        """Displays an animated 'is typing...' indicator."""
        self.chat_history.config(state='normal')
        # Add a tag to the indicator so we can find and delete it later
        self.chat_history.insert(tk.END, "Chef Tony is typing", ("bot_style", "typing_indicator"))
        self.chat_history.insert(tk.END, "...", ("typing_style", "typing_indicator"))
        self.chat_history.config(state='disabled')
        self.chat_history.yview(tk.END)
        self._animate_typing(0)

    def _animate_typing(self, counter):
        """Animates the dots of the typing indicator."""
        dots = "." * ((counter % 3) + 1)
        self.chat_history.config(state='normal')
        # Find the start of the dots and replace them
        start_index = self.chat_history.tag_ranges("typing_indicator")[-1]
        self.chat_history.delete(start_index, tk.END)
        self.chat_history.insert(tk.END, dots, ("typing_style", "typing_indicator"))
        self.chat_history.config(state='disabled')
        self.chat_history.yview(tk.END)
        
        # Schedule the next animation frame
        self.typing_animation_id = self.after(400, self._animate_typing, counter + 1)

    def hide_typing_indicator(self):
        """Removes the 'is typing...' indicator."""
        if self.typing_animation_id:
            self.after_cancel(self.typing_animation_id)
            self.typing_animation_id = None
        
        self.chat_history.config(state='normal')
        # Delete all text associated with the 'typing_indicator' tag
        self.chat_history.delete("typing_indicator.first", "typing_indicator.last")
        self.chat_history.config(state='disabled')

    def set_send_message_callback(self, callback):
        """Sets the function to be called when the send button is clicked."""
        self.on_send_message = callback

if __name__ == '__main__':
    # This is for testing the UI directly
    app = ChatApplication()
    def dummy_send(msg):
        app.add_message("You", msg)
        app.show_typing_indicator()
        # Simulate a delay before responding
        app.after(3000, lambda: [app.hide_typing_indicator(), app.add_message("Chef Tony", "This is a test response!\nIt has multiple lines.")])
    app.set_send_message_callback(dummy_send)
    app.mainloop()

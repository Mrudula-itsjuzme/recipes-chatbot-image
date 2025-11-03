# chatbot_ui_V8.py
# This file creates the user interface for our chatbot. (V8)

import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import io

# --- Color Palette ---
BG_COLOR = "#131314"
TEXT_COLOR = "#E0E0E0"
INPUT_BG_COLOR = "#1E1F22"
BUTTON_COLOR = "#89B4FA"
BUTTON_TEXT_COLOR = "#131314"
USER_COLOR = "#89B4FA"
BOT_COLOR = "#FDB663"


class ChatApplication(tk.Tk):
    """A chat application UI, updated to support displaying images."""

    def __init__(self):
        super().__init__()
        self.title("Chef Tony")
        self.geometry("600x750")

        self.on_send_message = None  # Callback function
        self.typing_animation_id = None # To control the animation
        self.image_references = [] # To prevent images from being garbage collected

        self._setup_ui()

    def _setup_ui(self):
        """Builds the widgets for the chat window."""
        self.configure(bg=BG_COLOR)

        main_frame = tk.Frame(self, bg=BG_COLOR)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.chat_history = scrolledtext.ScrolledText(
            main_frame, wrap=tk.WORD, state='disabled', font=("Arial", 12),
            bg=BG_COLOR, fg=TEXT_COLOR, padx=15, pady=15, bd=0, relief="flat"
        )
        self.chat_history.grid(row=0, column=0, sticky="nsew")

        self.chat_history.tag_config('user_style', font=('Arial', 13, 'bold'), foreground=USER_COLOR)
        self.chat_history.tag_config('bot_style', font=('Arial', 13, 'bold'), foreground=BOT_COLOR)
        self.chat_history.tag_config('typing_style', font=('Arial', 12, 'italic'), foreground=BOT_COLOR)

        input_frame = tk.Frame(main_frame, bg=BG_COLOR)
        input_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        input_frame.grid_columnconfigure(0, weight=1)

        self.message_entry = tk.Entry(
            input_frame, font=("Arial", 12), bg=INPUT_BG_COLOR, fg=TEXT_COLOR,
            bd=0, relief="flat", insertbackground=TEXT_COLOR
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=12, padx=(0, 10))
        self.message_entry.bind("<Return>", self._on_enter_key)

        self.send_button = tk.Button(
            input_frame, text="➤", command=self._send_message_from_ui, font=("Arial", 16, "bold"),
            bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, activebackground="#A3C7FF",
            activeforeground=BUTTON_TEXT_COLOR, bd=0, relief="flat", width=3
        )
        self.send_button.pack(side=tk.RIGHT)

    def _on_enter_key(self, event):
        self._send_message_from_ui()

    def _send_message_from_ui(self):
        message = self.message_entry.get().strip()
        if message and self.on_send_message:
            self.on_send_message(message)
            self.message_entry.delete(0, tk.END)

    def add_message(self, sender: str, message: str):
        self.chat_history.config(state='normal')
        sender_tag = "user_style" if sender == "You" else "bot_style"
        self.chat_history.insert(tk.END, f"{sender}:\n", sender_tag)
        self.chat_history.insert(tk.END, f"{message}\n\n")
        self.chat_history.config(state='disabled')
        self.chat_history.yview(tk.END)

    def add_image(self, image_data: bytes):
        """Displays an image in the chat window."""
        try:
            self.chat_history.config(state='normal')
            
            image = Image.open(io.BytesIO(image_data))
            max_width = 450
            if image.width > max_width:
                ratio = max_width / image.width
                new_height = int(image.height * ratio)
                image = image.resize((max_width, new_height), Image.LANCZOS)

            photo = ImageTk.PhotoImage(image)
            self.image_references.append(photo) # Keep a reference!
            
            self.chat_history.image_create(tk.END, image=photo)
            self.chat_history.insert(tk.END, "\n\n")

            self.chat_history.config(state='disabled')
            self.chat_history.yview(tk.END)
        except Exception as e:
            print(f"Error displaying image: {e}")
            self.add_message("System", "[Could not display image]")

    def show_typing_indicator(self):
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, "Chef Tony is typing", ("bot_style", "typing_indicator"))
        self.chat_history.insert(tk.END, "...", ("typing_style", "typing_indicator"))
        self.chat_history.config(state='disabled')
        self.chat_history.yview(tk.END)
        self._animate_typing(0)

    def _animate_typing(self, counter):
        dots = "." * ((counter % 3) + 1)
        self.chat_history.config(state='normal')
        start_index = self.chat_history.search("...", "end-1c", backwards=True)
        if start_index:
            self.chat_history.delete(start_index, f"{start_index}+{len(dots)}c")
            self.chat_history.insert(start_index, dots, ("typing_style", "typing_indicator"))
        self.chat_history.config(state='disabled')
        self.chat_history.yview(tk.END)
        self.typing_animation_id = self.after(400, self._animate_typing, counter + 1)

    def hide_typing_indicator(self):
        if self.typing_animation_id:
            self.after_cancel(self.typing_animation_id)
            self.typing_animation_id = None
        self.chat_history.config(state='normal')
        start = self.chat_history.search("Chef Tony is typing", "1.0", tk.END)
        if start:
             self.chat_history.delete(start, f"{start} + 20 lines")
        self.chat_history.config(state='disabled')


    def set_send_message_callback(self, callback):
        self.on_send_message = callback

if __name__ == '__main__':
    app = ChatApplication()
    app.mainloop()

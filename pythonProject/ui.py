import tkinter as tk
import sys
import os

class AssistantUI:
    def __init__(self, assistant):
        """Initialize the UI with buttons and a display area."""
        self.assistant = assistant  # Reference to the assistant instance

        # Create the main UI window
        self.root = tk.Tk()
        self.root.title("Voice Assistant")
        self.root.geometry("400x300")

        # Create a display area for interactions
        self.display = tk.Text(self.root, height=10, width=50, wrap="word")
        self.display.pack(pady=10)

        # Create stop assistant button (now fully shuts down everything)
        self.stop_button = tk.Button(self.root, text="Stop Assistant", command=self.force_shutdown, bg="red", fg="white")
        self.stop_button.pack(pady=10)

    def update_display(self, message):
        """Update the UI display with a new message."""
        self.display.insert(tk.END, f"{message}\n")
        self.display.see(tk.END)  # Auto-scroll to latest message

    def force_shutdown(self):
        """Shuts down both the UI and the assistant completely."""
        print("Assistant shutting down...")
        self.root.quit()  # Close Tkinter UI properly
        os._exit(0)  # Forcefully terminate Python process

    def start_ui(self):
        """Launch the UI event loop."""
        self.root.mainloop()
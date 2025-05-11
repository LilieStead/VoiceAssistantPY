import sys
import os
import threading
import speech_recognition as sr
import pyttsx3 as tts

# Ensure Python recognizes local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui import AssistantUI
from response_handler import get_best_response  # ML-powered response selection
from system_commands import shutdown_assistant  # Handles assistant shutdown

class Assistant:
    def __init__(self):
        """Initialize the voice assistant, speech recognition, and UI."""
        self.recognizer = sr.Recognizer()
        self.speaker = tts.init()
        self.speaker.setProperty("rate", 150)

        self.ui = AssistantUI(self)  # Pass assistant instance to UI

        # Start assistant in a separate thread
        threading.Thread(target=self.run_assistant).start()
        self.ui.start_ui()

    def shutdown_assistant(self):
        """Safely shuts down the assistant and closes the UI."""
        print("Assistant shutting down...")
        self.speaker.say("Shutting down.")
        self.speaker.runAndWait()
        self.ui.root.destroy()

    def run_assistant(self):
        """Continuously listens for commands, without needing a wake word."""
        with sr.Microphone() as mic:
            self.recognizer.adjust_for_ambient_noise(mic, duration=1)
            print("Voice Assistant is always listening...")

            while True:
                try:
                    audio = self.recognizer.listen(mic)

                    # Debugging: Ensure audio is captured correctly
                    raw_data = audio.get_raw_data()
                    print(f"✔ Raw audio length: {len(raw_data)}")
                    if len(raw_data) == 0:
                        print("Error: No speech detected.")
                        continue

                    text = self.recognizer.recognize_google(audio).lower().strip()
                    print(f"✔ User said: {text}")
                    self.ui.update_display(f"User: {text}")

                    if text in ["stop assistant", "shut down"]:
                        self.ui.root.quit()  # Close Tkinter UI
                        shutdown_assistant()  # Fully terminate script & all processes

                        break  # Stops continuous listening
                    else:
                        response = get_best_response(text)  # ML-powered response selection
                        print(f"Bot response: {response}")
                        if response:
                            self.speaker.say(response)
                            self.speaker.runAndWait()
                            self.ui.update_display(f"Assistant: {response}")

                except sr.UnknownValueError:
                    print("Error: Could not understand audio. Try again.")
                except sr.RequestError:
                    print("Error: Speech Recognition API failed. Check internet.")
                    return
                except Exception as e:
                    print(f"Error: {e}")
                    continue

# Run the assistant
Assistant()
import os
import sys

def shutdown_assistant():
    """Forcefully exits the entire Python runtime."""
    print("Assistant shutting down...")

    # Kill all running Python processes immediately
    os._exit(0)  # Terminates Python without waiting for thread cleanup

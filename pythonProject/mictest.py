import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as mic:
    print("Speak something...")
    recognizer.adjust_for_ambient_noise(mic, duration=0.5)
    audio = recognizer.listen(mic)

    print("Processing speech...")
    text = recognizer.recognize_google(audio)
    print(f"Recognized: {text}")

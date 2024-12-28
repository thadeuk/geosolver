import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
r = sr.Recognizer()

def speak(text):
    """Helper function for text-to-speech."""
    engine.say(text)
    engine.runAndWait()

def listen_for_command():
    """Listen for a voice command. Return the transcribed text."""
    with sr.Microphone() as source:
        print("Listening for command...")
        audio_data = r.listen(source)
        try:
            text = r.recognize_google(audio_data)
            text = text.lower()
            print(f"You said: {text}")
            return (0, text)
        except sr.UnknownValueError:
            print("Sorry, I did not catch that.")
            return (1, "")
        except sr.RequestError:
            print("API was unavailable or unresponsive.")
            return (2, "")
    return (0, "")

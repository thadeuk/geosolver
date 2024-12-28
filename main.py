import os
from dotenv import load_dotenv

import speech_recognition as sr
import pyttsx3
import pyautogui
import requests
import io

# Load the .env file
load_dotenv()

# Retrieve the variables
API_ENDPOINT = os.getenv("API_ENDPOINT")
API_KEY = os.getenv("API_KEY")

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
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not catch that.")
        except sr.RequestError:
            print("API was unavailable or unresponsive.")
    return ""

def take_screenshot():
    """Capture the screenshot and return bytes."""
    screenshot = pyautogui.screenshot()
    img_bytes = io.BytesIO()
    screenshot.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

def call_location_api(imgs):
    """
    Send the screenshot to an endpoint that can identify the location.
    If using GPT-4 with vision: the code would differ since that’s not
    publicly documented. For now, we’ll show a placeholder approach.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/octet-stream",
    }
    response = requests.post(API_ENDPOINT, headers=headers, data=imgs)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.text}")
        return None

def main_loop():
    speak("Go go go go go go.")
    imgs = []
    while True:
        command = listen_for_command()

        if "take photo" in command:
            speak("Taking screenshot now.")
            img_bytes = take_screenshot()
            imgs.append(img_bytes)
            speak(f"Saved screenshot in memory.")

        elif "solve location" in command:
            if not imgs:
                speak("No screenshots to analyze.")
                continue

            speak(f"Sending {len(imgs)} images to ChatGPT.")
            # Send to location identification service
            result = call_location_api(imgs)

            if result:
                location_info = result.get("location", "Location unknown")
                speak(f"This looks like {location_info}.")
                print(f"API response: {result}")
            else:
                speak("Sorry, I could not identify the location.")

            imgs = []
        else:
            speak("I didn't understand that command.")
        
        if "exit" in command or "quit" in command:
            speak("Goodbye!")
            break

if __name__ == "__main__":
    main_loop()


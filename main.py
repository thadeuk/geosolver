import os
from dotenv import load_dotenv

import speech_recognition as sr
import pyttsx3
import pyautogui
import requests
import io
import base64
from openai import OpenAI
import webbrowser
import folium

# Load the .env file
load_dotenv()

engine = pyttsx3.init()
r = sr.Recognizer()

client = OpenAI()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def create_map(lat, lon, zoom=10):
    # Center the map at the given coords
    my_map = folium.Map(location=[lat, lon], zoom_start=zoom)

    # Drop a pin
    folium.Marker(location=[lat, lon], popup="Guessed Location").add_to(my_map)

    filepath = "location_map.html"

    # Save to an HTML file
    my_map.save(filepath)
    print(f"Interactive map saved to {filepath}")
    webbrowser.open_new_tab(filepath)

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
    # Getting the base64 string
    base64_image1 = encode_image("photo1.png")
    base64_image2 = encode_image("photo2.png")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What is in this image?",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_image1}"},
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_image2}"},
                    },
                ],
            }
        ],
    )
    print(response.choices[0])

def main_loop():
    imgs = []
    while True:
        command = listen_for_command()

        if "take photo" in command:
            speak("Taking screenshot now.")
            img_bytes = take_screenshot()
            imgs.append(img_bytes)
            speak(f"Saved screenshot in memory.")
            break

        elif "solve location" in command:
            call_location_api([])
            break
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
        elif "open map" in command:
            speak("Opening the map.")
            # TODO
            create_map(0, 0)
        else:
            speak("I didn't understand that command.")
        
        if "exit" in command or "quit" in command:
            speak("Goodbye!")
            break

if __name__ == "__main__":
    main_loop()


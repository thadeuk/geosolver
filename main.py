# system imports
import os
from dotenv import load_dotenv

# 3rd party imports
import requests
from openai import OpenAI
import webbrowser

# local imports
from voice import speak, listen_for_command
from solution_map import create_map
from image import encode_image, take_screenshot

# Load the .env file
load_dotenv()

client = OpenAI()

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
        (res, command) = listen_for_command()

        if res != 0:
            continue

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
            filepath = "solution_map.html"
            create_map(filepath, 0, 0)
            webbrowser.open_new_tab(filepath)
        else:
            speak("I didn't understand that command.")
        
        if "exit" in command or "quit" in command:
            speak("Goodbye!")
            break

if __name__ == "__main__":
    main_loop()

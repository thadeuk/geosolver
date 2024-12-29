# system imports
import re
import json

# 3rd party imports
import webbrowser

# local imports
from ai import AIClient
from voice import speak, listen_for_command
from solution_map import create_map
from image import take_screenshot, encode_bytes
import vlc

aiClient = AIClient()

def play_sound(file_path):
    player = vlc.MediaPlayer(file_path)
    player.play()

def main_loop():
    imgs = []
    while True:
        (res, command) = listen_for_command()

        if res != 0:
            continue

        if "take photo" in command:
            play_sound("wakeup.mp3")
            img_bytes = take_screenshot()
            imgs.append(encode_bytes(img_bytes))
            play_sound("stop.mp3")
            speak(f"Saved photo...")

        elif "location" in command:
            if not imgs:
                speak("No screenshots to analyze.")
                continue

            play_sound("wakeup.mp3")
            # Send to location identification service
            result = aiClient.call_location_api(imgs)
            print(result)
            if result:
                location_str, lat, lon = parse_location_data(extract_json_from_markdown(result))
                if location_str:
                    speak(f"Most probable location is {location_str}.")
                if lat and lon:
                    speak("Opening the map.")
                    filepath = "solution_map.html"
                    create_map(filepath, lat, lon)
                    webbrowser.open_new_tab(filepath)

            else:
                speak("No location found in the image.")
            imgs = []
        
        if "exit" in command or "quit" in command:
            speak("Goodbye!")
            break

def extract_json_from_markdown(markdown_str):
    """
    Extracts JSON string from a Markdown code block.

    Args:
        markdown_str (str): String containing Markdown code block with JSON.

    Returns:
        str: Cleaned JSON string without Markdown delimiters.
    """
    # Use regex to extract content between ```json and ```
    json_pattern = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL | re.IGNORECASE)
    match = json_pattern.search(markdown_str)
    if match:
        return match.group(1)
    else:
        # If no code block found, assume the entire string is JSON
        return markdown_str.strip()

def parse_location_data(json_str):
    """
    Parses the JSON string to extract location and coordinates.

    Args:
        json_str (str): JSON-formatted string containing location data.

    Returns:
        tuple: (location (str), latitude (float), longitude (float))
    """
    try:
        # Parse the JSON string into a Python dictionary
        data = json.loads(json_str)

        # Extract the location
        location = data.get('location')

        # Extract coordinates
        coordinates = data.get('coordinates', {})
        latitude = coordinates.get('lat')
        longitude = coordinates.get('lon')

        return location, latitude, longitude
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None, None, None

if __name__ == "__main__":
    main_loop()

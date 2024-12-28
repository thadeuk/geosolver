import pyautogui
import base64
import io

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def encode_bytes(image_bytes):
    return base64.b64encode(image_bytes.getvalue()).decode("utf-8")

def take_screenshot():
    """Capture the screenshot and return bytes."""
    screenshot = pyautogui.screenshot()
    img_bytes = io.BytesIO()
    screenshot.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

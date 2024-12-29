import pyautogui
import base64
import io
from PIL import Image

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def reduce_image_size(
    input_path, 
    output_path=None, 
    quality=50
):
    if output_path is None:
        output_path = input_path  # Overwrite the original file if no output path is provided

    with Image.open(input_path) as img:
        # Convert to RGB because JPEG doesn't support alpha channels
        img = img.convert("RGB")
        
        # Save with reduced quality and optional optimization
        img.save(
            output_path, 
            format="JPEG", 
            quality=quality, 
            optimize=True
        )
    print(f"Saved reduced-quality image to: {output_path}")

def encode_bytes(image_bytes):
    return base64.b64encode(image_bytes.getvalue()).decode("utf-8")

def take_screenshot(quality=30):
    screenshot = pyautogui.screenshot()
    
    # Convert screenshot to RGB (in case it's RGBA)
    screenshot = screenshot.convert("RGB")
    
    # Save to an in-memory bytes buffer as JPEG
    img_bytes = io.BytesIO()
    screenshot.save(img_bytes, format='JPEG', quality=quality, optimize=True)
    
    # Reset buffer position
    img_bytes.seek(0)
    return img_bytes

if __name__ == "__main__":
    # 1. Take a screenshot with reduced quality (smaller file size)
    low_quality_bytes_30 = take_screenshot(quality=30)
    low_quality_base64_30 = encode_bytes(low_quality_bytes_30)

    low_quality_bytes_50 = take_screenshot(quality=50)
    low_quality_base64_50 = encode_bytes(low_quality_bytes_50)

    print("Base64 with quality=30 len:", len(low_quality_base64_30))
    print("Base64 with quality=50 len:", len(low_quality_base64_50))
    print("Ratio:", len(low_quality_base64_30) / len(low_quality_base64_50))

    # 3. Alternatively, if you have an existing image you want to shrink:
    #    reduce_image_size("original.png", "reduced.jpg", quality=30)
    #    print(encode_image("reduced.jpg"))


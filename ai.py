from openai import OpenAI

from image import encode_image, encode_bytes

from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def call_location_api(imgs):
    img_objs = []
    for img in imgs:
        img_objs.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img}"}})

    content = []
    content.append({"type": "text", "text": "I'm sending you pictures about a location, please respond first with the most probably locations and then give the explanation. Also, include the coordinate points"})
    content.extend(img_objs)

    print("Sending to ChatGPT...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": content
            }
        ],
    )
    return response.choices[0]

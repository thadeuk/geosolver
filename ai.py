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
    content.append({"type": "text", "text": "I'm sending you pictures of a location. Tell me where this location is with a JSON object, with the fields 'location' - succinct answer with country and city or region, and 'coordinates', with subfields 'lat' and 'lon' that are just numbers."})
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
    if response.choices[0]:
        return response.choices[0].message.content
    return None

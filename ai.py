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
    content.append({"type": "text", "text": "I'm sending you photos of a location. I need you to identify where this location is. You can use language that may be in the photo, people, style of cars, vegetation, bollards, roads, direction of travel, signs, really anything you can find in the image. I also need the coordinates of where this photo was taken, as accurately as possible. Answer with a JSON object, with the fields 'location' - succinct answer with country and city or region, and 'coordinates', with subfields 'lat' and 'lon' that are just numbers."})
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

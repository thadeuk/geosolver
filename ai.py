from openai import OpenAI

from image import encode_image, encode_bytes

client = OpenAI()

def call_location_api(imgs):
    img_objs = []
    for img in imgs:
        img_objs.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encode_bytes(img)}"}})

    content = []
    content.append({"type": "text", "text": "What is in this image?"})
    content.extend(img_objs)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": content
            }
        ],
    )
    print(response.choices[0])

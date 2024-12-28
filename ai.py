from openai import OpenAI

from image import encode_image

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

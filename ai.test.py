from ai import AIClient
from image import encode_image

imgs = [
    encode_image("photo1.png"),
    encode_image("photo2.png"),
]

ai = AIClient()
result = ai.call_location_api(imgs)
print(result)

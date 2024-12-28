from ai import call_location_api
from image import encode_image

imgs = [
    encode_image("photo1.png"),
    encode_image("photo2.png"),
]

result = call_location_api(imgs)
print(result)

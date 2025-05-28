import openai
import os
import requests


openai.api_key = "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"

try:
    #
    prompt = "A cute cat sitting on a cozy couch in a sunny room"

    # 
    response = openai.images.generate(
    model="dall-e-2",
    prompt="A cute cat sitting on a cozy couch in a sunny room",
    size="512x512",
    n=1
)

    # 
    image_url = response.data[0].url
    print(f"Ảnh tạo thành công: {image_url}")

    # 
    os.makedirs("generated", exist_ok=True)
    img_data = requests.get(image_url).content
    with open("generated/test_image.png", "wb") as f:
        f.write(img_data)
    print("📁 Đã lưu ảnh vào: generated/test_image.png")

except Exception as e:
    print(f"Lỗi: {e}")
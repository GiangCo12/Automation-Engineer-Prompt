import os
from openai import OpenAI
from dotenv import load_dotenv
import requests
import pandas as pd
from datetime import datetime

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Prompt và tên file
reference_data = [
    {
        "filename": "coding_interrupted.png",
        "prompt": "a digital painting of a student coding late at night, surprised as the teacher appears behind him holding a grade sheet",
    },
    {
        "filename": "ice_cream_rain.png",
        "prompt": "a cartoon boy eating ice cream under a sunny sky, suddenly it starts raining heavily, dramatic and funny scene",
    },
    {
        "filename": "date_in_the_rain.png",
        "prompt": "an anime-style couple on a scooter in the city, caught in a sudden rainstorm, both wearing casual clothes, laughing and soaked",
    }
]

os.makedirs("generated", exist_ok=True)
os.makedirs("logs", exist_ok=True)

log = []

# Gọi API 
for item in reference_data:
    prompt = item["prompt"]
    filename = item["filename"]
    try:
        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            n=1,
            size="512x512",
            response_format="url"
        )
        image_url = response.data[0].url
        img_data = requests.get(image_url).content
        path = os.path.join("generated", filename)
        with open(path, "wb") as f:
            f.write(img_data)

        print(f"Đã tạo ảnh: {filename}")
        log.append({
            "timestamp": datetime.now(),
            "reference_image": filename,
            "prompt": prompt,
            "output_file": path,
            "status": "Success"
        })
    except Exception as e:
        print(f"Lỗi với prompt: {prompt}")
        print("Lỗi:", e)
        log.append({
            "timestamp": datetime.now(),
            "reference_image": filename,
            "prompt": prompt,
            "output_file": "",
            "status": f"Fail: {e}"
        })

# Ghi log
df_log = pd.DataFrame(log)
df_log.to_csv("logs/prompt_engineering_log.csv", index=False)
print("📄 Đã ghi log vào logs/prompt_engineering_log.csv")
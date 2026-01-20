import os
import requests
import base64
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("STABILITY_API_KEY")

API_HOST = "https://api.stability.ai"

def generate_ai_image(prompt, style_preset="photographic"):
    if not API_KEY:
        raise Exception("API Key not found. Check your .env file!")

    url = f"{API_HOST}/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    body = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 7,
        "height": 1024,
        "width": 1024,
        "samples": 1,
        "steps": 30,
        "style_preset": style_preset
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200:
        raise Exception(f"AI Server Error: {response.text}")

    data = response.json()
    for i, image in enumerate(data["artifacts"]):
        img_data = base64.b64decode(image["base64"])
        return Image.open(BytesIO(img_data))
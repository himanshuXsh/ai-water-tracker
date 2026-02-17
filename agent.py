import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

# ✅ Correct working router endpoint
API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.1"


headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

def analyze_intake(total: int, goal: int):

    if not HF_API_KEY:
        return "HF_API_KEY not found. Check your .env file."

    prompt = (
        f"The user has consumed {total} ml of water today. "
        f"The daily goal is {goal} ml. "
        "Give short motivational hydration advice in 2 lines."
    )

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code != 200:
            return f"AI error {response.status_code}: {response.text}"

        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]

        return f"Unexpected AI response: {result}"

    except Exception as e:
        return f"Exception occurred: {str(e)}"

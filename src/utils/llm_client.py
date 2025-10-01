import os
import requests

HF_API_KEY = os.getenv("HF_API_KEY")
DEEPSEEK_MODEL = "deepseek-ai/DeepSeek-V3"
API_URL = f"https://api-inference.huggingface.co/models/{DEEPSEEK_MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

def query_deepseek(prompt: str, max_new_tokens: int = 200) -> str:
    if not prompt:
        return "No prompt provided."

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"].strip()
        elif isinstance(data, dict) and "generated_text" in data:
            return data["generated_text"].strip()
        elif isinstance(data, str):
            return data.strip()
        else:
            return "Unexpected response format."
    except requests.exceptions.Timeout:
        return "Request timed out."
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

import os
import requests


HF_API_KEY = os.getenv("HF_API_KEY")

DEFAULT_MODEL = "deepseek-ai/DeepSeek-V3"

API_URL = f"https://api-inference.huggingface.co/models/{DEFAULT_MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

def query_hf(prompt: str, model: str = DEFAULT_MODEL, max_new_tokens: int = 200) -> str:
    url = f"https://api-inference.huggingface.co/models/{model}"
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": max_new_tokens}
    }
    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code == 200:
        data = response.json()
        # HF returns a list of dicts with "generated_text"
        return data[0]["generated_text"]
    elif response.status_code == 503:
        return "Model is loading or unavailable. Try again in a minute."
    elif response.status_code == 429:
        return "Daily quota reached. Please try again tomorrow."
    else:
        return f"Error {response.status_code}: {response.text}"
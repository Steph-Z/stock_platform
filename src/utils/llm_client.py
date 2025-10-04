import os
import requests
from huggingface_hub import InferenceClient


def run_deepseek(prompt: str, max_tokens: int = 500):
    """
    Query DeepSeek-V3.2-Exp via Hugging Face Inference API
    Returns model output
    """
    if prompt is None:
        return "No valid prompt detected, try changing the timeframe to a maximum of three months."
    if not isinstance(prompt, str):
        raise TypeError(f"Prompt must be a string")
    if prompt.strip() == "":
        raise ValueError("Prompt is empty")

    api_key = os.environ.get("HF_API_KEY")

    try: #use exception i case provider has issues/problems
        
        client = InferenceClient(
            provider="novita", #relatively cheap provider
            api_key=api_key,
        )
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3.2-Exp",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        response_text = completion.choices[0].message["content"]

        
        return response_text

    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Problems calling the provider")
    except Exception as e:
        raise RuntimeError(f"UProblems getting an output from the provider")
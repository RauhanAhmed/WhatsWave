import pandas as pd
import requests
import litellm
import os

os.environ["GROQ_API_KEY"]="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"

prompt = """
You are an expert at crafting engaging, well-balanced WhatsApp messages. 
Based on the provided base message or use case, rewrite the message to be engaging and appropriate, ensuring any `{name}` placeholder is included where applicable. 
If no base message is provided, create a new message based on the use case, including `{name}` if required. 
Ensure the message is accurate and truthful, with no false information, hopes, or commitments.

Details provided:
BASE MESSAGE: {base_message}
USE CASE: {use_case}

Return only the WhatsApp message in plain text—no extra text, quotes, or explanations.
"""

def get_model_name():
    api_key = os.environ.get("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    models = pd.DataFrame(dict(response.json())["data"]).sort_values(by = ["created"], ascending = False)
    return "groq/" + models.iloc[0, :]["id"]

def rewrite_message(base_message: str, use_case: str):
    formatted_prompt = prompt.format(name = "{name}", base_message = base_message, use_case = use_case)
    response = litellm.completion(
        model=get_model_name(), 
        messages=[
        {"role": "user", "content": formatted_prompt}
    ],
    )
    return response.choices[0].message.content
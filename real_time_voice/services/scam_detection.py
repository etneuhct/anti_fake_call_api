import json
from pathlib import Path

from openai import OpenAI

from django.conf import settings 


# Get the parent directory as a Path object
base_dir = Path(__file__).resolve().parent
prompt_file = base_dir / 'prompt-scam-detection.txt'

with open(prompt_file, 'r') as f:
    prompt_template = f.read()


client = None

def run_detection(text: str):
    global prompt_template
    global client
    client = OpenAI(settings.OPENAI_API_KEY) if client is None else client
    prompt = prompt_template.replace('{TEXT}', text)
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    content = None
    if len(chat_completion.choices):
        content = chat_completion.choices[0].message.content
    return json.loads(content) if content is not None else {"is_scammy": False, "scam_score": 0, "explanation": "We could not figure out whether this content was scammy."}

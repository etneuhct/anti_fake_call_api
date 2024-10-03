import json
from pathlib import Path

from real_time_voice.services.openai import OpenAIClientProvider


# Get the parent directory as a Path object
base_dir = Path(__file__).resolve().parent
prompt_file = base_dir / 'prompt-scam-detection.txt'

with open(prompt_file, 'r') as f:
    prompt_template = f.read()


def run_detection(text: str):
    global prompt_template
    client = OpenAIClientProvider.get_openai_client()
    prompt = prompt_template.replace('{TEXT}', text)
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    content = None
    if len(chat_completion.choices):
        content = chat_completion.choices[0].message.content
    return json.loads(content) if content is not None else {"is_scammy": False, "scam_score": 0, "explanation": "We could not figure out whether this content was scammy."}

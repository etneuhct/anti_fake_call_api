from openai import OpenAI

from utils.exceptions import BadRequestException


class ConversationAnalyzerService:

    def __init__(self, data, dry_run):
        self.conversation_data = data
        self.dry_run = dry_run

    def run(self):
        if self.dry_run:
            return {"response": {}}
        else:
            return self.get_from_gpt()

    def get_from_gpt(self):
        client = OpenAI()
        prompt = self.conversation_data.pop("prompt")
        if len(prompt) == 0:
            prompt = self.get_default_prompt()
        if len(self.conversation_data["messages"]) == 0:
            raise BadRequestException("missing messages")

        self.conversation_data["messages"] = [
            *prompt, *self.conversation_data["messages"]
        ]

        completion = client.chat.completions.create(
            **self.conversation_data
        )
        print(completion)
        message = completion.choices[0].message.content
        print(message)
        return {
            "response": completion.model_dump_json()
        }

    @staticmethod
    def get_default_prompt():
        return []

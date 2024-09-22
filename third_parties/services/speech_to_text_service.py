import io

from openai import OpenAI


class SpeechToTextService:

    def __init__(self, data, dry_run):
        self.speech_to_text_data = data
        self.dry_run = dry_run

    def run(self):
        if self.dry_run:
            return {"response": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."}
        else:
            return self.get_from_whisper()

    def get_from_whisper(self):
        client = OpenAI()
        self.speech_to_text_data["file"] = self.convert_memory_to_io(
            self.speech_to_text_data["file"]
        )
        transcription = client.audio.transcriptions.create(
            **self.speech_to_text_data
        )
        return {
            "response": transcription.model_dump_json()
        }

    @staticmethod
    def convert_memory_to_io(memory_file):
        io_file = io.BytesIO(memory_file.read())
        io_file.seek(0)
        return io_file

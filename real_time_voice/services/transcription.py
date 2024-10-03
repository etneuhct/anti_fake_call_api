from pathlib import Path
import whisper

from real_time_voice.services.openai import OpenAIClientProvider

model = whisper.load_model("base")

def transcribe(wav_audio_file):
    audio = whisper.load_audio(wav_audio_file)
    audio = whisper.pad_or_trim(audio)
    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    return result

def transcribe_with_api(wav_audio_file):
    client = OpenAIClientProvider.get_openai_client()
    return client.audio.transcriptions.create(
        model="whisper-1",
        file=wav_audio_file
    )


if __name__ == '__main__':
    from services.audio import MulawConverter

    # Get the parent directory as a Path object
    base_dir = Path(__file__).resolve().parent

    mulaw_audio_file = base_dir / 'audio_conversation'
    wav_audio_file = mulaw_audio_file.with_suffix('.wav')
    print(wav_audio_file)

    converter = MulawConverter(wav_audio_file)
    converter.process_from_file(mulaw_audio_file)

    result = transcribe(wav_audio_file)
    print(f'Conversation transcription: {result.text}')

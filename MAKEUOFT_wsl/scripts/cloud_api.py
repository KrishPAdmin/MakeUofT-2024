import os
from google.cloud import texttospeech
from google.cloud import speech
from typing import Optional
import argparse

# Grant permission for Cloud API
os.environ["GOOGLE_CLOUD_API"]="YourServiceAccount.json"

SPEECH_FILE = 'speech.wav'


def text_to_speech(text_input: str) -> str:

    client_tts = texttospeech.TextToSpeechClient()

    synthesis_in = texttospeech.SynthesisInput(text=text_input[7:])
    # Let's make this a premium Wavenet voice in SSML
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-A",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )
    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )
    # Perform the text-to-speech request on the text input with theselected
    # voice parameters and audio file type
    response = client_tts.synthesize_speech(
    input=synthesis_in, voice=voice, audio_config=audio_config
    )
    print('tts is working')
    # The response's audio_content is binary.
    with open(SPEECH_FILE, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
    return text_input


def speech_to_text() -> Optional[str]:
    """Streams transcription of the given audio file."""
    client = speech.SpeechClient()

    with open(SPEECH_FILE, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=8000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        if result is not None:
            # The first alternative is the most likely one for this portion.
            response = str(result.alternatives[0].transcript)
            print(f"User: {response}")
            
    if not isinstance(response, str):
        return ' '
    else:
        return response

            

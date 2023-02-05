import io
import os

# Imports the Google Cloud client library
from google.cloud import speech

def SpeechToText(audio):
    # Instantiates a client
    client = speech.SpeechClient.from_service_account_file('key.json')

    # The name of the audio file to transcribe
    file_name = 'files/'+audio

    with open(file_name, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    diarization_config = speech.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=2,
        max_speaker_count=10,
    )

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        language_code="en-US",
        diarization_config=diarization_config,
    )

    print("Waiting for operation to complete...")
    response = client.recognize(config=config,  audio=audio)
    text="" 
    for i in response.results:
        for j in i.alternatives:
            text+= j.transcript

    with open('classify.txt','w') as f:
        f.write(text)
        f.close()

    # The transcript within each result is separate and sequential per result.
    # However, the words list within an alternative includes all the words
    # from all the results thus far. Thus, to get all the words with speaker
    # tags, you only have to take the words list from the last result:
    result = response.results[-1]

    words_info = result.alternatives[0].words

    current_speaker = None
    with open("output.txt", "w") as file:
        for word_info in words_info:
            if current_speaker != word_info.speaker_tag:
                current_speaker = word_info.speaker_tag
                line = "Speaker{} : ".format(current_speaker)
            else:
                line = " " * len("Speaker{} : ".format(current_speaker))
            line += "{} ({} - {})\n".format(word_info.word, word_info.start_time.seconds, word_info.end_time.seconds)
            file.write(line)
import argparse
import io
import json
import os

from google.cloud import language_v1
import numpy
import six

def classify(text, verbose=True):
    """Classify the input text into categories."""

    language_client = language_v1.LanguageServiceClient.from_service_account_file('key.json')

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = language_client.classify_text(request={"document": document})
    categories = response.categories

    result = {}
    topics=""

    for category in categories:
        # Turn the categories into a dictionary of the form:
        # {category.name: category.confidence}, so that they can
        # be treated as a sparse vector.
        result[category.name] = category.confidence

    if verbose:
        for category in categories:
            topics+=category.name+" \n"
            topics+=str(category.confidence)
            topics+='\n'

    # Saves the transcribed and speaker diarized text to a .txt file in the same directory
    file = open("Topic.txt", "w")
    file.write(topics)
    file.close()

    print(topics)

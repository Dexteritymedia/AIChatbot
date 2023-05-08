import os
import urllib.request
import re
from time import time, sleep

from django.conf import settings

import openai

openai.api_key = settings.OPENAI_API_KEY


def generate_ai_response(tone, language, message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Generate 5-6 detailed blog outlines on this\nTitle: {}".format(title),
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)

    return response['choices'][0]['text'].replace('\n','<br/>')

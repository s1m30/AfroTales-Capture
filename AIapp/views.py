from django.shortcuts import render
import os
from openai import AzureOpenAI
from PIL import Image
import requests
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from array import array
import os
import sys
import time

#Azure Ai will be used here
# Set up OpenAI API
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

# Function to recognize text from image
#Azure Read will be used here
def recognize_text_from_image(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    text = pytesseract.image_to_string(img)
    return text
# Function to fetch bot reply
def fetch_bot_reply(outline):
    response = client.Completion.create(
        engine="text-davinci-003",  # Adjust the engine according to your needs
        prompt=f"""
            Generate an enthusiastic response to the given outline.
            ###
            outline: {outline}
            response: This sounds fascinating! I'm eager to illustrate this unique perspective!
            ###
        """,
        max_tokens=60
    )
    return response.choices[0].text.strip()

# Function to fetch synopsis
def fetch_synopsis(outline):
    response = client.Completion.create(
        engine="text-davinci-003",  # Adjust the engine according to your needs
        prompt=f"""
            Generate an engaging, professional, and educative analysis based on an African literature excerpt.
            ###
            outline: {outline}
            synopsis: 
            ###
        """,
        max_tokens=700
    )
    synopsis = response.choices[0].text.strip()
    return synopsis



# Function to fetch image prompt
def fetch_image_prompt(synopsis):
    response = client.Completion.create(
        engine="text-davinci-003",  # Adjust the engine according to your needs
        prompt=f"""
            Give a short description of an image which illustrates events, characters or objects from African literature excerpts.
            ###
            excerpt: {synopsis}
            synopsis: {synopsis}
            character: A fine looking man
            image description: A handsome African black man with beautiful white teeth, he wears kohl around his eyes and runs as fast as a panther.
            ###
        """,
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Function to fetch image URL
def fetch_image_url(image_prompt):
    response = client.Image.create(
        prompt=f"{image_prompt}. There should be no text in this image.",
        n=1,
        size="256x256",
        response_format="json"
    )
    image_url = response.data[0].url
    return image_url

# Example usage:
outline = "At the gates, Biafran soldiers were waving cars through..."
bot_reply = fetch_bot_reply(outline)
print("Bot Reply:", bot_reply)

synopsis = "The Biafran Armed Forces (BAF) were the military..."
print("Synopsis:", fetch_synopsis(synopsis))

image_url = "URL_TO_YOUR_IMAGE"
text = recognize_text_from_image(image_url)
print("Text from Image:", text)

image_prompt = "But there was no such doubt anywhere about his skin..."
print("Image Prompt:", fetch_image_prompt(image_prompt))

image_url = fetch_image_url(image_prompt)
print("Image URL:", image_url)

# Create your views here.

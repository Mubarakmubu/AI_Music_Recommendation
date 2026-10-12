import requests
import os
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv("JAMENDO_CLIENT_ID")

# Read detected emotion
with open("emotion/current_emotion.txt", "r") as f:
    emotion = f.read().strip().capitalize()

print("Detected emotion:", emotion)

# Convert emotion to music search
emotion_music = {
    "Happy": "happy",
    "Sad": "sad",
    "Angry": "rock",
    "Fear": "calm",
    "Neutral": "chill",
    "Surprise":  "pop",
    "Disgust": "alternative"
}

search_term = emotion_music.get(
    emotion,
    "chill"
)

print("Searching Jamendo for:", search_term)

url = "https://api.jamendo.com/v3.0/tracks/"

params = {
    "client_id": CLIENT_ID,
    "format": "json",
    "search": search_term,
    "limit": 5
}

response = requests.get(url, params=params)

print("Status:", response.status_code)

data = response.json()

print("Songs found:", len(data.get("results", [])))

for track in data.get("results", []):

    print("--------------------------------")
    print("Song:", track.get("name"))
    print("Artist:", track.get("artist_name"))
    print("Audio:", track.get("audio"))
    print("Track page:", track.get("shareurl"))
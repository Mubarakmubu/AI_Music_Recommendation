import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
import requests
import subprocess
import sys
import random

app = Flask(__name__)

# ==========================================
# JAMENDO CLIENT ID
# ==========================================

load_dotenv()
CLIENT_ID = os.getenv("JAMENDO_CLIENT_ID")


# ==========================================
# READ DETECTED EMOTION
# ==========================================

def get_emotion():

    try:

        with open("emotion/current_emotion.txt", "r") as f:

            emotion = f.read().strip().capitalize()

            if emotion:
                return emotion

    except FileNotFoundError:

        print("Emotion file not found.")

    return "Neutral"


# ==========================================
# EMOTION → MUSIC SEARCH (multiple options per emotion)
# ==========================================

emotion_music = {

    "Happy": ["happy", "pop", "acoustic", "funk"],

    "Sad": ["sad", "acoustic", "piano", "blues"],

    "Angry": ["rock", "metal", "punk", "hardrock"],

    "Fear": ["ambient", "calm", "instrumental", "soundtrack"],

    "Neutral": ["chill", "lofi", "jazz", "indie"],

    "Surprise": ["pop", "energetic", "rock", "funk"],

    "Disgust": ["alternative", "grunge", "experimental", "punk"]
}


# ==========================================
# GET SONGS FROM JAMENDO
# ==========================================

def get_songs(emotion):

    # Pick a random search term from the emotion's options
    options = emotion_music.get(emotion, ["chill"])
    search_term = random.choice(options)

    print("Detected emotion:", emotion)
    print("Searching Jamendo for:", search_term)

    # Jamendo API
    url = "https://api.jamendo.com/v3.0/tracks/"

    # API parameters
    params = {

        "client_id": CLIENT_ID,

        "format": "json",

        "search": search_term,

        "limit": 5
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        print(
            "Jamendo status:",
            response.status_code
        )

        data = response.json()

        songs = data.get(
            "results",
            []
        )

        print(
            "Songs found:",
            len(songs)
        )

        return songs

    except Exception as e:

        print(
            "Jamendo error:",
            e
        )

        return []


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    # Read current emotion
    emotion = get_emotion()

    # Get recommended songs
    songs = get_songs(
        emotion
    )

    # Send data to HTML
    return render_template(

        "index.html",

        emotion=emotion,

        songs=songs
    )


# ==========================================
# START EMOTION DETECTION (blocking + returns JSON)
# ==========================================

@app.route(
    "/detect",
    methods=["POST"]
)
def detect():

    print(
        "Starting emotion detection..."
    )

    try:

        # subprocess.run() WAITS for the script to finish
        # (camera opens, detects for 5s, closes, writes file)
        subprocess.run(
            [sys.executable, "emotion/emotion_detector.py"],
            timeout=30
        )

    except subprocess.TimeoutExpired:

        print("Emotion detector timed out.")

    except Exception as e:

        print(
            "Error starting emotion detector:",
            e
        )

    # Read the freshly-updated emotion
    emotion = get_emotion()

    # Get songs for that emotion
    songs = get_songs(emotion)

    # Return JSON so the page updates without reloading
    return jsonify({
        "emotion": emotion,
        "songs": songs
    })


# ==========================================
# RUN FLASK
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
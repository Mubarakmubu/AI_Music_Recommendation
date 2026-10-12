# 🎵 AI Music Recommendation

A web app that detects your facial emotion through the webcam and recommends music that matches your mood.

The app reads your expression with a trained deep learning model, maps the detected emotion to a music genre or tag, and fetches matching royalty-free tracks from the [Jamendo API](https://developer.jamendo.com/). You can play the songs directly in the browser.

## Features

- Real-time facial emotion detection using OpenCV and a trained Keras model
- Recognizes 7 emotions: Happy, Sad, Angry, Fear, Neutral, Surprise, Disgust
- Maps each emotion to music tags (for example Sad → acoustic, piano; Angry → rock, metal)
- Fetches songs from Jamendo with album art, artist name and a built-in audio player
- Simple Flask web interface with a **Start Emotion Detection / Detect Again** button
- API key kept out of the code using a `.env` file

## Tech Stack

- **Language:** Python 3.10
- **Backend:** Flask
- **Computer Vision / ML:** OpenCV, TensorFlow / Keras
- **API:** Jamendo API (via `requests`)
- **Frontend:** HTML, CSS, JavaScript

## Project Structure

```
AI_Music_Recommendation/
├── app.py                  # Flask app: reads emotion, searches Jamendo, serves the page
├── emotion/
│   ├── emotion_detector.py # Webcam emotion detection, writes result to current_emotion.txt
│   ├── current_emotion.txt # Latest detected emotion
│   └── finalfacialemotionmodel.keras  # Trained emotion model
├── templates/
│   └── index.html          # Web page
├── static/
│   └── style.css           # Styling
├── camera_test.py          # Checks that the webcam works
├── face_detection.py       # Face detection test
├── test_jamendo.py         # Tests the Jamendo API on its own
└── .gitignore
```

## How It Works

1. Click **Start Emotion Detection** on the web page.
2. The emotion detector opens your webcam, finds your face and predicts your emotion with the trained model.
3. The result is saved to `emotion/current_emotion.txt`.
4. `app.py` reads the emotion, picks a matching music tag, and searches Jamendo for tracks.
5. The page shows your detected emotion and a list of recommended songs you can play.

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mubarakmubu/AI_Music_Recommendation.git
   cd AI_Music_Recommendation
   ```

2. **Install the dependencies**
   ```bash
   pip install flask requests python-dotenv opencv-python tensorflow
   ```
   Add any other packages your `emotion_detector.py` imports (for example `numpy`).

3. **Get a Jamendo client ID**
   Register for free at [developer.jamendo.com](https://developer.jamendo.com/) and create an app to get a client ID.

4. **Create a `.env` file** in the project folder:
   ```
   JAMENDO_CLIENT_ID=your_client_id_here
   ```
   The `.env` file is listed in `.gitignore`, so your key is never uploaded.

## Usage

```bash
python app.py
```

Then open **http://127.0.0.1:5000** in your browser, allow camera access, and click **Start Emotion Detection**.

To test the music search without the camera, put an emotion (for example `Happy`) in `emotion/current_emotion.txt` and run:

```bash
python test_jamendo.py
```

## Notes

- Fear and Disgust are harder for the model to detect and may be read as Neutral or Sad.
- Jamendo search works best with single-word tags such as `happy`, `rock`, `calm` or `chill`. Two-word phrases often return no results.

## Author

**Mubarak S. Kather Mohideen**
B.Tech Computer Science Engineering (AI & ML)

## License

This project is for learning and portfolio purposes. Music is provided by Jamendo under its respective Creative Commons licenses.

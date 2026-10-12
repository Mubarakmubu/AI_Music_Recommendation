import cv2
import tensorflow as tf
import numpy as np
import time

# ==========================================
# LOAD EMOTION MODEL
# ==========================================

model = tf.keras.models.load_model(
    "emotion/finalfacialemotionmodel.keras"
)


# ==========================================
# EMOTION LABELS
# ==========================================

emotion_labels = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Neutral",
    "Sad",
    "Surprise"
]


# ==========================================
# LOAD FACE DETECTOR
# ==========================================

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


# ==========================================
# START CAMERA
# ==========================================

camera = cv2.VideoCapture(0)

if not camera.isOpened():

    print("❌ Camera could not be opened")

    exit()


print("✅ Emotion detection started")
print("Look at the camera...")


# ==========================================
# CAMERA TIMER
# ==========================================

start_time = time.time()

# Camera will run for 5 seconds
detection_time = 5


detected_emotion = None


# ==========================================
# CAMERA LOOP
# ==========================================

while True:

    success, frame = camera.read()

    if not success:

        print("❌ Could not read camera")

        break


    # Convert to grayscale

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )


    # Detect faces

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50)
    )


    # ======================================
    # PROCESS FACE
    # ======================================

    for (x, y, w, h) in faces:

        # Crop face

        face = gray[
            y:y+h,
            x:x+w
        ]


        # Resize

        face = cv2.resize(
            face,
            (48, 48)
        )


        # Normalize

        face = face.astype(
            "float32"
        ) / 255.0


        # Reshape

        face = np.expand_dims(
            face,
            axis=0
        )

        face = np.expand_dims(
            face,
            axis=-1
        )


        # Predict emotion

        predictions = model.predict(
            face,
            verbose=0
        )


        # Get highest probability

        emotion_index = np.argmax(
            predictions[0]
        )


        emotion = emotion_labels[
            emotion_index
        ]


        # Save latest emotion

        detected_emotion = emotion


        # Confidence

        confidence = (
            predictions[0][emotion_index]
            * 100
        )


        # ==================================
        # DRAW FACE
        # ==================================

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )


        # Display emotion

        text = (
            f"{emotion} "
            f"({confidence:.1f}%)"
        )


        cv2.putText(
            frame,
            text,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )


    # ======================================
    # DISPLAY TIMER
    # ======================================

    elapsed_time = (
        time.time() - start_time
    )

    remaining_time = max(
        0,
        detection_time - int(elapsed_time)
    )


    cv2.putText(
        frame,
        f"Detecting... {remaining_time}s",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )


    # Display camera

    cv2.imshow(
        "AI Music - Emotion Detection",
        frame
    )


    # ======================================
    # STOP AFTER 5 SECONDS
    # ======================================

    if elapsed_time >= detection_time:

        break


    # Allow manual Q exit

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# ==========================================
# SAVE FINAL EMOTION
# ==========================================

if detected_emotion:

    with open(
        "emotion/current_emotion.txt",
        "w"
    ) as f:

        f.write(
            detected_emotion
        )

    print(
        "✅ Detected emotion:",
        detected_emotion
    )

else:

    print(
        "⚠️ No face detected"
    )


# ==========================================
# CLOSE CAMERA
# ==========================================

camera.release()

cv2.destroyAllWindows()

print("✅ Emotion detection finished")
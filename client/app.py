from flask import Flask, render_template, request, jsonify, session, Response
import cv2
import mediapipe as mp
import pickle
import numpy as np
import warnings
from flask_socketio import SocketIO, emit
import base64

import database

app = Flask(__name__, static_url_path='/static')
socketio = SocketIO(app)

app.secret_key = 'your_secret_key'

# Suppress specific deprecation warnings from protobuf
warnings.filterwarnings("ignore", category=UserWarning, message=".*GetPrototype.*")

words = {
    "alphabet": ["A", "B", "C"],
    "numbers": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
    "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "terms": ["Hello", "Goodbye", "Please", "Thank you", "Sorry", "Yes", "No"],
    "nature": ["Mountain", "Water", "Te reo"]
}

connection, cursor = database.connectDB()
database.setUpWordsTable(connection, cursor, words)
database.printTable(cursor, "words")
database.closeDB(connection)

# Load the model
model_dict = pickle.load(open('model.pickle', 'rb'))
model = model_dict['model']

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

prediction = None
def generate_frames():
    global prediction
    cap = cv2.VideoCapture(0)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            data_aux = []
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )

                    for landmark in hand_landmarks.landmark:
                        data_aux.extend([landmark.x, landmark.y])

                if len(results.multi_hand_landmarks) == 1:
                    data_aux.extend([0.0] * 42)

                if len(data_aux) == 84:
                    prediction = model.predict([np.asarray(data_aux)])
            else:
                prediction = None
                
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    finally:
        cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_gesture')
def get_gesture():
    return jsonify(gesture=str(prediction))

@app.route('/pokedex')
def pokedex():
    seen_words = session.get('seen_words', [])
    return render_template('pokedex.html', words=words, seen_words=seen_words)

# @app.route('/category/<category>')
# def category(category):
#     category_words = words.get(category, {})
#     seen_words = session.get('seen_words', [])
#     return render_template('category.html', category=category.capitalize(), words=category_words, seen_words=seen_words)

if __name__ == '__main__':
    app.run(debug=True)

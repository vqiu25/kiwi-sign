from flask import Flask, render_template, request, jsonify, session, Response
import cv2
import mediapipe as mp
import pickle
import numpy as np
import warnings
from flask_socketio import SocketIO, emit
import base64

app = Flask(__name__, static_url_path='/static')
socketio = SocketIO(app)

app.secret_key = 'your_secret_key'

# Suppress specific deprecation warnings from protobuf
warnings.filterwarnings("ignore", category=UserWarning, message=".*GetPrototype.*")

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

words = {
    "greetings": {
        "Hello": "Kia ora",
        "Goodbye": "Haere rā",
        "Thank you": "Ngā mihi"
    },
    "numbers": {
        "Zero": "Kore",
        "One": "Tahi",
        "Two": "Rua",
        "Three": "Toru",
        "Four": "Whā",
        "Five": "Rima",
        "Six": "Ono",
        "Seven": "Whitu",
        "Eight": "Waru",
        "Nine": "Iwa"
    },
    "days": {
        "Monday": "Rāhina",
        "Tuesday": "Rātū",
        "Wednesday": "Rāapa",
        "Thursday": "Rāpare",
        "Friday": "Rāmere",
        "Saturday": "Rāhoroi",
        "Sunday": "Rātapu"
    },
    "months": {
        "January": "Kohitātea",
        "February": "Hui-tanguru",
        "March": "Poutū-te-rangi",
        "April": "Paenga-whāwhā",
        "May": "Haratua",
        "June": "Pipiri",
        "July": "Hōngongoi",
        "August": "Here-turi-kōkā",
        "September": "Mahuru",
        "October": "Whiringa-ā-nuku",
        "November": "Whiringa-ā-rangi",
        "December": "Hakihea"
    },
    "terms": {
        "Welcome": "Nau mai",
        "Please": "Tēnā koa",
        "Yes": "Āe",
        "No": "Kāo",
        "Excuse me": "Aroha mai",
        "Family": "Whānau",
        "Friend": "Hoa",
        "House": "Whare",
        "Food": "Kai",
        "Water": "Wai"
    }
}

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

@app.route('/category/<category>')
def category(category):
    category_words = words.get(category, {})
    seen_words = session.get('seen_words', [])
    return render_template('category.html', category=category.capitalize(), words=category_words, seen_words=seen_words)


def translate_to_maori(word):
    translations = {
        "Hello": "Kia ora",
        "Goodbye": "Haere rā",
        "Thank you": "Ngā mihi",
        "A": "Ā",
        "E": "Ē",
        "I": "Ī",
        "O": "Ō",
        "U": "Ū",
        "Zero": "Kore",
        "One": "Tahi",
        "Two": "Rua",
        "Three": "Toru",
        "Four": "Whā",
        "Five": "Rima",
        "Six": "Ono",
        "Seven": "Whitu",
        "Eight": "Waru",
        "Nine": "Iwa",
        "Monday": "Rāhina",
        "Tuesday": "Rātū",
        "Wednesday": "Rāapa",
        "Thursday": "Rāpare",
        "Friday": "Rāmere",
        "Saturday": "Rāhoroi",
        "Sunday": "Rātapu",
        "January": "Kohitātea",
        "February": "Hui-tanguru",
        "March": "Poutū-te-rangi",
        "April": "Paenga-whāwhā",
        "May": "Haratua",
        "June": "Pipiri",
        "July": "Hōngongoi",
        "August": "Here-turi-kōkā",
        "September": "Mahuru",
        "October": "Whiringa-ā-nuku",
        "November": "Whiringa-ā-rangi",
        "December": "Hakihea"
    }
    return translations.get(word, word)

if __name__ == '__main__':
    app.run(debug=True)

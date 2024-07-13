from flask import Flask, render_template, Response, jsonify
import cv2
import mediapipe as mp
import pickle
import numpy as np
import warnings
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

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
                    # print(f"Predicted Gesture: {prediction}")

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    finally:
        cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @socketio.on('frame')
# def handle_frame(data):
#     emit('response', {'prediction': prediction})

@app.route('/get_gesture')
def get_gesture():
    return jsonify(gesture=str(prediction))

if __name__ == '__main__':
    app.run(debug=True)

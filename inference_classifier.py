import cv2
import mediapipe as mp
import pickle
import numpy as np
import warnings

# Suppress specific deprecation warnings from protobuf
warnings.filterwarnings("ignore", category=UserWarning, message=".*GetPrototype.*")

# Load the model
model_dict = pickle.load(open('model.pickle', 'rb'))
model = model_dict['model']

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        data_aux = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
                
                # Collect landmark data
                for landmark in hand_landmarks.landmark:
                    data_aux.extend([landmark.x, landmark.y])
            
            # Ensure data_aux is of length 84 (2 hands * 21 landmarks * 2 coordinates)
            if len(results.multi_hand_landmarks) == 1:
                # If only one hand is detected, pad with zeros
                data_aux.extend([0.0] * 42)

            # Predict gesture if data_aux is the right length
            if len(data_aux) == 84:
                prediction = model.predict([np.asarray(data_aux)])
                print(f"Predicted Gesture: {prediction}")

        cv2.imshow('frame', frame)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()

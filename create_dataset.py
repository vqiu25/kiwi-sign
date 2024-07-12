import os
import cv2
import pickle
import mediapipe as mp

mp_hands = mp.solutions.hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)

DATA_DIR = './data'

data = []
labels = []

for dir_ in os.listdir(DATA_DIR):
    dir_path = os.path.join(DATA_DIR, dir_)
    if os.path.isdir(dir_path):
        for img_path in os.listdir(dir_path):
            if img_path.endswith(('.png', '.jpg', '.jpeg', '.bmp')):  # Filter for image files only
                full_path = os.path.join(dir_path, img_path)
                img = cv2.imread(full_path)
                if img is None:
                    print(f"Failed to load image at {full_path}")
                    continue
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = mp_hands.process(img_rgb)

                data_aux = []
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        for landmark in hand_landmarks.landmark:
                            data_aux.extend([landmark.x, landmark.y])
                # Ensure data_aux is of length 84 (2 hands * 21 landmarks * 2 coordinates)
                if len(data_aux) < 84:
                    data_aux.extend([0.0] * (84 - len(data_aux)))

                data.append(data_aux)
                labels.append(dir_)

with open('data.pickle', 'wb') as f:
    pickle.dump({'data': data, 'labels': labels}, f)

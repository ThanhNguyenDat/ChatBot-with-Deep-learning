import os
import sys
import os

import numpy as np
from mtcnn import MTCNN
import cv2
import dlib
import pickle
from imutils import face_utils

print(sys.path)

detector = MTCNN()
landmark_detector = dlib.shape_predictor("../face_models/shape_predictor_68_face_landmarks.dat")


# 1. Read face_data folder
raw_folder = "face_data"

landmark_list = []
label_list = []

for folder in os.listdir(raw_folder):
    if folder[0] != ".":
        print("Process folder ", folder)

        for file in os.listdir(os.path.join(raw_folder, folder)):
            print("Process file ", file)

            # Phát hiện khuôn mặt
            pix_file = os.path.join(raw_folder, folder, file)
            image = cv2.imread(pix_file)

            results = detector.detect_faces(image)

            if len(results) > 0:
                # Get the first face
                result = results[0]

                # Extract location face
                x1, y1, width, height = result['box']

                x1, y1 = abs(x1), abs(y1)
                x2 = x1 + width
                y2 = y1 + height

                face = image[y1: y2, x1: x2]

                landmark = landmark_detector(image, dlib.rectangle(x1, y1, x2, y2))
                landmark = face_utils.shape_to_np(landmark)

                landmark = landmark.reshape(68 * 2)

                # Add landmark to list of landmarks
                landmark_list.append(landmark)
                label_list.append(folder)

print(len(landmark_list))

# Convert to numpy array
landmark_list = np.array(landmark_list)
label_list = np.array(label_list)

# Write list into pickle file
file = open("face_data/landmarks.pkl", "wb")
pickle.dump(landmark_list, file)
file.close()

file = open("face_data/labels.pkl", "wb")
pickle.dump(label_list, file)
file.close()

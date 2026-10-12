import dlib
import numpy as np
import cv2
import pandas as pd
import os
import logging
import requests
from datetime import datetime, time
import os
from dotenv import load_dotenv
load_dotenv()

# Load OpenCV DNN face detector
face_net = cv2.dnn.readNetFromCaffe(
    "deploy.prototxt.txt",
    "res10_300x300_ssd_iter_140000_fp16.caffemodel"
)

# Load Dlib models
predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')
face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

# ---- Backend connection settings ----
BACKEND_URL = "http://localhost:8000"
DEVICE_API_KEY = os.getenv("DEVICE_API_KEY")


class FaceRecognizer:
    def __init__(self):
        self.face_feature_known_list = []
        self.face_name_known_list = []
        self.frame_skip = 3
        self.frame_cnt = 0

    def get_face_database(self):
        if os.path.exists("data/features_all.csv"):
            csv_rd = pd.read_csv("data/features_all.csv", header=None)
            self.face_name_known_list = csv_rd.iloc[:, 0].tolist()
            self.face_feature_known_list = csv_rd.iloc[:, 1:].values
            logging.info(f"Loaded {len(self.face_name_known_list)} faces from database")
            return True
        else:
            logging.warning("Face database not found!")
            return False

    @staticmethod
    def return_euclidean_distance(feature_1, feature_2):
        feature_1 = np.array(feature_1)
        feature_2 = np.array(feature_2)
        return np.linalg.norm(feature_1 - feature_2)

    def save_attendance_to_api(self, name_str, check_out=False):
        """
        name_str is expected in 'Name_EmployeeID' format, e.g. 'Kumar_3'.
        Calls the FastAPI backend's face check-in/checkout endpoints.
        """
        try:
            name, employee_id = name_str.split('_')
        except ValueError:
            logging.error(f"Invalid name format in known faces database: {name_str} (expected Name_EmployeeID)")
            return

        endpoint = "/attendance/face-checkout" if check_out else "/attendance/face-checkin"
        url = BACKEND_URL + endpoint
        headers = {"X-Device-Key": DEVICE_API_KEY}
        payload = {"employee_id": int(employee_id)}

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            if response.status_code == 200:
                logging.info(f"Attendance recorded for {name}: {response.json()}")
            else:
                logging.error(f"Failed for {name} ({response.status_code}): {response.text}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Could not reach backend for {name}: {e}")

    def is_check_in_time(self):
        current_time = datetime.now().time()
        start_time = time(8, 0)   # 8:00 AM
        end_time = time(15, 0)    # 11:00 AM
        return start_time <= current_time <= end_time

    def is_check_out_time(self):
        current_time = datetime.now().time()
        check_out_time = time(17, 0)  # 5:00 PM
        return current_time >= check_out_time

    def detect_faces(self, img):
        blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), (104.0, 177.0, 123.0))
        face_net.setInput(blob)
        detections = face_net.forward()
        h, w = img.shape[:2]
        faces = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.6:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                faces.append((startX, startY, endX, endY))
        return faces

    def recognize_faces(self, img, faces):
        face_names = []
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        rgb_img = np.ascontiguousarray(rgb_img, dtype=np.uint8)
        # for (startX, startY, endX, endY) in faces:
        #     shape = predictor(img, dlib.rectangle(startX, startY, endX, endY))
        #     face_descriptor = np.array(face_reco_model.compute_face_descriptor(img, shape))
        
        
        for (startX, startY, endX, endY) in faces:
            shape = predictor(rgb_img, dlib.rectangle(startX, startY, endX, endY))
            face_descriptor = np.array(face_reco_model.compute_face_descriptor(rgb_img, shape))
            # Compare with known faces
            distances = [
                self.return_euclidean_distance(face_descriptor, known_face)
                for known_face in self.face_feature_known_list
            ]
            min_distance = min(distances) if distances else 999
            name = "Unknown"
            if distances and min_distance < 0.4:
                name = self.face_name_known_list[distances.index(min_distance)]

            face_names.append(name)

            # Draw rectangle and label
            cv2.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0), 1)
            cv2.putText(img, name, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # Save attendance only if the person is known and during the check-in or check-out time
            if name != "Unknown":
                if self.is_check_in_time():
                    self.save_attendance_to_api(name)
                elif self.is_check_out_time():
                    self.save_attendance_to_api(name, check_out=True)

        return img

    def process(self, stream):
        if not self.get_face_database():
            return

        while stream.isOpened():
            self.frame_cnt += 1
            ret, frame = stream.read()

            if not ret:
                break

            # Process every nth frame
            if self.frame_cnt % self.frame_skip == 0:
                # Resize frame for faster processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

                # Detect and recognize faces
                faces = self.detect_faces(small_frame)
                frame_with_names = self.recognize_faces(small_frame, faces)

                # Show the result
                cv2.imshow("Face Recognition", frame_with_names)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        stream.release()
        cv2.destroyAllWindows()

    def run(self):
        cap = cv2.VideoCapture(0)  # laptop webcam
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.process(cap)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    face_recognizer = FaceRecognizer()
    face_recognizer.run()
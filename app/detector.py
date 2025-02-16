import mediapipe as mp
import numpy as np
import cv2
from datetime import datetime

class BlinkDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.left_eye = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        self.right_eye = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        
    def detect_blink(self, frame):
        with self.mp_face_mesh.FaceMesh(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(frame)
            
            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0].landmark
                ratio = self.calculate_blink_ratio(landmarks)
                return ratio
            return None
    
    def calculate_blink_ratio(self, landmarks):
        # Calculate eye aspect ratio
        def get_eye_ratio(eye_points):
            p1 = np.array([landmarks[eye_points[0]].x, landmarks[eye_points[0]].y])
            p2 = np.array([landmarks[eye_points[8]].x, landmarks[eye_points[8]].y])
            p3 = np.array([landmarks[eye_points[12]].x, landmarks[eye_points[12]].y])
            p4 = np.array([landmarks[eye_points[4]].x, landmarks[eye_points[4]].y])
            
            horizontal = np.linalg.norm(p2 - p1)
            vertical = np.linalg.norm(p4 - p3)
            
            return horizontal / vertical if vertical != 0 else 0
            
        left_ratio = get_eye_ratio(self.left_eye)
        right_ratio = get_eye_ratio(self.right_eye)
        
        return (left_ratio + right_ratio) / 2

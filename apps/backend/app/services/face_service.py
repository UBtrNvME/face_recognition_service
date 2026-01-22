# app/services/face_service.py
from pathlib import Path
import numpy as np
import cv2
import dlib
from typing import List
from app.services.image_input import ImageInput

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODELS_PATH = BASE_DIR / "models"
class FaceService:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(str(MODELS_PATH / "shape_predictor_68_face_landmarks.dat"))
        self.face_recognition_model = dlib.face_recognition_model_v1(str(MODELS_PATH / "dlib_face_recognition_resnet_model_v1.dat"))

    def extract_encodings(self, image_input: ImageInput) -> List[np.ndarray]:
        """
        Extract face encodings from image.
        Returns a list of 128-dimensional face encodings.
        """
        print(image_input)
        img = image_input.to_ndarray()
        
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        faces = self.detector(rgb_img)
        
        encodings = []
        for face in faces:
            shape = self.predictor(rgb_img, face)
            face_encoding = self.face_recognition_model.compute_face_descriptor(rgb_img, shape)
            encodings.append(np.array(face_encoding))
        
        return encodings


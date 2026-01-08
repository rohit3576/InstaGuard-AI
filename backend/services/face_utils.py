import cv2
from typing import List
import numpy as np

# Load Haar Cascade once
FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def extract_faces(frame: np.ndarray) -> List[np.ndarray]:
    """
    Detect and crop faces from a frame.
    Returns list of face images.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = FACE_CASCADE.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(60, 60)
    )

    face_images = []
    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]
        face_images.append(face)

    return face_images

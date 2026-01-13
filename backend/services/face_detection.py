import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection


class FaceDetector:
    def __init__(self, min_confidence: float = 0.5):
        self.detector = mp_face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=min_confidence
        )

    def detect_faces(self, frame):
        """
        Input: BGR frame (OpenCV)
        Output: list of bounding boxes
        """
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.detector.process(rgb_frame)

        faces = []

        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box

                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)

                faces.append({
                    "x": x,
                    "y": y,
                    "w": width,
                    "h": height,
                    "confidence": float(detection.score[0])
                })

        return faces

import cv2
from typing import List

def extract_frames(video_path: str, every_n_frames: int = 30, max_frames: int = 20) -> List:
    cap = cv2.VideoCapture(video_path)
    frames = []
    idx = 0

    if not cap.isOpened():
        return frames

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if idx % every_n_frames == 0:
            frames.append(frame)

        if len(frames) >= max_frames:
            break

        idx += 1

    cap.release()
    return frames

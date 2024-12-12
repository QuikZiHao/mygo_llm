import os
import cv2  
from typing import Any


def get_frames(video_path: str, output_dir: str) -> Any:
    if not os.path.isfile(video_path):
        print(f"Error: {video_path} not found!")
        return

    os.makedirs(output_dir, exist_ok=True)
    print(f"Start Processing: {video_path}")
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Cannot open video.")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print(f"Total Frames: {total_frames}, FPS: {fps}")

    frame_interval = 12
    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_idx % frame_interval == 0:
            output_path = os.path.join(output_dir, f"frame_{frame_idx:06d}.jpg")
            cv2.imwrite(output_path, frame)
            print(f"Saved: {output_path}")
        
        frame_idx += 1

    cap.release()
    print("Extraction completed.")
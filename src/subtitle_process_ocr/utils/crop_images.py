import os
import cv2
import shutil
from typing import Any
from ..constants import FRAME_PATH, CROP_DIR


def crop_images(eps_idx:str) -> Any:
    if os.path.exists(CROP_DIR):
        shutil.rmtree(CROP_DIR)
    os.makedirs(CROP_DIR, exist_ok=True)
    frames_folder = os.path.join(FRAME_PATH, eps_idx)
    if not os.path.exists(frames_folder):
        raise FileNotFoundError(f"Frames folder does not exist: {frames_folder}")

    for frame in os.listdir(frames_folder):
        frame_path = os.path.join(frames_folder, frame)

        image = cv2.imread(frame_path)

        if image is None:
            print(f"Failed to load image: {frame_path}")
            continue

        subtitle_box = image[630:675, 0:1280]  # Adjust these coordinates
        cropped_path = os.path.join(CROP_DIR, frame)
        cv2.imwrite(cropped_path, subtitle_box)
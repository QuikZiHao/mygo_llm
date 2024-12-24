import os
from ..constants import CROP_DIR
from PIL import Image, ImageEnhance, ImageOps

def preprocess():
    for frame in os.listdir(CROP_DIR):
        frame_path = os.path.join(CROP_DIR, frame)

        image = Image.open(frame_path)
        if image is None:
            print(f"Failed to load image: {frame_path}")
            continue
        grayscale_image = ImageOps.grayscale(image)
        contrast_enhancer = ImageEnhance.Contrast(grayscale_image)
        high_contrast_image = contrast_enhancer.enhance(2.0)  # Increase contrast
        sharpness_enhancer = ImageEnhance.Sharpness(high_contrast_image)
        sharpened_image = sharpness_enhancer.enhance(2.0)  # Increase sharpness
        sharpened_image.save(frame_path)

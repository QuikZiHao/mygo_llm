
import os
import shutil
import pandas as pd
from typing import Any
from ..constants import SPEECH_PATH, DATASET_IMAGE_DIR, DATASET_PATH
import re

def get_frame_number(filename) -> int:
    # Use regular expression to extract the digits from the filename
    match = re.search(r'frame_(\d+)\.jpg', filename)
    if match:
        return int(match.group(1))  # Return the integer value of the frame number
    else:
        raise ValueError("Filename format is incorrect")


def get_dataset() -> Any:
    df = pd.read_excel(SPEECH_PATH)
    df = df.drop_duplicates(subset=['eps', 'get_frame'])
    grouped = df.groupby('eps')
    
    random_samples = []

    # Define the base directory for saving images  # Replace with your target directory
    os.makedirs(DATASET_IMAGE_DIR, exist_ok=True)  # Create base directory if not exists

    for eps, group in grouped:
    # Randomly sample 100 rows from the group
        sample = group.sample(n=100, replace=False) if len(group) >= 100 else group  # In case there are less than 100 rows
        # Step 4: Create the output format
        for _, row in sample.iterrows():
            get_frame_value = row['get_frame']
            image_name = f"{get_frame_value}"
            dir_name = f"assets/frames/{eps}"
            speech = row['speech']
            frame_number = get_frame_number(get_frame_value)
            dir_number = eps
            
            # Add to the list
            random_samples.append([image_name, dir_name, speech, frame_number, dir_number])

    output_df = pd.DataFrame(random_samples, columns=['image_name', 'dir_name', 'speech', 'frame_number', 'dir_number'])
    output_df.to_csv(DATASET_PATH, encoding="utf-8")

    print(f"Total rows in output_df: {len(output_df)}")

    for _, row in output_df.iterrows():
        source_path = os.path.join(row["dir_name"], row["image_name"])  # Original file path
        target_path = os.path.join(DATASET_IMAGE_DIR, f"{row["dir_number"]}_{row["image_name"]}")  # Target image path

        # Check if the source path exists before copying
        if os.path.exists(source_path):
            try:
                # Copy the image to the target directory
                shutil.copy(source_path, target_path)
                print(f"Copied: {source_path} -> {target_path}")
            except Exception as e:
                print(f"Error copying {source_path} to {target_path}: {e}")
        else:
            print(f"File not found: {source_path}")

    print("All images have been processed!")

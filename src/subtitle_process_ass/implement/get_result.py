import os
from typing import Tuple
from ..utils import solve_sub,save_sub_to_csv,save_sub_to_json, get_frame, get_fps
from ..constants import JSON_DATA_DIR, CSV_DATA_DIR, LANGUAGE, SUB_DIR, FILENAME_TEMPLATE, VIDEO_DIR
from ..entity.sub import Sub

def get_result(eps_range:Tuple[int, int]):
    if LANGUAGE not in ['sc', 'tc']:
        raise ValueError("Version must be 'sc' or 'tc'")
    version = LANGUAGE.upper()
    for eps_idx in range(eps_range[0],eps_range[1]+1):
        subtitles = []
        eps_filename = FILENAME_TEMPLATE.format(eps_idx, version)
        video_path = os.path.join(VIDEO_DIR, f"{eps_idx}.mp4")
        file_path = os.path.join(SUB_DIR,eps_filename)
        csv_output_dir = os.path.join(CSV_DATA_DIR,f"{eps_idx}.csv")
        json_output_dir = os.path.join(JSON_DATA_DIR,f"{eps_idx}.json")
        os.makedirs(CSV_DATA_DIR, exist_ok=True)
        os.makedirs(JSON_DATA_DIR, exist_ok=True)
        fps = get_fps(video_path)
        if os.path.exists(file_path):
            subtitles = solve_sub(file_path)
        else:
            print(f"File not found: {file_path}")
        if subtitles:
            for sub in subtitles:
                start_frame, end_frame = get_frame(fps=fps, start_time_ms=sub.start_time, end_time_ms=sub.end_time)
                sub.start_frame = start_frame
                sub.end_frame = end_frame
            save_sub_to_json(subtitles, json_output_dir)
            save_sub_to_csv(subtitles, csv_output_dir)
            print(f"Done eps: {eps_idx}")
        else:
            print(f"No subtitles to save for eps: {eps_idx}")

        



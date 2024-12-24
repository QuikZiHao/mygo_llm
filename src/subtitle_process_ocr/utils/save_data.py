import json
import csv
from typing import List
from ..entity.subtitle_data import SubtitleData


def save_sub_to_json(subtitle_data_list: List[SubtitleData], json_filepath: str):
    # Convert SubtitleData list to a list of dictionaries
    subtitle_dict_list = [subtitle.__dict__ for subtitle in subtitle_data_list]
    
    # Write to JSON file
    with open(json_filepath, 'w', encoding='utf-8') as json_f:
        json.dump(subtitle_dict_list, json_f, ensure_ascii=False, indent=4)
    print(f"Data saved to {json_filepath}.")

def save_sub_to_csv(subtitle_data_list: List[SubtitleData], csv_filepath: str):
    # Define the header for the CSV file
    header = [
        "image_name", "dir_name", "speech", "score", "have_sub",
        "left_top_x", "left_top_y", "right_top_x", "right_top_y",
        "left_bottom_x", "left_bottom_y", "right_bottom_x", "right_bottom_y"
    ]
    
    # Open the CSV file and write the data
    with open(csv_filepath, 'w', newline='', encoding='utf-8') as csv_f:
        writer = csv.DictWriter(csv_f, fieldnames=header)
        writer.writeheader()  # Write the header
        
        # Write each subtitle data row
        for subtitle in subtitle_data_list:
            writer.writerow(subtitle.__dict__)
    print(f"Data saved to {csv_filepath}.")
import os
from typing import Tuple
from paddleocr import PaddleOCR
from ..constants import OCR_LANGUAGE, JSON_DATA_DIR, CSV_DATA_DIR
from ..utils import crop_images, ocr_dir, save_sub_to_json, save_sub_to_csv


def get_result(eps_range:Tuple[int, int]):
    #chinese_cht_PP-OCRv3
    ocr = PaddleOCR(use_angle_cls=True, lang=OCR_LANGUAGE)
    for eps_idx in range(eps_range[0],eps_range[1]+1):
        print("start OCR eps:",eps_idx)
        crop_images(str(eps_idx))
        result = ocr_dir(str(eps_idx),ocr)
        json_filepath = os.path.join(JSON_DATA_DIR,f"{eps_idx}.json")
        csv_filepath = os.path.join(CSV_DATA_DIR,f"{eps_idx}.csv")
        save_sub_to_json(result, json_filepath)
        save_sub_to_csv(result, csv_filepath)
        print("Done eps:",eps_idx)


        



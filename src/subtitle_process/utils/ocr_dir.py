import os
from ..constants import CROP_DIR, FRAME_PATH
from typing import List
from paddleocr import PaddleOCR
from ..entity.subtitle_data import SubtitleData
from .solve_coordinates import solve_coordiante

def ocr_dir(eps_idx:str, ocr: PaddleOCR) -> List[SubtitleData]:
    result_list = []
    frame_dir = os.path.join(FRAME_PATH, eps_idx)

    if not os.path.exists(CROP_DIR):
        raise FileNotFoundError(f"Crop directory does not exist: {CROP_DIR}")
    
    for frame in os.listdir(CROP_DIR):
        frame_path = os.path.join(CROP_DIR, frame)
        try:
            result = ocr.ocr(frame_path, cls=True)
        except Exception as e:
            print(f"Error during OCR for {frame}: {e}")
            result = None

        if result != [None]:
            for res in result:
                try:
                    temp = SubtitleData(
                        image_name=frame,
                        dir_name=frame_dir,
                        speech=res[0][1][0],
                        score=res[0][1][1],
                        have_sub=True,
                        **solve_coordiante(res[0][0])
                    )
                    result_list.append(temp)
                except:
                    continue
            continue
        temp = SubtitleData(
            image_name=frame,
            dir_name=frame_dir,
            speech="",
            score=0,
            have_sub=False
        )
        result_list.append(temp)
    return result_list

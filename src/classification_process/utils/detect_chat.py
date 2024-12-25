import numpy as np
from typing import List
from ..entity.detection import Detection
from ..utils.predict_utils import name_include, solve_detections
from ..constants import CHARACTER_AMT, NAME_CONFIG

def detect_chat(speech: str, detections_list: List[List[Detection]]) -> str:
    name_score = name_include(speech)
    len_detections = len(detections_list)
    score_array = np.zeros(CHARACTER_AMT, dtype=float)
    for detections in detections_list:
        score_array += solve_detections(detections)
    score_array /= len_detections
    score_array += name_score
    max_score_idx = np.argmax(score_array)
    max_score = score_array[max_score_idx]
    if max_score >= 0.3:
        return NAME_CONFIG[max_score_idx]["label"]
    return "unknown"

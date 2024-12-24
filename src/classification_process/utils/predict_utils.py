import numpy as np
from ..entity.detection import Detection
from typing import List


def is_open_mouth(person:Detection, mouth:Detection)->bool:
    if person.have_open_mouth:
        return True
    x1 = max(person.bbox[0], mouth.bbox[0])
    y1 = max(person.bbox[1], mouth.bbox[1])
    x2 = min(person.bbox[2], mouth.bbox[2])
    y2 = min(person.bbox[3], mouth.bbox[3])
    intersection_area = max(0, x2 - x1) * max(0, y2 - y1)
    mouth_area = (mouth.bbox[2] - mouth.bbox[0]) * (mouth.bbox[3] - mouth.bbox[1])
    iou = intersection_area / mouth_area
    return iou >= 0.6

def check_open_mouth(detections:List[Detection]):
    ppl_detection = []
    mouth_detection = []

    for det in detections:
        if det.label == 0:
            ppl_detection.append(det)
        elif det.label == 1:
            mouth_detection.append(det)
    
    for mouth in mouth_detection:
        for ppl in ppl_detection:
            ppl.have_open_mouth = is_open_mouth(ppl, mouth)
            break
    
    return ppl_detection
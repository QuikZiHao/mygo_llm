import numpy as np

def is_open_mouth(person_bbox:np.ndarray, mouth_bbox:np.ndarray)->bool:
    x1 = max(person_bbox[0], mouth_bbox[0])
    y1 = max(person_bbox[1], mouth_bbox[1])
    x2 = min(person_bbox[2], mouth_bbox[2])
    y2 = min(person_bbox[3], mouth_bbox[3])
    intersection_area = max(0, x2 - x1) * max(0, y2 - y1)
    person_area = (person_bbox[2] - person_bbox[0]) * (person_bbox[3] - person_bbox[1])
    mouth_area = (mouth_bbox[2] - mouth_bbox[0]) * (mouth_bbox[3] - mouth_bbox[1])
    union_area = person_area + mouth_area - intersection_area
    iou = intersection_area / union_area if union_area != 0 else 0
    return iou >= 0.7
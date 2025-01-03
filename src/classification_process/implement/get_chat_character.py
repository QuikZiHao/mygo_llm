import os
from ..utils.load_speech import load_speech
from ..utils.detect_chat import detect_chat
from ..constants import SPEECH_PATH, FRAME_DIR
from typing import Tuple
from ..entity.predictior import YoloONNXPredictor
from tqdm import tqdm

def get_chat_character(eps_range:Tuple[int, int]):
    data = load_speech(SPEECH_PATH)
    predictor = YoloONNXPredictor()
    updated_speech_info = []
    for eps in tqdm(range(eps_range[0], eps_range[1] + 1, 1)):
        for speech_info in tqdm(data[eps-1], leave=False):
            start_frame = int(speech_info["start_frame"].split('_')[1].split('.')[0])
            end_frame = int(speech_info["start_frame"].split('_')[1].split('.')[0])
            list_detections = []
            character = "unknown"
            while(start_frame <= end_frame):
                image_path = os.path.join(FRAME_DIR, str(eps), f"frame_{start_frame:06d}.jpg") 
                list_detections.append(predictor.predict(image_path))
                start_frame += 12
            if len(list_detections) !=0 :
                character = detect_chat(speech_info["speech"], list_detections)
            speech_info["character"] = character
            updated_speech_info.append(speech_info)
    return updated_speech_info

    
    

                


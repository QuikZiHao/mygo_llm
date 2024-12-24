from typing import Tuple

def get_frame(fps:float, start_time_ms:int, end_time_ms:int) -> Tuple[int,int]:
    start_frame = int((start_time_ms / 1000) * fps)
    end_frame = int((end_time_ms / 1000) * fps)
    return (start_frame, end_frame)

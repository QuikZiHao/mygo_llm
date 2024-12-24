from typing import Dict
import json

class Sub:
    def __init__(self, start_time: int, end_time: int, speech: str):
        self.start_time = start_time
        self.end_time = end_time
        self.speech = speech
        self.start_frame = 0
        self.end_frame = 0       

    def to_dict(self) -> Dict:
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "speech": self.speech,
            "start_frame": self.start_frame,
            "end_frame": self.end_frame
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


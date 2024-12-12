import json


class SubtitleData:
    def __init__(
        self, 
        image_name: str,
        dir_name: str,
        speech: str,
        score: float,
        have_sub: bool,
        left_top_x: float = 0,
        left_top_y: float = 0,
        right_top_x: float = 0,
        right_top_y: float = 0,
        left_bottom_x: float = 0,
        left_bottom_y: float = 0,
        right_bottom_x: float = 0,
        right_bottom_y: float = 0
    ):
        self.image_name = image_name
        self.dir_name = dir_name
        self.speech = speech
        self.score = score
        self.have_sub = have_sub
        self.left_top_x = left_top_x
        self.left_top_y = left_top_y
        self.right_top_x = right_top_x
        self.right_top_y = right_top_y
        self.left_bottom_x = left_bottom_x
        self.left_bottom_y = left_bottom_y
        self.right_bottom_x = right_bottom_x
        self.right_bottom_y = right_bottom_y

    def __repr__(self):
        return (
            f"SubtitleData(image_name={self.image_name}, dir_name={self.dir_name}, "
            f"speech={self.speech}, score={self.score}, "
            f"left_top_x={self.left_top_x}, left_top_y={self.left_top_y}, "
            f"right_top_x={self.right_top_x}, right_top_y={self.right_top_y}, "
            f"left_bottom_x={self.left_bottom_x}, left_bottom_y={self.left_bottom_y}, "
            f"right_bottom_x={self.right_bottom_x}, right_bottom_y={self.right_bottom_y})"
        )
    
    def to_dict(self):
        return {
            "image_name": self.image_name,
            "dir_name": self.dir_name,
            "speech": self.speech,
            "score": self.score,
            "have_sub": self.have_sub,
            "left_top_x": self.left_top_x,
            "left_top_y": self.left_top_y,
            "right_top_x": self.right_top_x,
            "right_top_y": self.right_top_y,
            "left_bottom_x": self.left_bottom_x,
            "left_bottom_y": self.left_bottom_y,
            "right_bottom_x": self.right_bottom_x,
            "right_bottom_y": self.right_bottom_y
        }

    def to_json(self):
        return json.dumps(self.to_dict())
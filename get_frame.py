from src.subtitle_process.utils.get_frames import get_frames
import os

eps = 13
for idx in range(0,eps+1):
    get_frames(os.path.join("assets","resource",f"{str(idx)}.mp4"),os.path.join("assets","frames",f"{str(idx)}"))
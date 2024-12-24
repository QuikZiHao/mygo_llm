import cv2

def get_fps(video_path: str) -> float:
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Get FPS (Frames per second) of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    return fps



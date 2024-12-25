import os
from ..utils.load_config import load_config
import torch


DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
SPEECH_PATH = os.path.join("assets", "speech", "ass_result_chinese.xlsx")
DATASET_PATH = os.path.join("assets", "yolo_dataset", "data_frames.csv")
DATASET_IMAGE_DIR = os.path.join("assets", "yolo_dataset", "image")
TRAIN_CONFIG_PATH = os.path.join("config", "yolo_train.yaml")
ONNX_MODEL_CONFIG_PATH = os.path.join("config", "onnx_predictor.yaml")
RESNET_DATA_DIR = os.path.join("assets","resnet_dataset")
NAME_CONFIG_PATH = os.path.join("config", "chat_determine.yaml")
FRAME_DIR = os.path.join("assets", "frames")
CHAT_DATASET = os.path.join("assets", "speech", "speech_final.csv")
NAME_CONFIG = load_config(NAME_CONFIG_PATH)
CHARACTER_AMT = 11

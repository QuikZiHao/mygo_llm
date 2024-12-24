import os
import yaml
from ultralytics import YOLO
from ..utils import load_config
from ..constants import TRAIN_CONFIG_PATH

def train():
    config = load_config(TRAIN_CONFIG_PATH)
    model = YOLO('yolo11n.pt')
    # Run the training using the loaded configuration
    model.train(
        data=config['data'],
        epochs=config['epochs'],
        imgsz=config['imgsz'],
        batch=config['batch'],
        augment=config['augment'],
        device=config['device'],
        save_period=config['save_period']
    )
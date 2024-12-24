import onnxruntime as ort
import numpy as np
from ..constants import ONNX_MODEL_CONFIG_PATH
from ..utils import load_config,check_open_mouth
from .detection import Detection
from typing import List
import cv2
from ultralytics.utils import ops
import torch
from PIL import Image, ImageDraw



class YoloONNXPredictor:
    def __init__(self):
        config = load_config(ONNX_MODEL_CONFIG_PATH)
        self.yolo_session = ort.InferenceSession(config['model_path'])
        self.class_names = config['class_names']
        self.conf_threshold = config['conf_threshold']
        self.iou_threshold = config['iou_threshold']
        self.imgsz =  config["imgsz"]
    
    def preprocess_image(self, image_path:str) -> np.ndarray:
        """
        Preprocess the image for the model input.
        Resize and normalize the image to the correct input size and format.
        """
        image = cv2.imread(image_path)
        image_resized = cv2.resize(image, (self.imgsz, self.imgsz))
        image_resized = image_resized / 255.0
        image_resized = np.transpose(image_resized, (2, 0, 1))
        image_resized = np.expand_dims(image_resized, axis=0).astype(np.float32)
        return image_resized

    def postprocess_output(self, outputs:np.ndarray) -> List[Detection]:
        """
        Postprocess the outputs, apply NMS, and format the detections.
        """
        preds = ops.non_max_suppression( torch.tensor(outputs[0]),conf_thres=0.25,iou_thres=0.45,nc=2)
        preds = np.array(preds)
        preds = preds[0]
        detections = []
        for pred in preds:
            x1, y1, x2, y2, score, label = pred
            detections.append(Detection(label, score, [x1,y1,x2,y2]))
        detections = check_open_mouth(detections)
        return detections
    
    def show_img(self, image_path ,detections):
        image = Image.open(image_path)
        image_resized = image.resize((self.imgsz,self.imgsz))
        draw = ImageDraw.Draw(image_resized)
        for detect in detections:
            x1, y1, x2, y2 = detect.bbox
            x1, y1, x2, y2 = max(0, x1), max(0, y1), min(self.imgsz, x2), min(self.imgsz, y2)
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
            label = f"{'Open' if detect.have_open_mouth else 'Close'} Mouth, Conf {detect.confidence:.2f}"
            draw.text((x1, max(y1 - 10, 0)), label, fill="blue")
        image_resized.show()
        
    def predict(self, image_path, show:bool = False) -> List[Detection]:
        """
        Perform the whole pipeline: load image, run inference, and post-process results.
        """
        image = self.preprocess_image(image_path)
        inputs = {self.yolo_session.get_inputs()[0].name: image}
        outputs =  self.yolo_session.run(None, inputs)
        detections = self.postprocess_output(outputs)
        if show:
            self.show_img(image_path,detections)
        return detections
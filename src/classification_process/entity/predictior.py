import onnxruntime as ort
import numpy as np
from ..constants import ONNX_MODEL_CONFIG_PATH
from ..utils import load_config,check_open_mouth
from .detection import Detection
from typing import List
import cv2
from ultralytics.utils import ops
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image, ImageDraw
from .classification_model import ClassificationModel 



class YoloONNXPredictor:
    def __init__(self):
        config = load_config(ONNX_MODEL_CONFIG_PATH)
        self.yolo_session = ort.InferenceSession(config['onnx_path'])
        available_providers = ort.get_available_providers()
        if "CUDAExecutionProvider" in available_providers:
            self.yolo_session.set_providers(["CUDAExecutionProvider"])
        else:
            self.yolo_session.set_providers(["CPUExecutionProvider"])
        self.resnet_classification = ClassificationModel(len(config['class_names']),pretrained=False)
        self.resnet_classification.load(config['resnet_path'])
        self.conf_threshold = config['conf_threshold']
        self.iou_threshold = config['iou_threshold']
        self.imgsz =  config["imgsz"]
        self.resnet_imgsz = config["resnet_imgsz"]
    
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
        
    def get_images_list(self, image_path:str,detections:List[Detection])->torch.Tensor:
        image = Image.open(image_path).convert("RGB")
        image = image.resize((self.imgsz,self.imgsz))
        transform = transforms.Compose([
            transforms.Resize((self.resnet_imgsz, self.resnet_imgsz)),                
            transforms.ToTensor(),                        
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                std=[0.229, 0.224, 0.225]), 
        ])
        cropped_images = []
        for detection in detections:
            xmin, ymin, xmax, ymax = detection.bbox
            cropped_image = image.crop((xmin, ymin, xmax, ymax))
            transformed_image = transform(cropped_image)
            cropped_images.append(transformed_image)
        batch_tensor = torch.stack(cropped_images)       
        return batch_tensor

    
    def predict(self, image_path, show:bool = False) -> List[Detection]:
        """
        Perform the whole pipeline: load image, run inference, and post-process results.
        """
        image = self.preprocess_image(image_path)
        inputs = {self.yolo_session.get_inputs()[0].name: image}
        outputs =  self.yolo_session.run(None, inputs)
        detections = self.postprocess_output(outputs)
        if len(detections) == 0:
            return detections
        if show:
            self.show_img(image_path,detections)
        images_tensor = self.get_images_list(image_path, detections)
        outputs = self.resnet_classification.predict(images_tensor)
        probabilities = F.softmax(outputs, dim=1)
        max_scores, max_indices = torch.max(probabilities, dim=1)
        for idx in range(len(detections)):
            detections[idx].label = max_indices[idx]
            detections[idx].confidence = max_scores[idx] 
        return detections
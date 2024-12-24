import os
from typing import Any
from ultralytics import YOLO

def yolo_to_onnx(yolo_pt_pathway: str, onnx_output_path:str)-> Any:
    model = YOLO(yolo_pt_pathway)
    model.export(format='onnx') 
    model_dir = os.path.dirname(yolo_pt_pathway)
    onnx_file = os.path.join(model_dir, f"{os.path.basename(yolo_pt_pathway).split('.')[0]}.onnx")
    if os.path.exists(onnx_file):
        os.rename(onnx_file, onnx_output_path)
        print(f"Model saved to: {onnx_output_path}")
    else:
        print("ONNX file not found. Please check the model export path.")
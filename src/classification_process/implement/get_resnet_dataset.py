import os
from ..utils import load_config
from PIL import Image
from ..constants import TRAIN_CONFIG_PATH, RESNET_DATA_DIR, ONNX_MODEL_CONFIG_PATH

def get_resnet_dataset():
    config = load_config(TRAIN_CONFIG_PATH)
    class_config = load_config(ONNX_MODEL_CONFIG_PATH)
    output_path = RESNET_DATA_DIR
    
    dataset_path = os.path.dirname(config["data"]) 

    label_dirs = ['train/labels', 'valid/labels', 'test/labels']
    image_dirs = ['train/images', 'valid/images', 'test/images']

    class_mapping = {
        idx: class_config["class_names"][idx] for idx in range(len(class_config["class_names"]))
    }

    class_counters = {}
    for class_name in class_mapping.values():
        class_dir = os.path.join(output_path, class_name)
        os.makedirs(class_dir, exist_ok=True)
        class_counters[class_name] = 1 

    # Process label files and copy images
    for label_dir, image_dir in zip(label_dirs, image_dirs):
        full_label_dir = os.path.join(dataset_path, label_dir)
        full_image_dir = os.path.join(dataset_path, image_dir)
        
        # Check if label and image directories exist
        if not os.path.exists(full_label_dir) or not os.path.exists(full_image_dir):
            print(f"Warning: Directory missing - {full_label_dir} or {full_image_dir}")
            continue
        
        for label_file in os.listdir(full_label_dir):
            if label_file.endswith('.txt'):
                label_path = os.path.join(full_label_dir, label_file)
                image_name = os.path.splitext(label_file)[0] + '.jpg'
                image_path = os.path.join(full_image_dir, image_name)

                if not os.path.exists(image_path):
                    print(f"Warning: Image {image_name} not found for label {label_file}")
                    continue

                with Image.open(image_path) as img:
                    img_width, img_height = img.size

                    with open(label_path, 'r') as f:
                        lines = f.readlines()
                        for line in lines:
                            parts = line.strip().split()
                            class_id = int(parts[0]) 
                            if class_id in class_mapping:
                                x_center, y_center, width, height = map(float, parts[1:])
                                x_min = int((x_center - width / 2) * img_width)
                                y_min = int((y_center - height / 2) * img_height)
                                x_max = int((x_center + width / 2) * img_width)
                                y_max = int((y_center + height / 2) * img_height)

                                cropped_img = img.crop((x_min, y_min, x_max, y_max))

                                class_name = class_mapping[class_id]
                                class_dir = os.path.join(output_path, class_name)
                                os.makedirs(class_dir, exist_ok=True)

                                new_image_name = f"{class_counters[class_name]}.jpg"
                                class_counters[class_name] += 1

                                cropped_img.save(os.path.join(class_dir, new_image_name))
                                print(f"Saved cropped image {new_image_name} in {class_name}")
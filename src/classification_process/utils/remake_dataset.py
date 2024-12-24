import os
from ..constants import TRAIN_CONFIG_PATH
from .load_config import load_config


def remake_dataset():
    config = load_config(TRAIN_CONFIG_PATH)
    dataset_dir = os.path.dirname(config["data"])
    label_dirs = ['train/labels', 'valid/labels', 'test/labels'] 

    mouth_class_id = 2 
    new_classes = {
        mouth_class_id: 1,
    } 

    for label_dir in label_dirs:
        full_label_dir = os.path.join(dataset_dir, label_dir)
        if not os.path.exists(full_label_dir):
            continue
        for label_file in os.listdir(full_label_dir):
            if label_file.endswith('.txt'):
                file_path = os.path.join(full_label_dir, label_file)
                new_lines = []
                with open(file_path, 'r') as f:
                    for line in f:
                        parts = line.strip().split()
                        class_id = int(parts[0])
                        if class_id == mouth_class_id:
                            new_class_id = new_classes[mouth_class_id]
                        else:
                            new_class_id = 0  
                        new_lines.append(f"{new_class_id} " + " ".join(parts[1:]))

                with open(file_path, 'w') as f:
                    f.write("\n".join(new_lines))
import yaml
from typing import Any


def load_config(pathway: str) -> Any:
    with open(pathway, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config
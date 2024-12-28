import os
from ..utils.load_config import load_config


LLM_CONFIG_PATH = os.path.join("config", "llm_config.yaml")
LLM_CONFIG = load_config(LLM_CONFIG_PATH)
RAG_DATA_PATH = os.path.join("assets", "speech", "speech_final.csv")
FRAME_DIR = os.path.join("assets", "frames")
NOT_FOUND_PATH =  os.path.join("assets", "frames", "not_found.jpeg")


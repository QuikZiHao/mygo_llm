from src.classification_process.implement.get_chat_character import get_chat_character
from src.classification_process.utils.to_csv import to_csv
from src.classification_process.constants import CHAT_DATASET


speech_info = get_chat_character((1,13))
to_csv(speech_info, CHAT_DATASET)
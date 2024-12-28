import pandas as pd
from ..constants import RAG_DATA_PATH
import re


def clean_speech(text: str) -> str:
    text = re.sub(r'[^\w\s]', '', text) 
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\s+', '', text)   
    text = text.strip()                 
    return text


def solve_data() -> pd.DataFrame:
    df = pd.read_csv(RAG_DATA_PATH, encoding="utf-8")
    df['speech'] = df['speech'].apply(clean_speech)
    df['character_speech'] = df.apply(
        lambda row: f"<{row['character']}>{row['speech']}</{row['character']}>", axis=1
    )
    df['episode'] = df['eps']
    df = df[['character_speech','episode']]
    result ={
    "texts" : df.groupby('episode')['character_speech'].apply(''.join).tolist(),
    "episodes" : [{'episode': str(episode)} for episode in df['episode'].unique()]
    }
    return result   
    




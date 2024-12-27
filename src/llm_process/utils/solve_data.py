import pandas as pd
from ..constants import RAG_DATA_PATH


def solve_data() -> pd.DataFrame:
    df = pd.read_csv(RAG_DATA_PATH, encoding="utf-8")
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
    




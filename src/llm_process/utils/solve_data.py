import pandas as pd
from ..constants import RAG_DATA_PATH


def solve_data() -> pd.DataFrame:
    df = pd.read_csv(RAG_DATA_PATH, encoding="utf-8")
    df['speech'] = df['speech'].apply(lambda x: x.replace("\n", " ").strip())
    df['character_speech'] = df['character'] + ": " + df['speech']
    df['time_range'] = df['start_time'].astype(str) + "-" + df['end_time'].astype(str)
    df['episode'] = df['eps']
    return df[['character_speech', 'time_range', 'episode']]




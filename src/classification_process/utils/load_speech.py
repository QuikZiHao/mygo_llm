import pandas as pd
from typing import List, Dict

def load_speech(pathway: str) -> List[Dict]:
    df = pd.read_excel(pathway, engine='openpyxl')
    grouped = df.groupby('eps')
    grouped_dict_list = [group.to_dict(orient='records') for _, group in grouped]
    return grouped_dict_list
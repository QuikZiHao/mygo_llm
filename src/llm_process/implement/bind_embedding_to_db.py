from ..utils.solve_data import solve_data
from langchain.vectorstores import PGVector
from tqdm import tqdm


def bind_embedding(db: PGVector):
    df = solve_data()
    character_speech_list = df['character_speech'].tolist()
    metadatas = []
    for _, row in tqdm(df.iterrows(), total=df.shape[0], desc="get metadata"):
        metadata = {
            "time_range":row["time_range"],
            "episode":row["episode"]
        }
        metadatas.append(metadata)

    db.afrom_texts(texts=character_speech_list,embedding=db.embeddings,metadatas=metadatas)
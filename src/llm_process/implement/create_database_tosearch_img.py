import pandas as pd
import psycopg2
from ..constants import LLM_CONFIG, RAG_DATA_PATH
from ..utils.solve_data import clean_speech
from urllib.parse import urlparse


def save_speech_to_db():
    df = pd.read_csv(RAG_DATA_PATH, encoding='utf-8')
    connection_string = LLM_CONFIG["db_connection"]
    result = urlparse(connection_string)
    connection = psycopg2.connect(
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port,
        database=result.path[1:]  # Strip the leading '/' from the database name
    )
    cursor = connection.cursor()
    table_name = LLM_CONFIG.get("img_db")
    check_table_query = f"""
            SELECT to_regclass('{table_name}');
        """
    cursor.execute(check_table_query)
    result = cursor.fetchone()[0]
    
    if result is None:
        print(f"Table {table_name} does not exist. Creating the table...")
        # Create table if it doesn't exist
        create_table_query = f"""
        CREATE TABLE {table_name} (
            speech TEXT,
            eps INT,
            character TEXT,
            get_frame TEXT
        );
        """
        cursor.execute(create_table_query)
        print(f"Table {table_name} created successfully.")

    df['speech'] = df['speech'].apply(clean_speech)
    df = df[['speech', 'eps', 'character', 'get_frame']]

    # Insert data into the table
    insert_query = f"""
    INSERT INTO {table_name} (speech, eps, character, get_frame) 
    VALUES (%s, %s, %s, %s);
    """
    
    # Insert rows in batches for better performance
    for chunk_start in range(0, len(df), 1000):  # Adjust the batch size as needed
        chunk = df.iloc[chunk_start:chunk_start + 1000]
        data = chunk.values.tolist()
        cursor.executemany(insert_query, data)
        connection.commit()  # Commit each batch

    print("Data successfully saved to the database.")
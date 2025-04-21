import sqlite3
import pandas as pd
from .config import DB_PATH


TABLE_NAME = 'sources'


def init_db():
    conn = sqlite3.connect(DB_PATH)
    db = conn.cursor()
    db.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url   TEXT,
            xpath TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_sources(df: pd.DataFrame):
    conn = sqlite3.connect(DB_PATH)
    df[['title', 'url', 'xpath']].to_sql(TABLE_NAME, conn, if_exists='append', index=False)
    conn.close()

# engine/history_manager.py
import sqlite3
import pandas as pd
from datetime import datetime
from config import DB_PATH

class HistoryManager:
    def __init__(self):
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS signal_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME,
                    entry_price REAL,
                    predicted_vol REAL,
                    monte_carlo_prob REAL,
                    final_score REAL,
                    tp_price REAL,
                    sl_price REAL,
                    outcome TEXT DEFAULT 'PENDING',
                    real_exit_price REAL
                )
            ''')

    def save_signal(self, data):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute('''
                INSERT INTO signal_history 
                (timestamp, entry_price, predicted_vol, monte_carlo_prob, final_score, tp_price, sl_price)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (datetime.now(), data['entry'], data['vol'], data['prob_tp'], data['score'], data['tp'], data['sl']))

    def update_outcomes(self, current_price):
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query("SELECT * FROM signal_history WHERE outcome = 'PENDING'", conn)
            for _, row in df.iterrows():
                if current_price >= row['tp_price']:
                    conn.execute("UPDATE signal_history SET outcome = 'HIT_TP', real_exit_price = ? WHERE id = ?", (current_price, row['id']))
                elif current_price <= row['sl_price']:
                    conn.execute("UPDATE signal_history SET outcome = 'HIT_SL', real_exit_price = ? WHERE id = ?", (current_price, row['id']))

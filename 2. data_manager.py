# data_manager.py
import yfinance as yf
import time
import pandas as pd
from config import PIP_ADJUSTMENT, BACKOFF_STEPS

class DataManager:
    def __init__(self):
        self.intervals = BACKOFF_STEPS
        self.current_idx = 0
        self.last_fetch_time = 0

    def get_market_data(self):
        """Coleta dados do EUR/USD com tratamento de erro e backoff."""
        elapsed = time.time() - self.last_fetch_time
        if elapsed < self.intervals[self.current_idx]:
            return None

        try:
            # yfinance como fonte primária
            ticker = yf.Ticker("EURUSD=X")
            data = ticker.history(period="1d", interval="1m")
            
            if data.empty or len(data) < 30:
                raise ValueError("Dados insuficientes")
            
            self.last_fetch_time = time.time()
            self._adjust_backoff(success=True)
            
            # Aplica o ajuste de pips para alinhar com o spread real
            data['Close'] = data['Close'] + PIP_ADJUSTMENT
            return data
            
        except Exception as e:
            print(f"Erro na coleta: {e}")
            self._adjust_backoff(success=False)
            return None

    def _adjust_backoff(self, success):
        if success:
            self.current_idx = max(0, self.current_idx - 1)
        else:
            self.current_idx = min(len(self.intervals) - 1, self.current_idx + 1)

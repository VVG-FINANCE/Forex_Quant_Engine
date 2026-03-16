# engine/ml_module.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

class MLModule:
    def __init__(self):
        # RandomForest parametrizado para identificar padrões de Price Action
        self.model = RandomForestClassifier(n_estimators=100, max_depth=5, min_samples_split=10)
        self.is_trained = False

    def prepare_features(self, df):
        """Engenharia de Features: RSI, Volatilidade e Retornos."""
        df['returns'] = df['Close'].pct_change()
        df['volatility'] = df['returns'].rolling(window=10).std()
        df['rsi'] = self._calculate_rsi(df['Close'])
        return df.dropna()

    def _calculate_rsi(self, series, period=14):
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def predict_regime(self, features):
        """Retorna a probabilidade de um movimento altista (0 a 1)."""
        if not self.is_trained: return 0.5
        return self.model.predict_proba(features)[0][1]

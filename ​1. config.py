# config.py
"""
Configurações Globais do Forex Quant Engine (FQE)
"""

PIP_ADJUSTMENT = 0.0001  # Compensação de latência das APIs públicas
MAX_RETRIES = 5          # Máximo de tentativas de conexão
DEFAULT_MODEL_PATH = "data/model_rf.pkl"
DB_PATH = "data/forex_history.db"

# Intervalos do Backoff Adaptativo (em segundos)
BACKOFF_STEPS = [5, 10, 15, 20, 30, 60]

# Parâmetros de Risco
CONFIDENCE_THRESHOLD = 75.0  # Score mínimo para exibir oportunidade

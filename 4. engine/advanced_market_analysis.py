# engine/advanced_market_analysis.py
import numpy as np

class AdvancedAnalysis:
    @staticmethod
    def kalman_filter(measurements):
        """
        Filtro de Kalman Uni-variável para suavização dinâmica de preços.
        Elimina 'spikes' artificiais de feeds de dados públicos.
        """
        if len(measurements) == 0: return 0
        
        x_hat = measurements.iloc[0]  # Estimativa inicial
        p = 1.0                       # Erro de estimativa inicial
        q = 1e-5                      # Ruído do processo (estabilidade do EUR/USD)
        r = 0.0001                    # Ruído da medição (latência da API)
        
        filtered_values = []
        for z in measurements:
            # Predição
            p = p + q
            # Ganho de Kalman
            k = p / (p + r)
            # Atualização
            x_hat = x_hat + k * (z - x_hat)
            p = (1 - k) * p
            filtered_values.append(x_hat)
            
        return filtered_values[-1]

    @staticmethod
    def get_market_momentum(series):
        """Calcula a aceleração do preço (2ª derivada)."""
        velocity = np.diff(series)
        acceleration = np.diff(velocity)
        return acceleration[-1] if len(acceleration) > 0 else 0

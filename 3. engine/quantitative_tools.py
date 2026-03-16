# engine/quantitative_tools.py
import numpy as np
import pandas as pd
from arch import arch_model

class QuantitativeTools:
    @staticmethod
    def calculate_hurst(series):
        """
        Calcula o Expoente de Hurst (H).
        H > 0.5: Tendência (Persistente)
        H < 0.5: Reversão à Média (Anti-persistente)
        H = 0.5: Random Walk
        """
        lags = range(2, 20)
        tau = [np.sqrt(np.std(np.subtract(series[lag:], series[:-lag]))) for lag in lags]
        poly = np.polyfit(np.log(lags), np.log(tau), 1)
        return poly[0] * 2

    @staticmethod
    def get_garch_volatility(price_series):
        """
        Estima a volatilidade futura usando GARCH(1,1) com distribuição t-Student
        para capturar caudas longas (Fat Tails) do mercado Forex.
        """
        # Cálculo de retornos logarítmicos escalonados para estabilidade numérica
        returns = 100 * np.log(price_series / price_series.shift(1)).dropna()
        
        try:
            model = arch_model(returns, vol='Garch', p=1, q=1, dist='t')
            res = model.fit(disp='off')
            
            # Previsão de variância para o próximo passo
            forecast = res.forecast(horizon=1)
            future_vol = np.sqrt(forecast.variance.values[-1, 0]) / 100
            return future_vol
        except:
            # Fallback para desvio padrão simples em caso de erro de convergência
            return returns.std() / 100

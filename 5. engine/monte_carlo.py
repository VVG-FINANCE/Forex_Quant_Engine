# engine/monte_carlo.py
import numpy as np

def run_adaptive_monte_carlo(current_price, garch_vol, steps=60, iterations=1000):
    """
    Simulação de Monte Carlo com Volatilidade Adaptativa.
    Projeta 1.000 trajetórias possíveis para os próximos 60 minutos.
    """
    dt = 1 # Passo de tempo (minuto)
    drift = 0 # Assume-se neutralidade para curto prazo
    
    # Gerar ruído branco gaussiano
    stochastic_matrix = np.random.standard_normal((iterations, steps))
    
    # Caminhos de preços via Movimento Browniano Geométrico
    paths = np.zeros((iterations, steps))
    paths[:, 0] = current_price
    
    for t in range(1, steps):
        # A volatilidade garch_vol modula a dispersão do preço
        paths[:, t] = paths[:, t-1] * np.exp((drift - 0.5 * garch_vol**2) * dt + 
                                             garch_vol * np.sqrt(dt) * stochastic_matrix[:, t])
    
    return paths

def get_probability_metrics(paths, tp_level, sl_level):
    """Calcula P(TP) e P(SL) baseadas na dispersão das simulações."""
    prob_tp = np.mean(np.any(paths >= tp_level, axis=1)) * 100
    prob_sl = np.mean(np.any(paths <= sl_level, axis=1)) * 100
    return round(prob_tp, 2), round(prob_sl, 2)

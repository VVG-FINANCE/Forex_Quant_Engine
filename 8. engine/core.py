# engine/core.py
from engine.ml_module import MLModule
from engine.advanced_market_analysis import AdvancedAnalysis
from engine.quantitative_tools import QuantitativeTools
from engine.monte_carlo import run_adaptive_monte_carlo, get_probability_metrics

class AnalyticsEngine:
    def __init__(self):
        self.ml = MLModule()
        self.analysis = AdvancedAnalysis()

    def process_market_data(self, df):
        # 1. Limpeza
        clean_price = self.analysis.kalman_filter(df['Close'])
        
        # 2. Volatilidade GARCH
        garch_vol = QuantitativeTools.get_garch_volatility(df['Close'])
        
        # 3. Simulação Probabilística
        paths = run_adaptive_monte_carlo(clean_price, garch_vol)
        tp = clean_price + 0.0015
        sl = clean_price - 0.0008
        prob_tp, prob_sl = get_probability_metrics(paths, tp, sl)
        
        # 4. Cálculo de Score Bayesiano (Convergência de Modelos)
        ml_conf = self.ml.predict_regime(df.tail(1))
        hurst = QuantitativeTools.calculate_hurst(df['Close'].values[-30:])
        
        final_score = (ml_conf * 40) + (prob_tp * 0.4) + (hurst * 20)
        
        if final_score > 75:
            return {
                "score": round(final_score, 2),
                "entry": clean_price,
                "tp": tp,
                "sl": sl,
                "vol": garch_vol,
                "prob_tp": prob_tp
            }
        return None

# app.py
from flask import Flask, render_template, jsonify
from data_manager import DataManager
from engine.core import AnalyticsEngine
from engine.history_manager import HistoryManager
import threading
import time

app = Flask(__name__)
data_mgr = DataManager()
engine = AnalyticsEngine()
history = HistoryManager()

# Variável de estado global (simples, cache local)
current_analysis = {"status": "Inicializando..."}

def background_analysis():
    global current_analysis
    while True:
        df = data_mgr.get_market_data()
        if df is not None:
            # 1. Auditoria e Atualização
            history.update_outcomes(df['Close'].iloc[-1])
            
            # 2. Processamento Quantitativo
            analysis = engine.process_market_data(df)
            
            # 3. Persistência de Sinais Qualificados
            if analysis and analysis['score'] > 85:
                history.save_signal(analysis)
                current_analysis = {"opportunity": analysis, "price": df['Close'].iloc[-1]}
            else:
                current_analysis = {"status": "Aguardando setup de alta probabilidade"}
        
        time.sleep(10) # Intervalo de atualização assíncrona

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def status():
    return jsonify(current_analysis)

if __name__ == '__main__':
    threading.Thread(target=background_analysis, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)

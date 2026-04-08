import yfinance as yf
import pandas as pd
import os
from datetime import date

# Crea la cartella se non esiste
os.makedirs("dati", exist_ok=True)

# Lista dei titoli da monitorare
titoli = ["AAPL", "MSFT", "GOOGL", "NVDA", "ENI.MI"]

oggi = date.today().strftime("%Y-%m-%d")

for simbolo in titoli:
    print(f"Scarico {simbolo}...")
    ticker = yf.Ticker(simbolo)
    
    # Ultimi 30 giorni
    dati = ticker.history(period="1mo")
    
    # Salva in CSV
    percorso = f"dati/{simbolo}.csv"
    dati.to_csv(percorso, mode='a', header=not os.path.exists(percorso))
    print(f"  Salvato in {percorso}")

print("Fatto!")

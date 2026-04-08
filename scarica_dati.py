import yfinance as yf
import pandas as pd
import os
from datetime import date

os.makedirs("dati", exist_ok=True)

titoli = ["AAPL", "MSFT", "GOOGL", "NVDA", "ENI.MI"]

for simbolo in titoli:
    print(f"Scarico {simbolo}...")
    ticker = yf.Ticker(simbolo)
    nuovi_dati = ticker.history(period="1mo")

    percorso = f"dati/{simbolo}.csv"

    if os.path.exists(percorso):
        # Carica i dati esistenti e unisce con i nuovi
        dati_esistenti = pd.read_csv(percorso, index_col=0, parse_dates=True)
        dati_uniti = pd.concat([dati_esistenti, nuovi_dati])
        # Elimina i duplicati tenendo l'ultimo valore per ogni data
        dati_uniti = dati_uniti[~dati_uniti.index.duplicated(keep='last')]
        # Ordina per data
        dati_uniti = dati_uniti.sort_index()
        dati_uniti.to_csv(percorso)
    else:
        # Prima esecuzione, crea il file da zero
        nuovi_dati.to_csv(percorso)

    print(f"  Salvato in {percorso}")

print("Fatto!")

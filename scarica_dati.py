import yfinance as yf
import pandas as pd
import os

os.makedirs("dati", exist_ok=True)

titoli = ["AAPL", "MSFT", "GOOGL", "NVDA", "ENI.MI"]

for simbolo in titoli:
    print(f"Scarico {simbolo}...")
    ticker = yf.Ticker(simbolo)
    nuovi_dati = ticker.history(period="1mo")

    # Rimuove le informazioni sul fuso orario per semplicità
    nuovi_dati.index = nuovi_dati.index.tz_localize(None)
    # Mantiene solo la data senza orario
    nuovi_dati.index = nuovi_dati.index.normalize()

    percorso = f"dati/{simbolo}.csv"

    if os.path.exists(percorso):
        dati_esistenti = pd.read_csv(percorso, index_col=0, parse_dates=True)
        dati_uniti = pd.concat([dati_esistenti, nuovi_dati])
        dati_uniti = dati_uniti[~dati_uniti.index.duplicated(keep='last')]
        dati_uniti = dati_uniti.sort_index()
        dati_uniti.to_csv(percorso)
    else:
        nuovi_dati.to_csv(percorso)

    print(f"  Salvato in {percorso}")

print("Fatto!")

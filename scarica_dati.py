import yfinance as yf
import pandas as pd
import os

os.makedirs("dati", exist_ok=True)

titoli = ["AAPL", "MSFT", "GOOGL", "NVDA", "ENI.MI"]

for simbolo in titoli:
    print(f"Scarico {simbolo}...")
    
    try:
        ticker = yf.Ticker(simbolo)
        nuovi_dati = ticker.history(period="1mo")
        print(f"  Righe ricevute: {len(nuovi_dati)}")
        print(nuovi_dati.head())
        
        # Controlla che i dati non siano vuoti
        if nuovi_dati.empty:
            print(f"  Nessun dato ricevuto per {simbolo}, salto.")
            continue

        # Rimuove fuso orario solo se presente
        if hasattr(nuovi_dati.index, 'tz') and nuovi_dati.index.tz is not None:
            nuovi_dati.index = nuovi_dati.index.tz_localize(None)
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

    except Exception as e:
        print(f"  Errore per {simbolo}: {e}, salto.")
        continue

print("Fatto!")

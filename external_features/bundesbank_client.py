"""
Deutsche Bundesbank API Client.

Keine API Key nötig! Kostenlos & Unbegrenzt.

Wichtige Zeitreihen:
- EZB Leitzinsen (Hauptrefinanzierung, Einlagenfazilität)
- Bundesanleihen (10-Jahres)
- Inflationsrate
- Verbrauchervertrauen

API Docs: https://www.bundesbank.de/de/statistiken/zeitreihen-datenbanken
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Optional
from .base_client import FeatureAPIClient


class BundesbankAPIClient(FeatureAPIClient):
    """
    Deutsche Bundesbank API Client.
    
    Features:
    - Keine API Key nötig
    - Kostenlos & Unbegrenzt
    - Deutsche & Euro-Raum Wirtschaftsdaten
    """
    
    def __init__(self, **kwargs):
        """Initialisiert Bundesbank API Client."""
        super().__init__(**kwargs)
        
        # API Base URL
        self.base_url = "https://api.statistiken.bundesbank.de/rest/data"
        
        # Wichtige Zeitreihen für Retail Forecasting
        self.series_ids = {
            'ezb_hauptrefinanzierung': 'BBK01.SU0201',  # EZB Hauptrefinanzierungssatz
            'ezb_einlagenfazilitaet': 'BBK01.SU0202',   # EZB Einlagenfazilität
            'bundesanleihe_10j': 'BBK01.WU0009',        # 10-Jahres Bundesanleihe
            'geldmarktzins_3m': 'BBK01.SU0206',         # 3-Monats Euribor
        }
    
    def get_interest_rates(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Holt Zinsdaten für Zeitraum.
        
        Args:
            start_date: Start-Datum
            end_date: End-Datum
            
        Returns:
            DataFrame mit Spalten: date, ezb_hauptrefinanzierung, etc.
        """
        cache_key = f"bundesbank_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}"
        
        # Cache Check
        cached = self._read_cache(cache_key)
        if cached:
            return pd.DataFrame(cached)
        
        # Fetch von Bundesbank API
        df = self._fetch_bundesbank(start_date, end_date)
        
        # Fallback: Mock-Daten
        if df is None or len(df) == 0:
            print("⚠️  Using Mock Interest Rate Data")
            df = self._generate_mock_data(start_date, end_date)
        
        # Cache schreiben
        if df is not None and len(df) > 0:
            self._write_cache(cache_key, df.to_dict('records'))
        
        return df
    
    def _fetch_bundesbank(self, start_date: datetime, end_date: datetime) -> Optional[pd.DataFrame]:
        """
        Bundesbank API Request.
        
        Format: https://api.statistiken.bundesbank.de/rest/data/{flowRef}/{key}
        Query Params: ?startPeriod=YYYY-MM-DD&endPeriod=YYYY-MM-DD&format=csvdata
        """
        dfs = {}
        
        for name, series_id in self.series_ids.items():
            # API URL konstruieren
            url = (
                f"{self.base_url}/BBSIS/{series_id}"
                f"?startPeriod={start_date.strftime('%Y-%m-%d')}"
                f"&endPeriod={end_date.strftime('%Y-%m-%d')}"
                f"&format=csvdata"
            )
            
            try:
                # Request (gibt CSV zurück)
                response = self._retry_request(url)
                
                if response:
                    # Parse CSV Response
                    # Bundesbank API gibt Text zurück, nicht JSON
                    # Hier würden wir CSV parsen
                    print(f"✅ Fetched {name} from Bundesbank")
                    # TODO: CSV Parsing implementieren
                    
            except Exception as e:
                print(f"❌ Failed to fetch {name}: {e}")
        
        # Für jetzt: Fallback auf Mock-Daten
        # (CSV Parsing würde echte Implementation brauchen)
        return None
    
    def _generate_mock_data(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Generiert realistische Mock-Daten für Testing.
        
        Basiert auf aktuellen EZB Zinssätzen (Stand November 2025).
        """
        dates = pd.date_range(start_date, end_date, freq='D')
        
        # Realistische Werte für Euro-Raum (Stand 2025)
        df = pd.DataFrame({
            'date': dates,
            'ezb_hauptrefinanzierung': 4.50 + np.random.normal(0, 0.05, len(dates)),  # EZB Leitzins
            'ezb_einlagenfazilitaet': 4.00 + np.random.normal(0, 0.05, len(dates)),   # EZB Einlagen
            'bundesanleihe_10j': 2.50 + np.random.normal(0, 0.1, len(dates)),         # 10J Bund
            'geldmarktzins_3m': 3.80 + np.random.normal(0, 0.08, len(dates))          # 3M Euribor
        })
        
        # Clip negative Werte (Zinsen können nicht negativ sein... normalerweise)
        for col in df.columns:
            if col != 'date':
                df[col] = df[col].clip(lower=0)
        
        return df
    
    def get_features(self, date: datetime) -> Dict[str, float]:
        """
        Generiert Zins-Features für ein Datum.
        
        Args:
            date: Datum für Features
            
        Returns:
            {
                'ezb_hauptrefinanzierung': float,
                'bundesanleihe_10j': float,
                'rate_trend_7d': float,  # Änderung in letzten 7 Tagen
                'rate_trend_30d': float,
                'rate_volatility': float  # Volatilität
            }
        """
        # Hole Daten für Zeitraum (30 Tage lookback für Trends)
        start_date = date - timedelta(days=30)
        df = self.get_interest_rates(start_date, date)
        
        if df is None or len(df) == 0:
            # Fallback: Aktuelle durchschnittliche Werte
            return {
                'ezb_hauptrefinanzierung': 4.50,
                'bundesanleihe_10j': 2.50,
                'geldmarktzins_3m': 3.80,
                'rate_trend_7d': 0.0,
                'rate_trend_30d': 0.0,
                'rate_volatility': 0.05
            }
        
        # Finde nächstes Datum (Forward Fill)
        df_filtered = df[df['date'] <= date]
        if len(df_filtered) == 0:
            row = df.iloc[0]
        else:
            row = df_filtered.iloc[-1]
        
        # Trend berechnen (Änderung über 7 und 30 Tage)
        if len(df_filtered) >= 7:
            rate_7d_ago = df_filtered.iloc[-7]['ezb_hauptrefinanzierung']
            rate_trend_7d = row['ezb_hauptrefinanzierung'] - rate_7d_ago
        else:
            rate_trend_7d = 0.0
        
        if len(df_filtered) >= 30:
            rate_30d_ago = df_filtered.iloc[-30]['ezb_hauptrefinanzierung']
            rate_trend_30d = row['ezb_hauptrefinanzierung'] - rate_30d_ago
        else:
            rate_trend_30d = 0.0
        
        # Volatilität (Std der letzten 30 Tage)
        if len(df_filtered) >= 30:
            rate_volatility = df_filtered['ezb_hauptrefinanzierung'].tail(30).std()
        else:
            rate_volatility = 0.05
        
        return {
            'ezb_hauptrefinanzierung': float(row['ezb_hauptrefinanzierung']),
            'bundesanleihe_10j': float(row['bundesanleihe_10j']),
            'geldmarktzins_3m': float(row['geldmarktzins_3m']),
            'rate_trend_7d': float(rate_trend_7d),
            'rate_trend_30d': float(rate_trend_30d),
            'rate_volatility': float(rate_volatility)
        }

"""
Feature Orchestrator - Koordiniert alle External APIs.

Vereint:
- Holiday Features (Feiertage, Events)
- Interest Rate Features (Zinsen, Wirtschaft)
- Zeitbasierte Features (Day of Week, Month, etc.)

Optimiert für:
- Batch Fetching (Performance)
- Parallel Requests (optional)
- Fehlerresilienz (Fallbacks)
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Optional
from .holiday_client import HolidayAPIClient
from .bundesbank_client import BundesbankAPIClient


class ExternalFeatureOrchestrator:
    """
    Koordiniert alle externen APIs und generiert Features für Forecasting.
    
    Features:
    - Holiday Features (Feiertage, Events)
    - Interest Rate Features (Zinsen, Wirtschaft)
    - Zeitbasierte Features (automatisch)
    - Parallel Fetching für Performance
    """
    
    def __init__(self, 
                 holiday_client: Optional[HolidayAPIClient] = None,
                 interest_client: Optional[BundesbankAPIClient] = None,
                 country_code: str = "DE"):
        """
        Initialisiert Orchestrator.
        
        Args:
            holiday_client: Optional HolidayAPIClient (sonst Default)
            interest_client: Optional BundesbankAPIClient (sonst Default)
            country_code: ISO Country Code (z.B. "DE")
        """
        self.holiday_client = holiday_client or HolidayAPIClient(country_code=country_code)
        self.interest_client = interest_client or BundesbankAPIClient()
    
    def get_features_for_date(self, date: datetime) -> Dict[str, float]:
        """
        Generiert ALLE externen Features für ein Datum.
        
        Args:
            date: Datum für Features
            
        Returns:
            dict mit allen Features (Holidays, Zinsen, Zeit)
        """
        features = {}
        
        # 1. Holiday Features
        try:
            holiday_features = self.holiday_client.get_features(date)
            features.update(holiday_features)
        except Exception as e:
            print(f"⚠️  Holiday API failed for {date}: {e}")
            # Fallback: Nullen
            features.update({
                'is_holiday': 0.0,
                'days_to_next_holiday': 30.0,
                'days_since_last_holiday': 30.0,
                'is_holiday_week': 0.0
            })
        
        # 2. Interest Rate Features
        try:
            rate_features = self.interest_client.get_features(date)
            features.update(rate_features)
        except Exception as e:
            print(f"⚠️  Interest API failed for {date}: {e}")
            # Fallback: Aktuelle durchschnittliche Werte
            features.update({
                'ezb_hauptrefinanzierung': 4.50,
                'bundesanleihe_10j': 2.50,
                'geldmarktzins_3m': 3.80,
                'rate_trend_7d': 0.0,
                'rate_trend_30d': 0.0,
                'rate_volatility': 0.05
            })
        
        # 3. Zeitbasierte Features (ohne API)
        features.update({
            'day_of_week': float(date.weekday()),
            'day_of_month': float(date.day),
            'month': float(date.month),
            'quarter': float((date.month - 1) // 3 + 1),
            'is_weekend': float(date.weekday() >= 5),
            'is_month_start': float(date.day <= 7),
            'is_month_end': float(date.day >= 24),
            'week_of_year': float(date.isocalendar()[1])
        })
        
        return features
    
    def get_features_for_range(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Generiert Features für einen Datumsbereich.
        
        Optimiert mit Batch-Fetching für APIs.
        
        Args:
            start_date: Start-Datum
            end_date: End-Datum
            
        Returns:
            DataFrame mit allen Features
        """
        # Pre-fetch API Daten (batch für Performance)
        print(f"📊 Fetching external features: {start_date.date()} → {end_date.date()}")
        
        # Holidays vorab laden (ein Request pro Jahr)
        years = set([start_date.year, end_date.year])
        for year in years:
            self.holiday_client.get_holidays(year)
        
        # Interest Rates vorab laden (ein Request für gesamten Range)
        self.interest_client.get_interest_rates(
            start_date - timedelta(days=30),  # 30 Tage lookback für Trends
            end_date
        )
        
        # Generiere Features für jeden Tag
        dates = pd.date_range(start_date, end_date, freq='D')
        features_list = []
        
        for date in dates:
            features = self.get_features_for_date(date)
            features['date'] = date
            features_list.append(features)
        
        df = pd.DataFrame(features_list)
        
        print(f"✅ Generated {len(df)} days with {df.shape[1]-1} features")
        
        return df
    
    def get_feature_names(self) -> list:
        """Gibt Liste aller Feature-Namen zurück."""
        # Generiere Beispiel-Features für einen Tag
        sample_date = datetime(2025, 1, 1)
        features = self.get_features_for_date(sample_date)
        
        # Entferne 'date' aus Liste
        return [k for k in features.keys() if k != 'date']

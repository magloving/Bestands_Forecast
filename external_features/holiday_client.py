"""
Holiday API Client mit Multiple Providers.

Primary: Nager.Date (kostenlos, keine API Key)
Fallback: Calendarific (API Key, 1000/Monat)
Local Fallback: Manuelle Feiertags-Liste
"""

from datetime import datetime
from typing import Dict, List, Optional
from .base_client import FeatureAPIClient


class HolidayAPIClient(FeatureAPIClient):
    """
    Feiertags-API Client mit Multiple Providers.
    
    Features:
    - Nager.Date (Primary, kostenlos)
    - Calendarific (Fallback, API Key)
    - Local Fallback (manuel gepflegt)
    """
    
    def __init__(self, country_code: str = "DE", api_key: Optional[str] = None, **kwargs):
        """
        Initialisiert Holiday API Client.
        
        Args:
            country_code: ISO Country Code (z.B. "DE", "AT", "CH")
            api_key: Optional Calendarific API Key (für Fallback)
            **kwargs: Weitere Parameter für FeatureAPIClient
        """
        super().__init__(**kwargs)
        self.country_code = country_code
        self.api_key = api_key
        
        # Fallback: Wichtige Feiertage (DE)
        self.fallback_holidays = {
            "01-01": "Neujahr",
            "05-01": "Tag der Arbeit",
            "10-03": "Tag der Deutschen Einheit",
            "12-24": "Heiligabend",
            "12-25": "1. Weihnachtstag",
            "12-26": "2. Weihnachtstag",
            "12-31": "Silvester"
        }
    
    def get_holidays(self, year: int) -> List[Dict]:
        """
        Holt Feiertage für ein Jahr.
        
        Args:
            year: Jahr (z.B. 2025)
            
        Returns:
            Liste von {date: "YYYY-MM-DD", name: "...", type: "public/bank"}
        """
        cache_key = f"holidays_{self.country_code}_{year}"
        
        # 1. Cache Check
        cached = self._read_cache(cache_key)
        if cached:
            return cached
        
        # 2. Primary API: Nager.Date (kostenlos)
        holidays = self._fetch_nager_date(year)
        
        # 3. Fallback: Calendarific (wenn API Key vorhanden)
        if not holidays and self.api_key:
            holidays = self._fetch_calendarific(year)
        
        # 4. Last Fallback: Manuelle Liste
        if not holidays:
            print(f"⚠️  Using Fallback Holidays for {year}")
            holidays = self._generate_fallback_holidays(year)
        
        # Cache schreiben
        if holidays:
            self._write_cache(cache_key, holidays)
        
        return holidays or []
    
    def _fetch_nager_date(self, year: int) -> Optional[List[Dict]]:
        """Nager.Date API (kostenlos, keine API Key)."""
        url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{self.country_code}"
        
        try:
            data = self._retry_request(url)
            if data:
                return [
                    {
                        "date": h["date"],
                        "name": h["localName"],
                        "type": "public" if h.get("global", True) else "regional"
                    }
                    for h in data
                ]
        except Exception as e:
            print(f"❌ Nager.Date failed: {e}")
        
        return None
    
    def _fetch_calendarific(self, year: int) -> Optional[List[Dict]]:
        """Calendarific API (API Key benötigt)."""
        if not self.api_key:
            return None
            
        url = f"https://calendarific.com/api/v2/holidays?api_key={self.api_key}&country={self.country_code}&year={year}"
        
        try:
            data = self._retry_request(url)
            if data and data.get("response"):
                return [
                    {
                        "date": h["date"]["iso"],
                        "name": h["name"],
                        "type": h["type"][0] if h.get("type") else "public"
                    }
                    for h in data["response"]["holidays"]
                ]
        except Exception as e:
            print(f"❌ Calendarific failed: {e}")
        
        return None
    
    def _generate_fallback_holidays(self, year: int) -> List[Dict]:
        """Generiert Feiertage aus manueller Liste."""
        holidays = []
        
        for date_str, name in self.fallback_holidays.items():
            date = f"{year}-{date_str}"
            holidays.append({
                "date": date,
                "name": name,
                "type": "public"
            })
        
        return holidays
    
    def is_holiday(self, date: datetime) -> bool:
        """Prüft ob Datum ein Feiertag ist."""
        year = date.year
        holidays = self.get_holidays(year)
        
        date_str = date.strftime("%Y-%m-%d")
        return any(h["date"] == date_str for h in holidays)
    
    def get_features(self, date: datetime) -> Dict[str, float]:
        """
        Generiert Features für ein Datum.
        
        Args:
            date: Datum für Features
            
        Returns:
            {
                'is_holiday': 1/0,
                'days_to_next_holiday': int,
                'days_since_last_holiday': int,
                'is_holiday_week': 1/0
            }
        """
        holidays = self.get_holidays(date.year)
        holiday_dates = [datetime.strptime(h["date"], "%Y-%m-%d") for h in holidays]
        
        is_holiday = self.is_holiday(date)
        
        # Nächster Feiertag
        future_holidays = [h for h in holiday_dates if h >= date]
        days_to_next = (future_holidays[0] - date).days if future_holidays else 365
        
        # Letzter Feiertag
        past_holidays = [h for h in holiday_dates if h <= date]
        days_since_last = (date - past_holidays[-1]).days if past_holidays else 365
        
        # Holiday Week (7 Tage vor/nach Feiertag)
        is_holiday_week = days_to_next <= 7 or days_since_last <= 7
        
        return {
            'is_holiday': float(is_holiday),
            'days_to_next_holiday': float(days_to_next),
            'days_since_last_holiday': float(days_since_last),
            'is_holiday_week': float(is_holiday_week)
        }

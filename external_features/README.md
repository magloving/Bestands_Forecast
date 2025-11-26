# External Features API

Saubere, wiederverwendbare API Clients für Time Series Forecasting.

## 📁 Struktur

```
external_features/
├── __init__.py                 # Package Exports
├── base_client.py              # Base Client (Caching, Rate Limiting, Retry)
├── holiday_client.py           # Feiertags-API (Nager.Date, Calendarific)
├── bundesbank_client.py        # Deutsche Bundesbank API (EZB Zinsen)
├── orchestrator.py             # Koordiniert alle APIs
└── README.md                   # Diese Datei
```

## 🚀 Quick Start

### Installation

```bash
pip install requests pandas numpy
```

### Verwendung im Notebook

```python
from external_features import ExternalFeatureOrchestrator
from datetime import datetime

# Initialize Orchestrator
orchestrator = ExternalFeatureOrchestrator(country_code="DE")

# Get features for a single date
features = orchestrator.get_features_for_date(datetime(2025, 12, 25))
print(features)

# Get features for a date range (batch optimized)
df = orchestrator.get_features_for_range(
    datetime(2025, 12, 1),
    datetime(2025, 12, 31)
)
print(df.head())
```

### Verwendung einzelner Clients

```python
from external_features import HolidayAPIClient, BundesbankAPIClient

# Holiday Client
holiday_client = HolidayAPIClient(country_code="DE")
holidays = holiday_client.get_holidays(2025)
print(f"Feiertage 2025: {len(holidays)}")

# Bundesbank Client
bundesbank_client = BundesbankAPIClient()
rates = bundesbank_client.get_interest_rates(
    datetime(2025, 1, 1),
    datetime(2025, 12, 31)
)
print(rates.head())
```

## 📊 Verfügbare Features

### Holiday Features
- `is_holiday`: Ist heute ein Feiertag? (1/0)
- `days_to_next_holiday`: Tage bis nächster Feiertag
- `days_since_last_holiday`: Tage seit letztem Feiertag
- `is_holiday_week`: In Feiertagswoche? (±7 Tage)

### Interest Rate Features
- `ezb_hauptrefinanzierung`: EZB Leitzins
- `bundesanleihe_10j`: 10-Jahres Bundesanleihe Rendite
- `geldmarktzins_3m`: 3-Monats Euribor
- `rate_trend_7d`: Zinsänderung letzte 7 Tage
- `rate_trend_30d`: Zinsänderung letzte 30 Tage
- `rate_volatility`: Zinsvolatilität (Std 30 Tage)

### Zeitbasierte Features
- `day_of_week`: Wochentag (0=Montag)
- `day_of_month`: Tag im Monat (1-31)
- `month`: Monat (1-12)
- `quarter`: Quartal (1-4)
- `is_weekend`: Ist Wochenende? (1/0)
- `is_month_start`: Monatsanfang? (Tag 1-7)
- `is_month_end`: Monatsende? (Tag 24-31)
- `week_of_year`: Kalenderwoche (1-52)

## 🔧 Konfiguration

### Cache Settings

```python
from external_features import HolidayAPIClient

# Custom Cache Settings
client = HolidayAPIClient(
    cache_dir="./my_cache",
    cache_ttl_hours=48  # 48 Stunden statt 24
)

# Cache Stats
stats = client.get_cache_stats()
print(stats)

# Clear Cache
client.clear_cache()
```

### API Keys (Optional)

```python
# Calendarific Fallback (optional)
from external_features import HolidayAPIClient

client = HolidayAPIClient(
    country_code="DE",
    api_key="your_calendarific_key"
)
```

## 🏗️ Architektur

### Base Client Pattern

Alle API Clients erben von `FeatureAPIClient`:

- ✅ File-based Caching (TTL 24h)
- ✅ Rate Limiting (60 req/min default)
- ✅ Retry Logic (3 Versuche, Exponential Backoff)
- ✅ Fehlerbehandlung mit Fallbacks

### Multi-Provider Strategy

Jeder Client hat mehrere Provider:

1. **Primary API** (kostenlos, unbegrenzt)
2. **Secondary API** (Fallback mit API Key)
3. **Local Fallback** (Mock-Daten)

→ System läuft IMMER, auch ohne Internet!

## 🧪 Testing

```python
# Test mit Mock-Daten (kein Internet nötig)
from external_features import ExternalFeatureOrchestrator

orchestrator = ExternalFeatureOrchestrator()

# Funktioniert sofort ohne API Keys
df = orchestrator.get_features_for_range(
    datetime(2025, 12, 1),
    datetime(2025, 12, 31)
)

assert len(df) == 31  # 31 Tage Dezember
assert 'is_holiday' in df.columns
assert 'ezb_hauptrefinanzierung' in df.columns
```

## 🚀 Performance

### Batch Fetching

```python
# ❌ SCHLECHT: 30 einzelne API Calls
for date in dates:
    features = orchestrator.get_features_for_date(date)

# ✅ GUT: 1-2 Batch Calls für 30 Tage
df = orchestrator.get_features_for_range(start_date, end_date)
```

### Caching

- Erste Anfrage: ~2-3 Sekunden (API Calls)
- Zweite Anfrage: ~10ms (Cache Hit)
- TTL: 24 Stunden (konfigurierbar)

## 🔒 Security

- ✅ Keine API Keys in Code
- ✅ `.env` für Credentials
- ✅ Cache in `.gitignore`
- ✅ HTTPS für alle API Calls

## 📞 Support

Bei Problemen:
1. Check Cache: `client.get_cache_stats()`
2. Clear Cache: `client.clear_cache()`
3. Fallback prüfen: Mock-Daten sollten immer funktionieren

## 📝 License

MIT - Free for Research & Commercial Use

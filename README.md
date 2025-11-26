# 📊 Bestands Forecast - Retail Inventory Forecasting

**Production-ready Time Series Forecasting mit DeepAR & External Features**

---

## 🎯 Projekt-Übersicht

Probabilistisches Forecasting von Produktbeständen für Retail Stores mit:
- **DeepAR Model**: Konfidenzintervalle & Unsicherheitsschätzung
- **External Features**: Feiertage, Zinsen, Wirtschaftsindikatoren
- **Hybrid Data Strategy**: Development-Cache + Production-Snapshots

---

## 📁 Projekt-Struktur

```
Bestands_Forecast/
├── data/                           # 📊 Finale Datasets (IN GIT!)
│   ├── retail_store_inventory.csv      # Rohdaten
│   ├── external_features_training.csv  # Feature-Snapshot Training
│   └── external_features_test.csv      # Feature-Snapshot Test
│
├── cache/                          # 💾 Temporäre API-Caches (NICHT in Git)
│   ├── holidays_DE_2024.json
│   └── bundesbank_rates_*.json
│
├── models/                         # 🤖 Trained Models (optional in Git)
│   ├── deepar_final.keras
│   └── scalers.pkl
│
├── external_features/              # 🔌 Feature API Package
│   ├── __init__.py
│   ├── base_client.py                  # Cache, Rate Limiting, Retry
│   ├── holiday_client.py               # Feiertags-API
│   ├── bundesbank_client.py            # Deutsche Bundesbank API
│   ├── orchestrator.py                 # Koordiniert alle APIs
│   ├── data_manager.py                 # Hybrid-Strategie Manager
│   └── README.md
│
├── Umsatz_Forecast_DeepAR.ipynb    # 📓 Hauptnotebook
├── requirements.txt                 # 📦 Dependencies
├── .gitignore                       # 🚫 Git-Ausschlüsse
└── README.md                        # 📖 Diese Datei
```

---

## 🚀 Quick Start

### 1. Setup

```bash
# Clone Repository
git clone https://github.com/magloving/Bestands_Forecast.git
cd Bestands_Forecast

# Virtual Environment (empfohlen)
python -m venv venv
source venv/bin/activate  # macOS/Linux
# oder: venv\Scripts\activate  # Windows

# Dependencies installieren
pip install -r requirements.txt
```

### 2. Notebook starten

```bash
jupyter notebook Umsatz_Forecast_DeepAR.ipynb
```

### 3. External Features nutzen

```python
from external_features import ExternalFeatureOrchestrator, FeatureDataManager
from datetime import datetime

# Orchestrator initialisieren
orchestrator = ExternalFeatureOrchestrator(country_code="DE")

# Features abrufen (wird automatisch gecacht!)
df_features = orchestrator.get_features_for_range(
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 12, 31)
)

# Finales Training-Dataset exportieren
data_manager = FeatureDataManager()
data_manager.export_training_snapshot(
    features_df=df_features,
    name="training_2024"
)
```

---

## 💾 Hybrid Data Strategy

**Best Practice für ML Projects:**

### Development Phase
```python
# ✅ Automatisches Caching (schnell, flexibel)
df = orchestrator.get_features_for_range(...)
# → Speichert in cache/ (24h TTL)
# → Kein CSV nötig
# → Perfekt für Experimente
```

### Production Phase
```python
# ✅ Finale CSV-Snapshots (reproduzierbar, versioniert)
data_manager.export_training_snapshot(
    features_df=df,
    name="training_2024"
)
# → Speichert in data/external_features_training_2024.csv
# → UNVERÄNDERLICH (nie wieder geändert)
# → Git commit für Reproduzierbarkeit
```

### Vorteile
| Phase | Speicher | Zweck | Git |
|-------|----------|-------|-----|
| Development | `cache/` | Schnelle Iteration | ❌ |
| Training | `data/*.csv` | Reproduzierbare Snapshots | ✅ |
| Production | `cache/` | Live-Predictions | ❌ |

---

## 🔌 External Features API

### Verfügbare Clients

**1. HolidayAPIClient**
- Feiertage für Deutschland
- 3-Layer Fallback (Nager.Date → Calendarific → Local)
- Features: `is_holiday`, `days_to_next_holiday`, `is_holiday_week`

**2. BundesbankAPIClient**
- Deutsche Bundesbank API (keine API Key!)
- EZB Zinsen, Bundesanleihen, Inflation
- Features: `ecb_main_rate`, `german_10y_yield`, `inflation_rate`

**3. ExternalFeatureOrchestrator**
- Koordiniert alle APIs
- Automatisches Caching (24h TTL)
- Batch-Abruf für Datumsbereiche

### Beispiel

```python
orchestrator = ExternalFeatureOrchestrator(country_code="DE")

# Einzelnes Datum
features = orchestrator.get_features_for_date(datetime(2025, 12, 25))

# Datumsbereich (batch)
df_features = orchestrator.get_features_for_range(
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 12, 31)
)

# Feature-Namen
feature_names = orchestrator.get_feature_names()
# → ['is_holiday', 'days_to_next_holiday', 'is_holiday_week',
#    'ezb_hauptrefinanzierung', 'bundesanleihe_10j', ...]
```

---

## 🤖 DeepAR Model

**Probabilistisches Forecasting mit Konfidenzintervallen**

- **Input**: 60-Tage Sequenzen + External Features
- **Output**: μ (Mittelwert) + σ (Standardabweichung)
- **Loss**: Gaussian Negative Log-Likelihood
- **Architektur**: 2-Layer Bidirectional LSTM (256→128 Units)

### Performance
```
MAE:      89.41 Units
Std:      109.77 Units (gut kalibriert!)
Coverage: 86.6% (90% Prediction Intervals)
```

---

## 📊 Workflow

```
┌──────────────────────────────────────────────────────────────┐
│ 1. DEVELOPMENT                                               │
├──────────────────────────────────────────────────────────────┤
│ • Nutze cache/ für schnelle Iteration                       │
│ • Experimentiere mit Features                                │
│ • Kein Git commit nötig                                      │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ 2. FINAL TRAINING                                            │
├──────────────────────────────────────────────────────────────┤
│ • Exportiere CSV-Snapshots (data/)                           │
│ • Git commit für Reproduzierbarkeit                          │
│ • Trainiere finales Model                                    │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ 3. PRODUCTION                                                │
├──────────────────────────────────────────────────────────────┤
│ • Nutze cache/ für neue Predictions                          │
│ • Live-Daten automatisch gecacht                             │
│ • Optional: Neue Snapshots für neue Zeiträume                │
└──────────────────────────────────────────────────────────────┘
```

---

## 📦 Dependencies

- **Core**: numpy, pandas, scipy
- **ML**: tensorflow, scikit-learn
- **Viz**: matplotlib, seaborn
- **API**: requests
- **Dev**: jupyter, notebook

Siehe `requirements.txt` für Details.

---

## 🔧 Configuration

### .env (optional)
```bash
# API Keys (nur wenn du NICHT Mock-Daten nutzen willst)
CALENDARIFIC_API_KEY=your_key_here
```

### .gitignore
```gitignore
# Temporär (nicht committen)
cache/
*.pkl
models/*.keras

# Daten (committen wenn < 10 MB)
!data/retail_store_inventory.csv
!data/external_features_*.csv
```

---

## 🎓 Use Cases

### Studium / Thesis
- ✅ Reproduzierbare Experimente (CSV-Snapshots)
- ✅ Klare Versionierung (Git)
- ✅ Dokumentation (README, Docstrings)

### Production Deployment
- ✅ Live-Predictions (Cache)
- ✅ API-Integration (external_features Package)
- ✅ Monitoring-ready (Logging, Fallbacks)

### Team Collaboration
- ✅ Geteilte Datasets (data/ in Git)
- ✅ Saubere Struktur (modular)
- ✅ Dependencies fixiert (requirements.txt)

---

## 📚 Dokumentation

- **External Features API**: `external_features/README.md`
- **API Setup Guide**: `API_SETUP_GUIDE.md`
- **Notebook**: `Umsatz_Forecast_DeepAR.ipynb` (vollständig dokumentiert)

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork Repository
2. Create Feature Branch (`git checkout -b feature/amazing-feature`)
3. Commit Changes (`git commit -m 'Add amazing feature'`)
4. Push to Branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

MIT License - siehe LICENSE Datei

---

## 👤 Author

**Magnus**
- GitHub: [@magloving](https://github.com/magloving)
- Repository: [Bestands_Forecast](https://github.com/magloving/Bestands_Forecast)

---

## 🙏 Acknowledgments

- **Deutsche Bundesbank**: Kostenlose Wirtschaftsdaten API
- **Nager.Date**: Kostenlose Feiertags-API
- **TensorFlow/Keras**: Deep Learning Framework
- **DeepAR Paper**: Salinas et al. (2020)

---

**🚀 Happy Forecasting!**

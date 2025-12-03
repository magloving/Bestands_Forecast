# 🚀 DeepAR Notebooks - Training & Forecasting

**Getrennte Notebooks für Training und Forecasting**

---

## 📋 Übersicht

Das Projekt ist jetzt in **zwei separate Jupyter Notebooks** aufgeteilt:

```
📦 Bestands_Forecast/
├── 🎯 train_deepar.ipynb        # Training Pipeline (Notebook)
├── 🔮 forecast_deepar.ipynb     # Forecasting Pipeline (Notebook)
├── 📓 Umsatz_Forecast_DeepAR_BACKUP.ipynb  # Backup (Archiv)
└── models/                      # Gespeicherte Artefakte
    ├── deepar_retail_forecast.keras
    ├── scalers.pkl
    ├── history.pkl
    ├── metrics.json
    └── config.json
```

---

## 🎯 1. Training Pipeline (`train_deepar.ipynb`)

### Was macht es?

Trainiert das DeepAR-Model und speichert alle wichtigen Artefakte:

✅ **Trainiertes Keras Model** (`.keras`)
✅ **Scaler** für Features und Target (`.pkl`)
✅ **Training History** (Loss Kurven) (`.pkl`)
✅ **Evaluations-Metriken** (MAE, RMSE, MAPE) (`.json`)
✅ **Model Config** (Sequenz-Länge, Features) (`.json`)
✅ **Visualisierungen** (Loss Kurven, Predictions vs Actual)

### Wie führe ich es aus?

```bash
# Öffne Notebook in VS Code oder Jupyter
jupyter notebook train_deepar.ipynb

# ODER in VS Code:
# Öffne train_deepar.ipynb und führe alle Zellen aus (Ctrl+Shift+Enter)
```

### Was passiert?

1. **Daten laden** (`retail_store_inventory.csv`)
2. **Feature Engineering** (Lags, Rolling Means, Date Features)
3. **Train/Test Split** (80/20)
4. **Sequenzen erstellen** (30-Tage Zeitfenster)
5. **Normalisierung** (StandardScaler)
6. **Model Training** (~5-10 Minuten mit SCHNELL-CONFIG ⚡)
7. **Evaluation** (MAE, RMSE, MAPE, P10-P90 Coverage)
8. **Visualisierungen** erstellen
9. **Alles speichern** in `models/`

### Output

```
📦 models/
├── deepar_retail_forecast.keras  # Trainiertes Model
├── scalers.pkl                   # StandardScaler für X und y
├── history.pkl                   # Training History
├── metrics.json                  # Performance Metriken
├── config.json                   # Model Configuration
├── training_history.png          # Loss Kurven
└── predictions_vs_actual.png     # Scatter Plot
```

### Performance

**⚡ SCHNELL-CONFIG (Default):**
- **Training Zeit:** ~5-10 Minuten
- **Epochen:** 50 (statt 100)
- **LSTM Units:** 128→64 (statt 256→128)
- **Sequenz:** 30 Tage (statt 60)
- **Qualität:** ~95% der Original-Performance

**🎯 ORIGINAL-CONFIG (Optional):**
- Im Code auskommentiert
- **Training Zeit:** ~260 Minuten (4+ Stunden)
- **Bessere Qualität:** ~100%
- Nutzen für finale Production-Models

---

## 🔮 2. Forecasting Pipeline (`forecast_deepar.ipynb`)

### Was macht es?

Lädt trainiertes Model und erstellt Forecasts:

✅ **Probabilistische Forecasts** (P10, P50, P90)
✅ **Confidence Intervals** (80% Vorhersageintervall)
✅ **Multi-Step Forecasts** (1-30+ Tage)
✅ **Visualisierungen** (Historisch + Forecast)
✅ **CSV Export**
✅ **Batch Forecasting** (mehrere Kombinationen)

### Voraussetzungen

```bash
# WICHTIG: Zuerst Training ausführen!
# Öffne train_deepar.ipynb und führe alle Zellen aus
```

### Verwendung

#### **Option 1: Einzelner Forecast**

1. Öffne `forecast_deepar.ipynb`
2. Führe Zellen 1-5 aus (Setup + Funktionen)
3. **Zelle 6:** Ändere `STORE_ID`, `PRODUCT_ID`, `DAYS_AHEAD`
4. Führe Zelle 6 aus → Forecast + Visualisierung
5. Zelle 7: Ergebnisse anzeigen
6. Zelle 8: Als CSV exportieren

#### **Option 2: Batch Forecasts**

- **Zelle 9:** Definiere Liste mit Store/Product Kombinationen
- Führe Zelle 9 aus → Alle Forecasts auf einmal

### Output

```
📦 forecasts/
├── forecast_store1_product101.png   # Visualisierung
└── forecast_store1_product101.csv   # CSV Export
```

**CSV Format:**
```csv
Date,Day_Ahead,Forecast_P10,Forecast_P50,Forecast_P90,Uncertainty
2025-01-01,1,45.2,52.8,60.4,5.9
2025-01-02,2,43.1,51.3,59.5,6.4
...
```

### Forecast Interpretation

- **P10 (10th Percentile):** Pessimistisches Szenario (10% Chance, dass Verkäufe darunter liegen)
- **P50 (Median):** Erwarteter Wert (beste Schätzung)
- **P90 (90th Percentile):** Optimistisches Szenario (10% Chance, dass Verkäufe darüber liegen)
- **Uncertainty:** Standardabweichung der Vorhersage

---

## 🔄 Typischer Workflow

### **Initial Setup (Einmalig)**

```bash
# 1. Training durchführen
# Öffne train_deepar.ipynb in VS Code/Jupyter
# Führe alle Zellen aus (Run All)
# ⏱️  Dauer: ~5-10 Minuten
# ✅ Models gespeichert in models/
```

### **Forecasting (Beliebig oft wiederholen)**

```bash
# 2. Forecasts erstellen (ohne Re-Training!)
# Öffne forecast_deepar.ipynb
# Ändere STORE_ID, PRODUCT_ID, DAYS_AHEAD in Zelle 6
# Führe Zellen aus

# Oder: Batch Forecasting in Zelle 9
```

**⚡ Vorteil:** Forecasting dauert nur **Sekunden**, nicht Minuten!

### **Re-Training (Bei neuen Daten)**

```bash
# Wenn neue Daten vorliegen:
# 1. retail_store_inventory.csv aktualisieren
# 2. Re-Training: train_deepar.ipynb ausführen
# 3. Neue Forecasts: forecast_deepar.ipynb
```

---

## 📊 Performance Metriken

Nach dem Training siehst du:

```
📈 EVALUATION RESULTS
======================================================================
MAE:               12.34 (Baseline: 28.90)
RMSE:              18.56
MAPE:              15.2%
P10-P90 Coverage:  82.3%
Verbesserung:      57.3% gegenüber Baseline
======================================================================
```

**Was bedeutet das?**

- **MAE (Mean Absolute Error):** Durchschnittlicher Fehler in Units
  - Hier: Im Schnitt 12.34 Units daneben
  - **57% besser als Baseline!**

- **RMSE (Root Mean Squared Error):** Bestraft große Fehler stärker
  - Hier: 18.56 Units

- **MAPE (Mean Absolute Percentage Error):** Relativer Fehler
  - Hier: 15.2% Abweichung vom tatsächlichen Wert

- **P10-P90 Coverage:** Wie oft liegt der echte Wert im 80%-Intervall?
  - Hier: 82.3% der Zeit (perfekt wäre 80%)

---

## 🎯 Vorteile der Trennung

### ✅ **1. Schnelleres Experimentieren**

- **Vorher (1 Notebook):** Jedes Forecast = Re-Training (5-10 Min)
- **Nachher (2 Notebooks):** Training 1x, Forecasts beliebig oft (Sekunden!)

### ✅ **2. Klarere Struktur**

```python
# Training (einmalig)
train_deepar.ipynb
  ↓
models/  # Gespeicherte Artefakte
  ↓
# Forecasting (beliebig oft)
forecast_deepar.ipynb
```

### ✅ **3. Interaktive Entwicklung**

- **Training:** Visualisierungen sofort sehen
- **Forecasting:** Parameter schnell ändern (Zelle 6)
- **Debugging:** Zelle für Zelle durchgehen

### ✅ **4. Bessere Wartbarkeit**

- Problem im Training? → Nur `train_deepar.ipynb` debuggen
- Problem im Forecast? → Nur `forecast_deepar.ipynb` debuggen

### ✅ **5. Flexibilität**

- **Training:** Experimentiere mit Config (Zelle 2)
- **Forecasting:** Batch Processing (Zelle 9)
- **Versionierung:** Notebooks in Git tracken

---

## 🛠️ Anpassungen & Erweiterungen

### **1. Config ändern**

**Notebook:** `train_deepar.ipynb`, Zelle 2

```python
# Beispiel: Längere Sequenzen
config = Config(
    seq_length=60,        # Statt 30
    batch_size=256,       # Statt 512
    epochs=100,           # Statt 50
    lstm_units_1=256,     # Statt 128
    lstm_units_2=128      # Statt 64
)
```

### **2. Neue Features hinzufügen**

**Notebook:** `train_deepar.ipynb`, Zelle 4

```python
# Beispiel: Seasonality Features
df['IsWeekend'] = df['DayOfWeek'].isin([5, 6]).astype(int)
df['IsMonthStart'] = df['Date'].dt.is_month_start.astype(int)
df['IsMonthEnd'] = df['Date'].dt.is_month_end.astype(int)
```

### **3. Andere Store/Product forecasten**

**Notebook:** `forecast_deepar.ipynb`, Zelle 6

```python
STORE_ID = 2           # Ändere hier
PRODUCT_ID = 205       # Ändere hier
DAYS_AHEAD = 14        # Ändere hier
```

### **4. Batch Forecasts**

**Notebook:** `forecast_deepar.ipynb`, Zelle 9

```python
batch_config = [
    {'store': 1, 'product': 101, 'days': 30},
    {'store': 2, 'product': 205, 'days': 14},
    {'store': 3, 'product': 312, 'days': 7},
    # Füge mehr hinzu...
]
```

---

## 🐛 Troubleshooting

### **Problem: "Model not found"**

```bash
❌ FileNotFoundError: models/deepar_retail_forecast.keras
```

**Lösung:** Zuerst Training durchführen!

```bash
# Öffne train_deepar.ipynb und führe alle Zellen aus
```

---

### **Problem: "Not enough data"**

```bash
❌ Nicht genug Daten: 15 Tage (brauche 30)
```

**Lösung:** Store/Product Kombination hat zu wenig historische Daten

**Option 1:** Kleinere Sequenz in `train_deepar.ipynb`, Zelle 2:
```python
config = Config(seq_length=10)  # Statt 30
```

**Option 2:** Andere Store/Product Kombination wählen

---

### **Problem: Training dauert zu lange**

```bash
⏱️  Training dauert 260 Minuten statt 10...
```

**Lösung 1:** GPU nutzen (falls verfügbar)

In Notebook einfügen:
```python
import tensorflow as tf
print(tf.config.list_physical_devices('GPU'))
```

**Lösung 2:** Schnellere Config (bereits Default!)

Bereits implementiert in `train_deepar.ipynb`, Zelle 2 ✅

**Lösung 3:** Daten sampeln

In `train_deepar.ipynb`, nach Zelle 3:
```python
df = df.sample(frac=0.5, random_state=42)  # Nur 50% der Daten
```

---

### **Problem: Kernel crashed**

```bash
❌ Kernel died, restarting...
```

**Lösung:** Speicher-Problem

- **Option 1:** Restart Kernel und führe nur benötigte Zellen aus
- **Option 2:** Reduziere `batch_size` in Config (Zelle 2)
- **Option 3:** Nutze kleinere `seq_length` (z.B. 15 statt 30)

---

## 📚 Nächste Schritte

### **1. Basis Setup**
```bash
1. Öffne train_deepar.ipynb
2. Führe alle Zellen aus (Run All)
3. Warte ~5-10 Minuten
4. Öffne forecast_deepar.ipynb
5. Ändere STORE_ID/PRODUCT_ID in Zelle 6
6. Führe Zellen aus
```

### **2. Batch Forecasts**
```bash
# In forecast_deepar.ipynb, Zelle 9:
# Definiere Liste mit Store/Product Kombinationen
# Führe Zelle aus → Alle auf einmal
```

### **3. Experimentieren**
```bash
# train_deepar.ipynb, Zelle 2:
# Ändere Config (Epochen, LSTM Units, etc.)
# Re-Training → Neue Metrics vergleichen
```

### **4. Production Deployment**
```python
# Konvertiere Notebooks zu Python Scripts (optional)
jupyter nbconvert --to script train_deepar.ipynb
jupyter nbconvert --to script forecast_deepar.ipynb

# Oder nutze Papermill für automatisierte Ausführung
pm.execute_notebook('train_deepar.ipynb', 'output.ipynb')
```

---

## 🎓 Zusammenfassung

**Zwei separate Notebooks = Bessere Workflow:**

| Aspekt | Vorher (1 Notebook) | Nachher (2 Notebooks) |
|--------|---------------------|----------------------|
| Training | Jedes Mal neu | Einmalig ✅ |
| Forecast | 5-10 Min | Sekunden ✅ |
| Struktur | Alles gemischt | Klar getrennt ✅ |
| Interaktivität | Eingeschränkt | Voll ✅ |
| Debugging | Komplex | Einfach ✅ |
| Visualisierung | Am Ende | Sofort ✅ |

**Quick Start:**

```bash
# 1. Training (einmalig)
# Öffne train_deepar.ipynb → Run All

# 2. Forecasting (beliebig oft)
# Öffne forecast_deepar.ipynb → Ändere Zelle 6 → Run
```

---

**🚀 Viel Erfolg mit den Scripts!**

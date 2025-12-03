# 🔄 AUSFÜHRUNGSREIHENFOLGE

**Letzte Aktualisierung:** 26. November 2025

---

## 🚀 EMPFOHLEN: Python Scripts (Getrennt)

**✨ Neu ab Version 2.0:** Training und Forecasting sind jetzt in separate Python-Dateien aufgeteilt!

### **Vorteile der Trennung:**
✅ **Training nur 1x** (nicht bei jedem Forecast wiederholen)
✅ **Forecasting in Sekunden** (statt Minuten)
✅ **Klarere Struktur** (Training ≠ Forecasting)
✅ **Production-Ready** (API, Cron-Jobs, Batch Processing)
✅ **Besseres Debugging** (isolierte Probleme)

### **Quick Start:**

```bash
# 1. Training (einmalig, ~5-10 Minuten ⚡)
python train_deepar.py

# 2. Forecasting (beliebig oft, Sekunden!)
python forecast_deepar.py

# Oder direkt mit Parametern:
python forecast_deepar.py --store 1 --product 101 --days 30
```

**📖 Detaillierte Anleitung:** Siehe `README_SCRIPTS.md`

---

## 📓 ALTERNATIV: Jupyter Notebook

Falls du lieber im Notebook arbeiten möchtest:

## 📋 INHALT

1. [Workflow 1: DeepAR Model Training (Komplett)](#workflow-1-deepar-model-training)
2. [Workflow 2: Hybrid-Strategie testen (External Features)](#workflow-2-hybrid-strategie-testen)
3. [Troubleshooting](#troubleshooting)

---

## 🎯 WORKFLOW 1: DeepAR Model Training

**Ziel:** Komplettes Training des probabilistischen Forecasting-Modells

### Phase 1: Setup & Daten laden (5 Minuten)

| Zelle | Inhalt | Was passiert | Wichtig |
|-------|--------|--------------|---------|
| **2** | Imports | Lädt numpy, pandas, tensorflow, etc. | ⚠️ Fehler? `pip install -r requirements.txt` |
| **3** | Config | Definiert alle Hyperparameter | ✏️ Anpassbar für Experimente |
| **5** | Daten laden | Liest `retail_store_inventory.csv` | ✅ Zeigt Datensatz-Info |
| **7** | Temporal Features | Erstellt Zeitfeatures (day_of_week, month, etc.) | 📅 Essential für Patterns |
| **9** | Feature Engineering | Lag, Rolling Mean, Diff Features | 🔬 Feature-Matrix |

**Checkpoint:** Du solltest jetzt einen DataFrame mit ~30 Features haben.

---

### Phase 2: Daten vorbereiten (2 Minuten)

| Zelle | Inhalt | Was passiert | Output |
|-------|--------|--------------|--------|
| **11** | Train/Test Split | Zeitbasiert: Letzte 20% = Test | 📊 Train/Test Shapes |
| **13** | Scaling | StandardScaler auf Features & Target | ⚖️ Mean=0, Std=1 |
| **16** | Sequences | Erstellt 60-Tage Sequenzen | 🔢 (samples, 60, features) |

**Checkpoint:** 
- Train: ~80% der Daten
- Test: ~20% der Daten
- Shape: (n_samples, 60, n_features)

---

### Phase 3: EDA & Model Building (2 Minuten)

| Zelle | Inhalt | Was passiert | Output |
|-------|--------|--------------|--------|
| **18** | EDA & Stats | Visualisierungen, Statistiken | 📈 Plots & Metriken |
| **21** | Model definieren | DeepAR Architektur (2-Layer LSTM) | 🏗️ Model Summary |
| **22** | Model kompilieren | Gaussian NLL Loss | ⚙️ Optimizer: Adam |

**Checkpoint:** Model Summary sollte ~2-3M Parameter zeigen.

---

### Phase 4: Training & Evaluation (5-10 Minuten)

| Zelle | Inhalt | Was passiert | Dauer |
|-------|--------|--------------|-------|
| **24** | Training | Model trainieren mit EarlyStopping | ⏱️ 5-10 Min |
| **26** | Predictions | Vorhersagen auf Test-Set | 📊 μ & σ |
| **27** | Evaluation | MAE, Coverage, Plots | 📈 Visualisierungen |

**Checkpoint:** 
- **MAE:** ~89.41 (Ziel: < 90)
- **Std:** ~109.77 (gut kalibriert!)
- **Coverage:** ~86.6% (Ziel: ~90%)

---

### ✅ Workflow 1 Complete!

**Was du jetzt hast:**
- ✅ Trainiertes DeepAR Model
- ✅ Predictions mit Konfidenzintervallen
- ✅ Evaluation Metriken
- ✅ Visualisierungen

**Nächste Schritte:**
- Experimentiere mit Hyperparametern (Zelle 3)
- Teste verschiedene Features
- Integriere External Features (Workflow 2)

---

## 🚀 WORKFLOW 2: Hybrid-Strategie testen

**Ziel:** External Features API testen & CSV-Snapshots erstellen

### Quick Setup (1 Minute)

| Zelle | Inhalt | Was passiert | Output |
|-------|--------|--------------|--------|
| **51** | Setup | Ordner erstellen, Manager initialisieren | 📁 data/, cache/, models/ |

**Checkpoint:** Ordnerstruktur sollte existieren.

---

### Phase 1: Development mit Cache (1 Minute)

| Zelle | Inhalt | Was passiert | Output |
|-------|--------|--------------|--------|
| **52** | Cache Test | API-Call → automatisches Caching | 📂 cache/ Dateien |

**Was du siehst:**
```
✅ Features abgerufen: (365, 18)
📂 Cache: 
   - holidays_DE_2024.json
   - bundesbank_rates_2024.json
```

**Wichtig:** 
- Erster Call = API-Request (langsam)
- Zweiter Call (< 24h) = Cache (instant!)

---

### Phase 2: Training Snapshot erstellen (30 Sekunden)

| Zelle | Inhalt | Was passiert | Output |
|-------|--------|--------------|--------|
| **53** | Training Snapshot | CSV exportieren (EINMALIG!) | 💾 data/external_features_training_2024.csv |

**Was du siehst:**
```
✅ SNAPSHOT EXPORTIERT
Datei:     data/external_features_training_2024.csv
Shape:     (365, 18)
Größe:     45.2 KB
Zeitraum:  2024-01-01 bis 2024-12-31

💡 Nächste Schritte:
   1. git add data/external_features_training_2024.csv
   2. git commit -m 'Add training feature snapshot'
   3. git push origin main
```

**Wichtig:** Diese CSV wird **NIE** mehr geändert! (Immutable Snapshot)

---

### Phase 3: Test Snapshot (Optional, 30 Sekunden)

| Zelle | Inhalt | Was passiert | Output |
|-------|--------|--------------|--------|
| **54** | Test Snapshot | Zweiter Snapshot für Test-Set | 💾 data/external_features_test_2025_H1.csv |

**Checkpoint:** Du hast jetzt 2 unveränderliche Snapshots.

---

### Phase 4: Übersicht & Kombinieren (1 Minute)

| Zelle | Inhalt | Was passiert | Output |
|-------|--------|--------------|--------|
| **55** | Snapshot Info | Zeigt alle verfügbaren Snapshots | 📊 Liste + Stats |
| **56** | Kombiniertes Dataset | Merged Retail + Features | 💾 data/training_dataset_complete.csv |

**Was du siehst:**
```
✅ KOMBINIERTES DATASET:
   Retail Rows:    10,000
   Features Rows:  365
   Combined Rows:  10,000
   Combined Cols:  35
```

---

### ✅ Workflow 2 Complete!

**Was du jetzt hast:**
- ✅ Funktionierendes API-Caching
- ✅ Training & Test Snapshots (unveränderlich)
- ✅ Kombiniertes Dataset ready für Training
- ✅ Git-ready Structure

**Nächste Schritte:**
```bash
# Git commit
git add data/external_features_*.csv
git commit -m "Add final feature snapshots"
git push origin main
```

---

## 📊 KOMBINIERTER WORKFLOW (Empfohlen)

**Bestes Vorgehen für Production-Training:**

### Schritt 1: Features vorbereiten (5 Minuten)
```
Zelle 51 → Setup
Zelle 52 → Cache Test (optional)
Zelle 53 → Training Snapshot erstellen
Zelle 54 → Test Snapshot erstellen (optional)
```

### Schritt 2: Model Training (10 Minuten)
```
Zelle 2  → Imports
Zelle 3  → Config
Zelle 5  → Daten laden (+ Features joinen!)
Zelle 7-13 → Preprocessing
Zelle 16 → Sequences
Zelle 21-22 → Model bauen
Zelle 24 → Training
Zelle 26-27 → Evaluation
```

### Schritt 3: Production Ready
```
Zelle 31-33 → Prediction Functions (neue Daten)
```

---

## 🔍 TROUBLESHOOTING

### Problem: ImportError

**Fehler:**
```
ModuleNotFoundError: No module named 'tensorflow'
```

**Lösung:**
```bash
pip install -r requirements.txt
```

---

### Problem: Cache-Verzeichnis fehlt

**Fehler:**
```
FileNotFoundError: [Errno 2] No such file or directory: './cache'
```

**Lösung:**
- Führe Zelle 51 (Setup) aus
- Oder manuell: `mkdir -p cache data models`

---

### Problem: retail_store_inventory.csv nicht gefunden

**Fehler:**
```
FileNotFoundError: retail_store_inventory.csv
```

**Lösung:**
- Check Dateiname: Muss exakt `retail_store_inventory.csv` heißen
- Check Pfad: Datei muss im Root-Verzeichnis sein
- Oder: Passe Pfad in Zelle 3 (Config) an

---

### Problem: API-Calls zu langsam

**Symptom:**
- Erster Call dauert 5-10 Sekunden

**Erklärung:**
- Das ist **normal**! API-Requests sind langsam
- Ab dem zweiten Call: **Instant aus Cache!**

**Lösung:**
- Einmal warten beim ersten Call
- Danach: Cache nutzt sich selbst

---

### Problem: Snapshot existiert bereits

**Fehler:**
```
FileExistsError: ❌ Snapshot existiert bereits
```

**Lösung:**
```python
# Option 1: Überschreiben
data_manager.export_training_snapshot(
    features_df=df,
    name="training_2024",
    overwrite=True  # ← Force overwrite
)

# Option 2: Anderen Namen wählen
data_manager.export_training_snapshot(
    features_df=df,
    name="training_2024_v2"  # ← Neue Version
)
```

---

### Problem: Git commit schlägt fehl

**Fehler:**
```
error: Your local changes to the following files would be overwritten
```

**Lösung:**
```bash
# Option 1: Stash changes
git stash
git pull
git stash pop

# Option 2: Force commit
git add -A
git commit -m "Update features"
git push origin main
```

---

## 📚 WEITERE RESOURCES

- **README.md**: Vollständige Projektdokumentation
- **external_features/README.md**: API-Dokumentation
- **requirements.txt**: Alle Dependencies

---

## 🎯 EMPFOHLENE REIHENFOLGE FÜR VERSCHIEDENE ZIELE

### 🎓 Für Studium/Thesis
```
1. Workflow 1: Model verstehen (Zelle 2-27)
2. Workflow 2: Features hinzufügen (Zelle 51-56)
3. Kombiniert trainieren
4. Snapshots committen für Reproduzierbarkeit
```

### 🚀 Für Production Deployment
```
1. Workflow 2: Features vorbereiten (Zelle 51-54)
2. Git commit Snapshots
3. Workflow 1: Training (Zelle 2-27)
4. Prediction Functions (Zelle 31-33)
5. Deployment (Docker, API, etc.)
```

### 🔬 Für Experimente
```
1. Zelle 51-52: Cache aktivieren
2. Zelle 2-3: Config anpassen
3. Zelle 5-27: Quick Training
4. Iterate! (nur Zelle 3 + 24 wiederholen)
```

---

**💡 Tipp:** Nutze "Run All Above" in Jupyter für schnelle Re-runs!

**🎉 Viel Erfolg mit deinem Forecasting-Projekt!**

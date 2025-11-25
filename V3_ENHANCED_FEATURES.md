# V3.0 - Enhanced Feature Engineering

## 🚀 Was wurde hinzugefügt?

### Neue Features: +25 zusätzliche Features

## 1. Kategoriale Features (6 neue)

| Feature | Werte | Encoding | Business Impact |
|---------|-------|----------|-----------------|
| **Category** | 5 (Groceries, Toys, Electronics, Clothing, Furniture) | `Category_Encoded` | Unterschiedliche Verkaufsmuster pro Kategorie |
| **Region** | 4 (North, South, East, West) | `Region_Encoded` | Regionale Unterschiede (Demografie, Klima) |
| **Weather** | 4 (Sunny, Cloudy, Rainy, Snowy) | `Weather_Encoded` | Wetterabhängige Produkte (Getränke, Kleidung) |
| **Seasonality** | 4 (Spring, Summer, Autumn, Winter) | `Seasonality_Encoded` | Explizite Saisonalität |

## 2. Preis & Wettbewerbs-Features (9 neue)

| Feature | Beschreibung | Formel | Impact |
|---------|--------------|--------|--------|
| **Price** | Eigener Preis | Direkt aus Daten | Preissensitivität |
| **Discount** | Rabatt in % | Direkt aus Daten | Promotions-Effekt |
| **Competitor_Price** | Konkurrenz-Preis | Direkt aus Daten | Wettbewerbsdruck |
| **Price_Diff** | Preisvorteil | `Price - Competitor_Price` | Relativer Wettbewerbsvorteil |
| **Price_Ratio** | Relatives Pricing | `Price / Competitor_Price` | Preis-Position |
| **Effective_Price** | Preis nach Rabatt | `Price * (1 - Discount/100)` | Echter Kundenpreis |
| **Has_Discount** | Rabatt aktiv? | Binary (0/1) | Promotion-Indikator |
| **Price_lag_1** | Gestrige Preise | Lag 1 Tag | Verzögerte Reaktion |
| **Discount_lag_1** | Gestriger Rabatt | Lag 1 Tag | Verzögerte Promotion-Wirkung |

**Erwarteter Impact:** 
- Erfasst Preis-Elastizität
- Modelliert Promotions-Effekte
- Berücksichtigt Wettbewerbssituation

## 3. Inventory Features (2 neue)

| Feature | Beschreibung | Impact |
|---------|--------------|--------|
| **Inventory_Level** | Aktueller Bestand | Verfügbarkeit beeinflusst Verkauf |
| **Inventory_lag_1** | Gestriger Bestand | Stockout-Historie |

**Erwarteter Impact:**
- Modelliert Stockout-Situationen (Bestand=0 → Units Sold sinkt)
- Erfasst Nachbestell-Dynamik

## 4. Event Features (1 neues)

| Feature | Beschreibung | Werte | Impact |
|---------|--------------|-------|--------|
| **Is_Holiday** | Holiday/Promotion Tag | Binary (0/1) | Event-Spitzen (Weihnachten, Black Friday) |

**Erwarteter Impact:**
- Erfasst Verkaufsspitzen an Feiertagen
- Modelliert Promotions-Perioden

## 5. Verbesserte Temporale Features (4 neue)

| Feature | Beschreibung | Formel | Vorteil |
|---------|--------------|--------|---------|
| **Month_sin** | Zyklischer Monat (Sinus) | `sin(2π * Month / 12)` | Dezember ≈ Januar |
| **Month_cos** | Zyklischer Monat (Kosinus) | `cos(2π * Month / 12)` | Kontinuität |
| **DayOfWeek_sin** | Zyklischer Wochentag (Sinus) | `sin(2π * DayOfWeek / 7)` | Sonntag ≈ Montag |
| **DayOfWeek_cos** | Zyklischer Wochentag (Kosinus) | `cos(2π * DayOfWeek / 7)` | Kontinuität |

**Warum zyklisches Encoding?**

❌ **Problem mit linearem Encoding:**
```
Monat: 1, 2, 3, ..., 11, 12
→ Model denkt: Dezember (12) ist weit weg von Januar (1)!
```

✅ **Lösung mit zyklischem Encoding:**
```
sin(2π * 12/12) ≈ sin(2π * 1/12)  → Ähnliche Werte!
cos(2π * 12/12) ≈ cos(2π * 1/12)
```

## 6. Rolling Price/Discount Features (2 neue)

| Feature | Beschreibung | Window | Impact |
|---------|--------------|--------|--------|
| **Price_rolling_mean_7** | Durchschnittspreis letzte 7 Tage | 7 Tage | Preistrend |
| **Discount_rolling_mean_7** | Durchschnittsrabatt letzte 7 Tage | 7 Tage | Promotions-Trend |

---

## 📊 Feature Vergleich: V2.0 vs V3.0

| Kategorie | V2.0 | V3.0 | Neu |
|-----------|------|------|-----|
| **Kategoriale** | 2 (Store, Product) | 8 | +6 |
| **Temporal** | 5 | 9 | +4 |
| **Price/Discount** | 0 | 9 | +9 |
| **Inventory** | 0 | 2 | +2 |
| **Events** | 0 | 1 | +1 |
| **Lag Units Sold** | 4 | 4 | 0 |
| **Rolling Units Sold** | 7 | 7 | 0 |
| **Lag Price/Inventory** | 0 | 3 | +3 |
| **Rolling Price** | 0 | 2 | +2 |
| **TOTAL** | **~25** | **~50** | **+25** |

---

## 🎯 Erwartete Verbesserungen

### Baseline (V2.0):
- MAE: 89.95
- Prediction Std: 12.37
- Overfitting: 1.08

### Ziel (V3.0):
- **MAE: 75-80** (-15 bis -20 Punkte, 11-17% besser)
- Prediction Std: 12-14 (ähnlich)
- Overfitting: <1.2 (leicht höher durch mehr Features)

### Warum diese Erwartung?

1. **Category-Effekt (5-10 MAE Reduktion):**
   - Groceries haben andere Muster als Electronics
   - Category = stärkster neuer Predictor

2. **Price/Discount-Effekt (3-5 MAE Reduktion):**
   - Promotions haben massive Verkaufs-Spikes
   - Preissensitivität unterscheidet sich pro Produkt

3. **Weather-Effekt (2-3 MAE Reduktion):**
   - Getränke bei Sonne, Kleidung bei Kälte
   - Regionale Unterschiede

4. **Holiday-Effekt (2-3 MAE Reduktion):**
   - Feiertags-Spitzen bisher nicht modelliert
   - Wichtig für Toys, Electronics

5. **Inventory-Effekt (1-2 MAE Reduktion):**
   - Stockouts limitieren Verkäufe
   - Out-of-stock Situationen

---

## ⚠️ Risiken & Monitoring

### Overfitting-Risiko:
- **+25 Features = +50% Parameter**
- Model könnte komplexer werden
- **Lösung:** Bestehende Regularisierung (Dropout, L2) sollte ausreichen

### Trainingszeit:
- **Mehr Features = mehr Rechenzeit**
- Erwartung: +10-20% Trainingszeit (7 Min → 8-9 Min)
- Immer noch unter Ziel (<10 Min) ✅

### Data Quality:
- **Price = 0** oder negative Werte?
- **Inventory = 0** bei Units Sold > 0? (Inkonsistenz)
- **→ Validation-Funktion bereits implementiert** ✅

---

## 🔧 Code-Änderungen

### 1. validate_dataframe()
```python
# Spaltennamen angepasst:
'Store_ID' → 'Store ID'
'Product_ID' → 'Product ID'
'Units_Sold' → 'Units Sold'
```

### 2. Feature Engineering (Zelle 7)
- **Komplett neu geschrieben**
- +25 Features hinzugefügt
- Zyklisches Encoding implementiert
- Price/Inventory Lags hinzugefügt

### 3. Scaling (Zelle 11)
```python
# Exclude-Liste erweitert um neue Original-Spalten:
exclude_cols = ['Date', 'Store ID', 'Product ID', 'Units Sold', 
                'Category', 'Region', 'Weather Condition', 
                'Seasonality', 'Inventory Level', ...]
```

---

## 📝 Nächste Schritte

1. **✅ Notebook ausführen**
   - Feature Engineering testen
   - Überprüfen: Feature-Anzahl ~50
   
2. **Training starten**
   - Baseline: MAE 89.95
   - Ziel: MAE 75-80
   
3. **Ergebnisse vergleichen**
   - MAE Verbesserung?
   - Overfitting OK? (<1.3)
   - Std erhalten? (>10)
   
4. **Feature Importance analysieren**
   ```python
   # Welche neuen Features sind wichtig?
   from sklearn.inspection import permutation_importance
   ```

5. **Dokumentation updaten**
   - Finale Ergebnisse in Header
   - DOKUMENTATION_LSTM_System.md ergänzen

---

## 🎓 Learnings für Future Work

### Wenn V3.0 FUNKTIONIERT:
- **Category/Region sind wichtig** → Bestätigt
- **Price-Elastizität messbar** → Business Insight
- **Zyklisches Encoding hilft** → Best Practice

### Wenn V3.0 NICHT funktioniert:
- **Feature Selection nötig** → Nur wichtigste Features behalten
- **Overfitting Problem** → Regularisierung erhöhen
- **Data Quality Issues** → Mehr Validation nötig

---

## ✅ Checklist

- [x] Feature Engineering Code geschrieben
- [x] Validation angepasst (Spaltennamen)
- [x] Scaling angepasst (Exclude-Liste)
- [x] Header-Dokumentation updated
- [ ] Notebook ausgeführt
- [ ] Ergebnisse evaluiert
- [ ] Feature Importance analysiert
- [ ] Dokumentation finalisiert

---

**Status:** Code implementiert, bereit für Training ✅  
**Erwartete Trainingszeit:** ~8-9 Minuten  
**Erwartete MAE Verbesserung:** 11-17% (89.95 → 75-80)  
**Nächster Schritt:** Notebook ausführen und Ergebnisse prüfen! 🚀

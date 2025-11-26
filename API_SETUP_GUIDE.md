# 🔑 API Setup Guide

## Quick Start (5 Minuten)

### 1️⃣ FRED API (EMPFOHLEN - Kostenlos & Unbegrenzt)

**Was:** Zinsdaten von der Federal Reserve (US Zentralbank)

**Registration:**
1. Gehe zu: https://fred.stlouisfed.org/docs/api/api_key.html
2. Klicke "Request API Key"
3. Fülle Formular aus (Name, Email, Organisation: "Student Research")
4. API Key kommt sofort per Email

**Free Tier:**
- ✅ Unbegrenzte Requests
- ✅ 120 Requests/Minute
- ✅ Keine Kreditkarte nötig
- ✅ Für Forschung & Bildung kostenlos

**Beispiel Key Format:** `abcd1234efgh5678ijkl9012mnop3456`

---

### 2️⃣ Nager.Date API (KEINE REGISTRATION NÖTIG!)

**Was:** Feiertage für 100+ Länder

**Best Part:** ✅ **KEINE API Key nötig!**

**Free Tier:**
- ✅ Unbegrenzte Requests
- ✅ Keine Rate Limits
- ✅ Open Source

**Unsere Implementation nutzt bereits Nager.Date als Primary!**

---

### 3️⃣ Calendarific API (Optional - Fallback)

**Was:** Alternative Feiertags-API mit mehr Details

**Registration:**
1. Gehe zu: https://calendarific.com/signup
2. Fülle Formular aus (Name, Email)
3. API Key kommt sofort

**Free Tier:**
- 1000 Requests/Monat
- Alle Länder
- Feiertag-Typen (Public, Bank, Observance)

**Benötigt:** Nur wenn Nager.Date down ist (sehr selten)

---

### 4️⃣ Alpha Vantage (Optional - Fallback für Zinsen)

**Was:** Financial & Economic Data

**Registration:**
1. Gehe zu: https://www.alphavantage.co/support/#api-key
2. Email eingeben → API Key sofort

**Free Tier:**
- 25 Requests/Tag (niedrig!)
- Nur für Fallback nutzen

---

## 🚀 Installation & Setup

### Schritt 1: Dependencies installieren

```bash
pip install python-dotenv requests redis
```

### Schritt 2: .env Datei erstellen

```bash
# Kopiere Template
cp .env.example .env

# Editiere .env und füge deine Keys ein
nano .env  # oder VSCode
```

### Schritt 3: Teste APIs

```python
from dotenv import load_dotenv
import os

load_dotenv()

# Test FRED Key
fred_key = os.getenv('FRED_API_KEY')
print(f"FRED Key: {fred_key[:10]}... (OK)" if fred_key else "❌ FRED Key fehlt")

# Test Holiday API (kein Key nötig)
from datetime import datetime
holiday_client = HolidayAPIClient(country_code="DE")
holidays = holiday_client.get_holidays(2025)
print(f"✅ Feiertage 2025: {len(holidays)} geladen")
```

---

## 🎯 Minimum für Start

**Du brauchst NUR:**
1. ✅ **FRED API Key** (5 min Registrierung)
2. ✅ **Nager.Date** (keine Registration!)

→ Damit hast du **Zinsen + Feiertage** abgedeckt!

**Optional später:**
- Calendarific (Fallback für Feiertage)
- Alpha Vantage (Fallback für Zinsen)
- OpenWeather (Weather Features)

---

## 📊 API Priorität

```
┌─────────────────────────────────────────┐
│ MUST HAVE (Jetzt)                       │
├─────────────────────────────────────────┤
│ 1. FRED API         (Zinsen)            │
│ 2. Nager.Date       (Feiertage, no key) │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ NICE TO HAVE (Später)                   │
├─────────────────────────────────────────┤
│ 3. Calendarific     (Fallback)          │
│ 4. Alpha Vantage    (Fallback)          │
│ 5. OpenWeather      (Weather)           │
└─────────────────────────────────────────┘
```

---

## 🔒 Security Best Practices

### .gitignore (bereits gesetzt)

```gitignore
# Environment Variables
.env
.env.local
.env.*.local

# API Cache
cache/
*.cache

# Credentials
*.key
*.pem
secrets/
```

### Nie im Code:

```python
# ❌ SCHLECHT
api_key = "abcd1234efgh5678"

# ✅ GUT
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('FRED_API_KEY')
```

---

## 🐛 Troubleshooting

### Problem: "API Key ungültig"

```python
# Check ob Key geladen wurde
import os
from dotenv import load_dotenv

load_dotenv()
print(os.getenv('FRED_API_KEY'))  # Sollte Key zeigen, nicht None
```

### Problem: "Rate Limit exceeded"

```python
# Unsere Implementation hat Rate Limiting eingebaut
# Warte automatisch zwischen Requests
_rate_limit(requests_per_minute=60)
```

### Problem: "API nicht erreichbar"

```python
# Unsere Implementation hat 3-Layer Fallback:
# 1. Primary API (FRED, Nager.Date)
# 2. Secondary API (Alpha Vantage, Calendarific)
# 3. Local Fallback (Mock Data)

# System läuft IMMER, auch ohne Internet!
```

---

## 📞 Support

**FRED API:**
- Docs: https://fred.stlouisfed.org/docs/api/
- Email: api.support@stls.frb.org

**Nager.Date:**
- GitHub: https://github.com/nager/Nager.Date
- Issues: https://github.com/nager/Nager.Date/issues

---

## ✅ Validation Checklist

Nach Setup:

- [ ] .env Datei erstellt
- [ ] FRED API Key eingetragen
- [ ] `python-dotenv` installiert
- [ ] Test-Script ausgeführt
- [ ] Cache-Ordner angelegt (`./cache`)
- [ ] .gitignore enthält `.env`
- [ ] Keys NICHT in Git committed

---

**Ready?** Zurück zum Notebook → Test die APIs! 🚀

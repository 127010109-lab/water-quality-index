# AquaSafe: Advanced Drinking Water Quality Index (WQI) & Hydrochemical Decision Support Platform

An end-to-end, scientifically rigorous environmental engineering software system for **multi-index water quality evaluation, statutory compliance auditing, hydrochemical corrosivity and scaling prediction, mathematical eclipsing diagnostics, quantitative chemical dosing, and official laboratory certificate compilation**.

---

> **Important notes**
> * The 500-sample benchmark file and the 50-station file in `data/` are **simulated** (synthetic) values designed to resemble each source type. They are used to test the software and are **not field measurements**.
> * The PDF output is a **computer-generated screening report**, not an accredited laboratory certificate.
> * Calcium hardness is assumed to be 70% of total hardness (and sodium 18% of TDS) because ion-specific data are not entered; measured values would improve LSI and SAR.

---

## 🌟 Executive Overview & Academic Scope

In environmental biotechnology and water supply engineering, evaluating water potability goes far beyond single-parameter pass/fail thresholds. Traditional machine learning models trained on synthetic datasets frequently suffer from lack of interpretability and external field invalidity. 

**AquaSafe** eliminates artificial machine learning dependencies and instead implements an advanced, deterministic **multi-criteria hydrochemical decision support architecture**. The platform integrates:
1. **Multi-Index Environmental Modeling:** Weighted Arithmetic WQI (WAWQI), Canadian Council of Ministers of the Environment WQI (CCME WQI 1.0), and National Sanitation Foundation WQI (NSF-WQI Additive & Multiplicative).
2. **Mathematical Eclipsing & Ambiguity Diagnostics:** Rigorous detection of when arithmetic averaging masks hazardous contaminant spikes (Eclipsing Ratio $EI$).
3. **Hydrochemical Water Stability & Corrosivity Engine:** Langelier Saturation Index (LSI), Ryznar Stability Index (RSI), Puckorius Scaling Index (PSI), and Aggressiveness Index (AI).
4. **International Multi-Standard Regulatory Auditor:** Simultaneous cross-evaluation against **BIS IS 10500:2012** (India), **WHO 4th Edition**, **US EPA National Primary/Secondary Standards**, and the **EU Drinking Water Directive (2020/2184)**.
5. **Quantitative Engineering Dosing & Equipment Sizing:** Real-time chemical dosage calculation for coagulant mass (Alum/PAC in kg/day), acid/lime neutralization, cation-exchange softening resin volume (Liters) and salt demand, Reverse Osmosis membrane operating pressure and recovery, and germicidal UV fluence ($40\ \text{mJ/cm}^2$).
6. **Batch Monitoring Station Profiling:** Geospatial coordinates and spatial analysis across 50 regional monitoring stations spanning five aquatic source typologies.
7. **Automated PDF Report Generator:** Compiles computer-generated PDF water quality assessment reports using ReportLab (with a disclaimer: not an accredited laboratory certificate).

---

## 📐 Mathematical Formulations & Governing Equations

### 1. Weighted Arithmetic Water Quality Index (WAWQI)
The WAWQI aggregates multi-parameter water data using an inverse-limit weighting sequence (Brown et al., 1970; Horton, 1965):

$$K = \frac{1}{\sum_{i=1}^{n} \frac{1}{S_i}}$$

$$W_i = \frac{K}{S_i}, \quad \text{such that} \quad \sum_{i=1}^{n} W_i = 1.0000$$

For standard contaminants with ideal baseline concentration $V_{ideal} = 0$:

$$q_i = \left( \frac{V_i - V_{ideal}}{S_i - V_{ideal}} \right) \times 100 = \left( \frac{V_i}{S_i} \right) \times 100$$

For pH (where ideal neutral baseline is $7.0$ within permissible range $6.5 – 8.5$):

$$q_{pH} = \begin{cases} 
\frac{V_{pH} - 7.0}{8.5 - 7.0} \times 100 & \text{if } V_{pH} \ge 7.0 \\
\frac{7.0 - V_{pH}}{7.0 - 6.5} \times 100 & \text{if } V_{pH} < 7.0
\end{cases}$$

For Dissolved Oxygen (DO) (ideal saturation $14.6\ \text{mg/L}$, minimum permissible threshold $5.0\ \text{mg/L}$):

$$q_{DO} = \left( \frac{14.6 - V_{DO}}{14.6 - 5.0} \right) \times 100$$

The aggregate composite index:

$$\text{WAWQI} = \sum_{i=1}^{n} (W_i \times q_i)$$

| WAWQI Score | Grade | Classification Status | Potability Assessment | Operational Action |
| :---: | :---: | :--- | :--- | :--- |
| **0.0 – 25.0** | **Grade A** | Excellent Water Quality | Completely Potable | Safe for direct consumption; routine disinfection |
| **25.1 – 50.0** | **Grade B** | Good Water Quality | Potable | Suitable for domestic supply after conventional treatment |
| **50.1 – 75.0** | **Grade C** | Poor Water Quality | Doubtful Potability | Requires coagulation, flocculation, and filtration |
| **75.1 – 100.0** | **Grade D** | Very Poor Water Quality | Non-Potable | Advanced membrane separation (RO) required |
| **> 100.0** | **Grade E** | Unsuitable for Drinking | Hazardous / Toxic | Severe pollution; acute physiological risk |

---

### 2. CCME Water Quality Index (CCME WQI 1.0)
Formulated by the Canadian Council of Ministers of the Environment across three vector dimensions:
* **Factor 1: Scope ($F_1$):** Percentage of variables failing statutory limits:
  $$F_1 = \left( \frac{\text{Number of Failed Parameters}}{\text{Total Parameters Tested}} \right) \times 100$$
* **Factor 2: Frequency ($F_2$):** Percentage of individual failed tests:
  $$F_2 = \left( \frac{\text{Number of Failed Tests}}{\text{Total Tests Conducted}} \right) \times 100$$
* **Factor 3: Amplitude ($F_3$):** Normalized sum of excursions ($nse$):
  $$\text{excursion}_i = \left( \frac{\text{Failed Test Value}_i}{\text{Guideline Limit}_i} \right) - 1$$
  $$\text{nse} = \frac{\sum_{i=1}^{n} \text{excursion}_i}{\text{Total Tests}}$$
  $$F_3 = \frac{\text{nse}}{0.01 \cdot \text{nse} + 0.01}$$
* **Composite CCME Score:**
  $$\text{CCME WQI} = 100 - \left( \frac{\sqrt{F_1^2 + F_2^2 + F_3^2}}{1.732} \right)$$

---

### 3. Langelier Saturation Index (LSI) & Water Corrosivity
Predicts calcium carbonate ($\text{CaCO}_3$) precipitation versus pipe wall dissolution:

$$\text{LSI} = \text{pH} - \text{pH}_s$$

$$\text{pH}_s = (9.3 + A + B) - (C + D)$$

* $A = \frac{\log_{10}(\text{TDS}) - 1}{10}$
* $B = -13.12 \times \log_{10}(\text{Temp}_{\text{Kelvin}}) + 34.55$
* $C = \log_{10}(\text{Calcium Hardness as } \text{CaCO}_3) - 0.4$
* $D = \log_{10}(\text{Total Alkalinity as } \text{CaCO}_3)$

**Interpretation:**
* $\text{LSI} > +0.5$: Supersaturated with $\text{CaCO}_3$; scale-forming (protects pipes but clogs heat exchangers).
* $-0.5 \le \text{LSI} \le +0.5$: Stable water in chemical equilibrium.
* $\text{LSI} < -0.5$: Undersaturated; aggressive water that corrodes metallic conduits and leaches toxic lead ($\text{Pb}$) and copper ($\text{Cu}$).

---

## 📂 Project Directory Structure

```
Water_Quality_Index_System_Web/
├── app.py                     # Main interactive Streamlit Web Dashboard
├── cli.py                     # Command-line interface for terminal users
├── test_system.py             # Automated unit verification test suite (7/7 checks)
├── requirements.txt           # Python dependencies (Zero ML overhead)
├── run_app.bat                # 1-Click Windows web application launcher
├── run_cli_test.bat           # 1-Click CLI assessment & PDF export batch file
├── README.md                  # Comprehensive scientific and architectural documentation
├── core/
│   ├── __init__.py            # Core package initializer
│   ├── standards.py           # Multi-Standard database (BIS, WHO, US EPA, EU) & presets
│   ├── wqi_calculator.py      # Multi-WQI Engine (WAWQI, CCME, NSF, Eclipsing Analysis)
│   ├── hydrochemistry.py      # Water Stability & Corrosivity Engine (LSI, RSI, PSI, AI, SAR)
│   ├── dosing_calculator.py   # Environmental Engineering Chemical Dosing & Sizing Engine
│   ├── recommender.py         # Multi-Barrier Treatment Train & Remediation Recommender
│   └── report_generator.py    # PDF Assessment Report Generator (ReportLab)
├── data/
│   ├── benchmark_water_samples.csv   # 500 SIMULATED benchmark samples (not field data)
│   └── monitoring_stations_50.csv    # 50 spatial monitoring stations with GPS coordinates
└── reports/                   # Generated PDF assessment reports
```

---

## 🚀 Execution & Quick Start Guide

### Step 1: Install Dependencies
Open PowerShell or Command Prompt in the project directory (or just double-click `run_app.bat`, which installs everything and starts the app):
```bash
pip install -r requirements.txt
```

### Step 2: Launch the Interactive Web Dashboard
Run the one-click Windows launcher:
```cmd
run_app.bat
```
*Or execute directly via Streamlit:*
```bash
python -m streamlit run app.py
```
Open your web browser at **`http://localhost:8501`**.

### Step 3: Run Headless Analysis & Export PDF via Terminal
```bash
python cli.py --generate_pdf --sample_id LAB-2026-001
```

### Step 4: Execute Automated System Verification Suite
```bash
python test_system.py
```
*Expected Output:*
```
[PASS] 1. Standards and unit weights verified (Sum = 1.0000).
[PASS] 2. Pristine water evaluation: WAWQI = 18.97 (Grade A), CCME = 100.0.
[PASS] 3. Contaminated water evaluation: WAWQI = 167.7 (Grade E), Violations = 14.
[PASS] 4. Eclipsing diagnostic engine successfully detected eclipsing paradox (Ratio = 2.29).
[PASS] 5. Hydrochemistry engine verified: LSI = -1.88 (Corrosive / Aggressive).
[PASS] 6. Engineering dosing calculator verified (Alum = 16.0 mg/L, Resin = 52.9 L).
[PASS] 7. Automated PDF assessment report successfully compiled.
============================================================
ALL 7 SYSTEM VERIFICATION TESTS PASSED SUCCESSFULLY!
```

---

## 🛡️ Multi-Barrier Treatment Train Architecture

```
[ Raw Water Feed ]
        │
        ▼
[ Stage 1: Mechanical Depth Filtration ] (5 µm Melt-Blown Polypropylene)
        │ - Intercepts silt, sand, rust, and macro-colloids (>99% efficiency)
        ▼
[ Stage 2: Catalytic Activated Carbon ] (High-Activity Coconut Shell Media)
        │ - Chemisorbs chlorine, chloramines, VOCs, THMs, odor, and color
        ▼
[ Stage 3: Reverse Osmosis / Membrane ] (Thin-Film Composite Polyamide, 0.0001 µm)
        │ - Rejects 95–99% of dissolved mineral salts (TDS), sulfates, and nitrates
        ▼
[ Stage 4: Germicidal UV Photolysis ] (254 nm Short-Wave Quartz Lamp, 40 mJ/cm²)
        │ - Inactivates bacteria, viruses, Cryptosporidium, and Giardia (4-Log / 99.99%)
        ▼
[ Stage 5: Calcite Remineralization ] (Food-Grade Calcite / Dolomite Bed)
        │ - Restores essential Ca2+/Mg2+ electrolytes and balances pH to 7.2–7.6
        ▼
[ Ultra-Pure Potable Water Output ]
```

---

*Mini Project 2026 | School of Chemical and Biotechnology*

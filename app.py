"""
AquaSafe: Advanced Drinking Water Quality Index (WQI) & Hydrochemical Decision Support System
Modern, Multi-Index Environmental Engineering Web Platform (Non-ML).
Harmonized with BIS IS 10500:2012, WHO, US EPA, and EU Drinking Water Directives.
"""

import os
import sys
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure local core packages are importable
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.standards import DRINKING_WATER_STANDARDS, WAWQI_CATEGORIES, CCME_CATEGORIES, WATER_PRESETS
from core.wqi_calculator import MultiWQIEngine
from core.hydrochemistry import HydrochemistryEngine
from core.dosing_calculator import EngineeringDosingCalculator
from core.recommender import WaterTreatmentRecommender
from core.report_generator import WaterReportGenerator

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AquaSafe - Water Quality Index & Hydrochemical Decision Platform",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CUSTOM STYLING (CSS)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .app-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%);
        color: white;
        padding: 24px 30px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.25);
    }
    .app-header h1 {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        color: #FFFFFF !important;
        letter-spacing: -0.02em;
    }
    .app-header p {
        font-size: 1.05rem;
        margin-top: 6px;
        margin-bottom: 0;
        color: #BFDBFE !important;
        font-weight: 400;
    }
    
    .metric-card {
        background: white;
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        height: 100%;
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }
    .metric-title {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 700;
        color: #64748B;
        margin-bottom: 6px;
    }
    .metric-val {
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 4px;
    }
    .metric-sub {
        font-size: 0.88rem;
        color: #475569;
        font-weight: 500;
    }
    
    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 700;
        margin-top: 6px;
    }
    
    .section-banner {
        background: #F8FAFC;
        border-left: 5px solid #2563EB;
        padding: 14px 18px;
        border-radius: 8px;
        margin: 18px 0;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# INITIALIZE COMPUTATIONAL ENGINES
# -----------------------------------------------------------------------------
@st.cache_resource
def get_engines():
    wqi = MultiWQIEngine()
    hydro = HydrochemistryEngine()
    dosing = EngineeringDosingCalculator()
    recom = WaterTreatmentRecommender()
    pdf_gen = WaterReportGenerator()
    return wqi, hydro, dosing, recom, pdf_gen

wqi_engine, hydro_engine, dosing_engine, recom_engine, pdf_engine = get_engines()

# -----------------------------------------------------------------------------
# APPLICATION HEADER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="app-header">
    <h1>💧 AquaSafe | Water Quality Index & Hydrochemical Decision Platform</h1>
    <p>Comprehensive Environmental Informatics & Multi-Index Potability Assessment System | BIS IS 10500:2012 & WHO Standards</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR CONTROLS & WATER PRESET LOADER
# -----------------------------------------------------------------------------
st.sidebar.markdown("### ⚙️ Hydrochemical Configuration")
preset_choice = st.sidebar.selectbox(
    "Load Standard Water Preset:",
    list(WATER_PRESETS.keys()),
    index=0,
    help="Select a baseline composition representing diverse ecological and municipal sources."
)

preset_data = WATER_PRESETS[preset_choice]

st.sidebar.markdown("---")
st.sidebar.markdown("### 🌡️ Physical Conditions")
water_temp = st.sidebar.slider("Water Temperature (°C):", min_value=5.0, max_value=60.0, value=25.0, step=1.0)
treatment_flow_rate = st.sidebar.number_input("Design Flow Rate (m³/day):", min_value=0.5, max_value=1000.0, value=5.0, step=1.0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📄 Export PDF Report")
sample_id_input = st.sidebar.text_input("Sample Identifier:", value="WTR-2026-001")
facility_input = st.sidebar.text_input("Source / Facility:", value=preset_choice)
location_input = st.sidebar.text_input("Sampling Location:", value="Central Water Supply Zone")
analyst_input = st.sidebar.text_input("Lead Hydrochemist:", value="Dr. Sadhna Lakshmi P")

# -----------------------------------------------------------------------------
# MAIN DASHBOARD TABS
# -----------------------------------------------------------------------------
tabs = st.tabs([
    "🔬 Water Sample Lab",
    "⚖️ Multi-Index & Eclipsing",
    "🌐 International Standards",
    "🧪 Corrosivity & Stability",
    "🛠️ Treatment & Dosing",
    "📊 Batch Station Analytics",
    "📚 Chemical Knowledge Base"
])

# =============================================================================
# TAB 1: WATER SAMPLE LAB (INTERACTIVE TESTING)
# =============================================================================
with tabs[0]:
    st.markdown("#### 🧪 Hydrochemical Parameter Inputs")
    st.caption("Adjust chemical analytes using sliders or load realistic presets from the sidebar.")

    col_in1, col_in2, col_in3 = st.columns(3)
    
    with col_in1:
        st.markdown("**General & Physical Parameters**")
        val_ph = st.slider("pH (Acidity / Alkalinity):", 3.0, 11.0, float(preset_data.get("pH", 7.20)), 0.05)
        val_solids = st.number_input("Total Dissolved Solids (TDS, mg/L):", 0.0, 3500.0, float(preset_data.get("Solids", 320.0)), 10.0)
        val_turbidity = st.number_input("Turbidity (NTU):", 0.0, 30.0, float(preset_data.get("Turbidity", 1.20)), 0.1)
        val_ec = st.number_input("Electrical Conductivity (µS/cm):", 0.0, 4000.0, float(preset_data.get("Conductivity", 380.0)), 10.0)
        val_do = st.slider("Dissolved Oxygen (DO, mg/L):", 0.0, 14.6, float(preset_data.get("Dissolved_oxygen", 7.4)), 0.1)

    with col_in2:
        st.markdown("**Major Minerals & Inorganics**")
        val_hardness = st.number_input("Total Hardness (as CaCO3, mg/L):", 0.0, 1000.0, float(preset_data.get("Hardness", 180.0)), 10.0)
        val_alkalinity = st.number_input("Total Alkalinity (as CaCO3, mg/L):", 0.0, 800.0, float(preset_data.get("Alkalinity", 120.0)), 10.0)
        val_sulfate = st.number_input("Sulfate (SO4 2-, mg/L):", 0.0, 800.0, float(preset_data.get("Sulfate", 180.0)), 10.0)
        val_chloride = st.number_input("Chloride (Cl-, mg/L):", 0.0, 1500.0, float(preset_data.get("Chloride", 85.0)), 10.0)
        val_nitrate = st.number_input("Nitrate (NO3-, mg/L):", 0.0, 150.0, float(preset_data.get("Nitrate", 18.0)), 1.0)

    with col_in3:
        st.markdown("**Disinfectants, Organics & Trace Toxins**")
        val_chloramines = st.number_input("Chloramines / Residual Cl (mg/L):", 0.0, 10.0, float(preset_data.get("Chloramines", 2.10)), 0.05)
        val_toc = st.number_input("Total Organic Carbon (TOC, mg/L):", 0.0, 20.0, float(preset_data.get("Organic_carbon", 2.00)), 0.1)
        val_thms = st.number_input("Trihalomethanes (THMs, µg/L):", 0.0, 250.0, float(preset_data.get("Trihalomethanes", 45.0)), 1.0)
        val_fluoride = st.number_input("Fluoride (F-, mg/L):", 0.0, 5.0, float(preset_data.get("Fluoride", 0.85)), 0.05)

    # Current sample dictionary
    current_sample = {
        "pH": val_ph,
        "Hardness": val_hardness,
        "Solids": val_solids,
        "Turbidity": val_turbidity,
        "Chloramines": val_chloramines,
        "Sulfate": val_sulfate,
        "Conductivity": val_ec,
        "Organic_carbon": val_toc,
        "Trihalomethanes": val_thms,
        "Nitrate": val_nitrate,
        "Fluoride": val_fluoride,
        "Dissolved_oxygen": val_do,
        "Alkalinity": val_alkalinity,
        "Chloride": val_chloride
    }

    # Execute Computations
    eval_res = wqi_engine.evaluate_all(current_sample)
    wawqi_res = eval_res["wawqi"]
    ccme_res = eval_res["ccme"]
    nsf_res = eval_res["nsf"]
    eclipsing_res = eval_res["eclipsing"]
    hydro_res = hydro_engine.calculate_corrosivity_and_scaling(current_sample, water_temp_c=water_temp)
    recom_res = recom_engine.generate_recommendations(current_sample, wawqi_res)

    st.markdown("---")
    st.markdown("### 🏆 Diagnostic Index Assessment Summary")

    # Metric Cards Row
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Weighted Arithmetic WQI</div>
            <div class="metric-val" style="color: {wawqi_res['color']};">{wawqi_res['score']}</div>
            <div class="metric-sub"><b>{wawqi_res['grade']}</b> • {wawqi_res['status']}</div>
            <div class="badge-pill" style="background: {wawqi_res['color']}22; color: {wawqi_res['color']};">
                {wawqi_res['potability']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with kpi2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">CCME Water Quality Index</div>
            <div class="metric-val" style="color: {ccme_res['color']};">{ccme_res['score']}</div>
            <div class="metric-sub"><b>{ccme_res['status']}</b> (Scope: {ccme_res['f1_scope']}%)</div>
            <div class="badge-pill" style="background: {ccme_res['color']}22; color: {ccme_res['color']};">
                Failed Tests: {ccme_res['failed_tests']}/{ccme_res['total_tests']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Langelier Corrosivity (LSI)</div>
            <div class="metric-val" style="color: {hydro_res['lsi_color']};">{hydro_res['lsi']}</div>
            <div class="metric-sub">pH: {val_ph:.2f} | Saturation pHs: {hydro_res['ph_s']}</div>
            <div class="badge-pill" style="background: {hydro_res['lsi_color']}22; color: {hydro_res['lsi_color']};">
                {hydro_res['lsi_status']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with kpi4:
        v_count = wawqi_res['violation_count']
        v_color = "#10B981" if v_count == 0 else ("#F59E0B" if v_count <= 2 else "#EF4444")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Guideline Violations</div>
            <div class="metric-val" style="color: {v_color};">{v_count}</div>
            <div class="metric-sub">Standard: BIS IS 10500:2012</div>
            <div class="badge-pill" style="background: {v_color}22; color: {v_color};">
                {'All Parameters Compliant' if v_count == 0 else f'{v_count} Breaches Detected'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Visualization: Parameter Breakdown Chart
    chart_col1, chart_col2 = st.columns([3, 2])

    with chart_col1:
        st.markdown("##### 📊 Parameter Sub-Index Ratings (qi) & Weight Contribution")
        sub_df = pd.DataFrame([
            {
                "Parameter": info["name"],
                "Sub-Index (qi)": info["qi"],
                "Unit Weight (Wi)": info["wi"],
                "Weighted qi": info["weighted_qi"]
            }
            for param, info in wawqi_res["sub_indices"].items()
        ]).sort_values("Sub-Index (qi)", ascending=True)

        fig, ax = plt.subplots(figsize=(7, 4.2))
        bar_colors = ["#EF4444" if q > 100.0 else "#3B82F6" for q in sub_df["Sub-Index (qi)"]]
        bars = ax.barh(sub_df["Parameter"], sub_df["Sub-Index (qi)"], color=bar_colors, edgecolor="none", height=0.65)
        ax.axvline(100.0, color="#DC2626", linestyle="--", linewidth=1.5, label="Permissible Limit (qi = 100)")
        ax.set_xlabel("Sub-Index Score (qi)", fontsize=9, fontweight="bold")
        ax.set_title("Individual Parameter Quality Rating (qi > 100 indicates breach)", fontsize=10, fontweight="bold")
        ax.legend(loc="lower right", fontsize=8)
        ax.grid(axis="x", linestyle=":", alpha=0.6)
        sns.despine(top=True, right=True)
        st.pyplot(fig)

    with chart_col2:
        st.markdown("##### 🚨 Parameter Compliance Audit Table")
        audit_rows = []
        for param, s_data in wawqi_res["sub_indices"].items():
            viol = next((v for v in wawqi_res["violations"] if v["parameter"] == param), None)
            audit_rows.append({
                "Parameter": s_data["name"],
                "Measured": f"{s_data['value']} {s_data['unit']}",
                "Standard": f"≤ {s_data['standard']}",
                "Status": "⚠️ VIOLATION" if viol else "✅ Compliant"
            })
        st.dataframe(pd.DataFrame(audit_rows), use_container_width=True, hide_index=True)

    # One-Click PDF Generator
    st.markdown("---")
    st.markdown("##### 📥 Generate PDF Assessment Report")
    pdf_btn_col1, pdf_btn_col2 = st.columns([1, 3])
    with pdf_btn_col1:
        if st.button("Generate & Download PDF Report", type="primary"):
            with st.spinner("Compiling PDF assessment report..."):
                pdf_path = pdf_engine.generate_pdf_report(
                    sample_dict=current_sample,
                    wawqi_res=wawqi_res,
                    ccme_res=ccme_res,
                    hydro_res=hydro_res,
                    recom_res=recom_res,
                    sample_id=sample_id_input,
                    source_name=facility_input,
                    location=location_input,
                    analyst_name=analyst_input
                )
                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()
                st.download_button(
                    label="⬇️ Download Report PDF",
                    data=pdf_bytes,
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf"
                )
                st.success(f"Report successfully compiled: {os.path.basename(pdf_path)}")

# =============================================================================
# TAB 2: MULTI-INDEX COMPARISON & ECLIPSING DIAGNOSTICS
# =============================================================================
with tabs[1]:
    st.markdown("### ⚖️ Multi-Index Hydrochemical Comparison & Eclipsing Analysis")
    st.write(
        "Environmental indexing frameworks handle contaminant aggregations with distinct mathematical philosophies. "
        "Comparing multiple indices reveals analytical discrepancies and uncovers hidden eclipsing phenomena."
    )

    idx_c1, idx_c2, idx_c3 = st.columns(3)
    with idx_c1:
        st.info(f"**Weighted Arithmetic WQI (WAWQI)**\n\nScore: **{wawqi_res['score']}**\n\nGrade: **{wawqi_res['grade']}** ({wawqi_res['status']})\n\nMethod: Inverse-standard weight aggregation.")
    with idx_c2:
        st.info(f"**CCME Water Quality Index**\n\nScore: **{ccme_res['score']}** / 100\n\nStatus: **{ccme_res['status']}**\n\nMethod: Scope (F1), Frequency (F2), and Amplitude (F3) 3D vector.")
    with idx_c3:
        st.info(f"**NSF Water Quality Index**\n\nAdditive: **{nsf_res['additive_score']}** / 100\n\nMultiplicative: **{nsf_res['multiplicative_score']}** / 100\n\nMethod: Parameter-specific functional curves.")

    st.markdown("---")
    st.markdown("#### 🔍 The Eclipsing & Ambiguity Problem")
    
    eclip = eclipsing_res
    if eclip["is_eclipsed"]:
        st.error(f"""
        **⚠️ {eclip['eclipsing_severity']} DETECTED!**
        
        The overall Weighted Arithmetic index classified this sample as **{wawqi_res['grade']} ({wawqi_res['status']})**, 
        yet the sample exceeds statutory permissible thresholds in **{wawqi_res['violation_count']} critical parameter(s)**!
        
        *Reason:* In arithmetic weighting, parameters with large numerical thresholds (such as Hardness, Sulfate, and TDS) 
        receive extremely small mathematical unit weights (Wi = K / Si). As a consequence, high concentrations of these minerals 
        are 'eclipsed' by favorable readings in other parameters.
        """)
        for note in eclip["diagnostic_notes"]:
            st.warning(note)
    elif eclip["is_ambiguous"]:
        st.warning(f"**Index Ambiguity Detected:** {eclip['diagnostic_notes'][0]}")
    else:
        st.success("✅ **No Eclipsing Detected:** Composite index scores agree consistently with individual parameter compliance states.")

    st.markdown(f"**Eclipsing Index Factor (EI):** `{eclip['eclipsing_ratio']}` (Ratio of worst single parameter rating to aggregate score: {eclip['max_parameter_sub_index']} / {wawqi_res['score']})")

    st.markdown("---")
    st.markdown("#### 📐 Mathematical Formulation Breakdown")
    with st.expander("View Governing Equations"):
        st.latex(r"K = \frac{1}{\sum_{i=1}^{n} \frac{1}{S_i}}, \quad W_i = \frac{K}{S_i}")
        st.latex(r"q_i = \left(\frac{V_i - V_{ideal}}{S_i - V_{ideal}}\right) \times 100, \quad \text{WAWQI} = \sum_{i=1}^{n} W_i q_i")
        st.latex(r"F_1 = \left(\frac{\text{Failed Variables}}{\text{Total Variables}}\right) \times 100, \quad F_3 = \frac{\text{nse}}{0.01 \cdot \text{nse} + 0.01}")
        st.latex(r"\text{CCME WQI} = 100 - \frac{\sqrt{F_1^2 + F_2^2 + F_3^2}}{1.732}")

# =============================================================================
# TAB 3: INTERNATIONAL MULTI-STANDARD REGULATORY AUDITOR
# =============================================================================
with tabs[2]:
    st.markdown("### 🌐 International Multi-Standard Regulatory Auditor")
    st.write("Cross-evaluates current water sample against four major international drinking water guidelines.")

    audit_matrix = []
    for p_key, p_info in DRINKING_WATER_STANDARDS.items():
        val = current_sample.get(p_key, 0.0)
        bis_pass = "✅ Pass" if (p_key == "pH" and 6.5 <= val <= 8.5) or (p_key == "Dissolved_oxygen" and val >= 5.0) or (p_key not in ["pH", "Dissolved_oxygen"] and val <= p_info["bis_permissible"]) else "❌ Fail"
        who_pass = "✅ Pass" if (p_key == "pH" and 6.5 <= val <= 8.5) or (p_key == "Dissolved_oxygen" and val >= 5.0) or (p_key not in ["pH", "Dissolved_oxygen"] and val <= p_info["who_guideline"]) else "❌ Fail"
        epa_pass = "✅ Pass" if (p_key == "pH" and 6.5 <= val <= 8.5) or (p_key not in ["pH", "Dissolved_oxygen"] and val <= p_info["epa_secondary"]) else "❌ Fail"
        eu_pass = "✅ Pass" if (p_key == "pH" and 6.5 <= val <= 9.5) or (p_key not in ["pH", "Dissolved_oxygen"] and val <= p_info["eu_standard"]) else "❌ Fail"

        audit_matrix.append({
            "Parameter": p_info["name"],
            "Measured Value": f"{val} {p_info['unit']}",
            "BIS IS 10500:2012": f"{p_info['bis_permissible']} ({bis_pass})",
            "WHO 4th Ed.": f"{p_info['who_guideline']} ({who_pass})",
            "US EPA": f"{p_info['epa_secondary']} ({epa_pass})",
            "EU Directive": f"{p_info['eu_standard']} ({eu_pass})"
        })

    st.dataframe(pd.DataFrame(audit_matrix), use_container_width=True, hide_index=True)

# =============================================================================
# TAB 4: CORROSIVITY, SCALING & HYDROCHEMISTRY
# =============================================================================
with tabs[3]:
    st.markdown("### 🧪 Water Stability, Corrosivity & Scaling Diagnostic Engine")
    st.write(
        "Water potability and infrastructure safety depend critically on chemical stability. "
        "Corrosive water leaches lead and copper from pipes, while scale-forming water clogs municipal conduits and boilers."
    )

    c_col1, c_col2 = st.columns(2)

    with c_col1:
        st.markdown("#### 1. Carbonate Saturation Indices")
        st.metric(label="Langelier Saturation Index (LSI)", value=f"{hydro_res['lsi']}", delta=hydro_res['lsi_status'])
        st.write(f"**Action Interpretation:** {hydro_res['lsi_action']}")

        st.metric(label="Ryznar Stability Index (RSI)", value=f"{hydro_res['rsi']}", delta=hydro_res['rsi_status'])
        st.metric(label="Puckorius Scaling Index (PSI)", value=f"{hydro_res['psi']}")
        st.metric(label="Aggressiveness Index (AI)", value=f"{hydro_res['ai']} ({hydro_res['ai_status']})")

    with c_col2:
        st.markdown("#### 2. Secondary Irrigation & Soil Hazard Indices")
        irrig_res = hydro_engine.calculate_irrigation_suitability(current_sample)
        st.metric(label="Sodium Adsorption Ratio (SAR)", value=f"{irrig_res['sar']}", delta=irrig_res['sar_status'])
        st.metric(label="Magnesium Hazard Ratio (MAR)", value=f"{irrig_res['mar']}%", delta=irrig_res['mar_status'])
        
        st.markdown("""
        **Engineering Guidance:**
        - **SAR < 10:** Safe for all domestic lawns, urban horticulture, and agriculture.
        - **MAR < 50%:** Balanced calcium-magnesium ratio; no soil permeability degradation.
        """)

# =============================================================================
# TAB 5: TREATMENT ENGINEERING & CHEMICAL DOSING
# =============================================================================
with tabs[4]:
    st.markdown("### 🛠️ Targeted Engineering Remediation & Process Design Engine")
    st.write(f"**Overall System Recommendation:** {recom_res['verdict']}")
    st.info(recom_res['guidance'])

    st.markdown("#### 📋 Contaminant-Specific Remediation Solutions")
    if not recom_res["action_items"]:
        st.success("✅ Water complies with all tested parameters. No corrective engineering filtration required.")
    else:
        for idx, act in enumerate(recom_res["action_items"], start=1):
            with st.expander(f"Action {idx}: {act['action_title']} ({act['parameter']}) - Urgency: {act['urgency']}"):
                st.write(f"**Recommended Technology:** {act['technology']}")
                st.write(f"**Scientific Mechanism:** {act['scientific_mechanism']}")
                st.write(f"**Domestic / Municipal Implementation:** {act['household_solution']}")
                st.write(f"**Expected Performance:** {act['removal_efficiency']}")

    st.markdown("---")
    st.markdown("#### ⚗️ Chemical Dosing & Unit Process Sizing Calculator")
    st.caption(f"Calculations based on selected flow rate: **{treatment_flow_rate} m³/day** ({treatment_flow_rate * 1000:.0f} Liters/day)")

    dose_c1, dose_c2 = st.columns(2)

    with dose_c1:
        st.markdown("##### Coagulation & Clarification (Turbidity)")
        coag_res = dosing_engine.calculate_coagulant_dose(val_turbidity, flow_rate_m3_day=treatment_flow_rate)
        st.write(f"- **Recommended Alum Dose:** `{coag_res['alum_dose_mg_l']} mg/L`")
        st.write(f"- **Daily Alum Consumption:** `{coag_res['daily_alum_demand_kg']} kg/day`")
        st.write(f"- **Coagulant Type:** {coag_res['recommended_coagulant']}")

        st.markdown("##### Water Softening Unit Sizing (Hardness)")
        soft_res = dosing_engine.calculate_softener_sizing(val_hardness, flow_rate_m3_day=treatment_flow_rate)
        st.write(f"- **Hardness to Remove:** `{soft_res['hardness_to_remove_mg_l']} mg/L CaCO3`")
        st.write(f"- **Required Cation Resin Bed:** `{soft_res['recommended_resin_volume_l']} Liters`")
        st.write(f"- **Salt per Regeneration Cycle:** `{soft_res['salt_per_regeneration_kg']} kg NaCl`")

    with dose_c2:
        st.markdown("##### Reverse Osmosis (RO) Membrane Parameters (TDS)")
        ro_res = dosing_engine.calculate_ro_membrane_performance(val_solids, flow_rate_m3_day=treatment_flow_rate)
        st.write(f"- **Osmotic Pressure (Π):** `{ro_res['osmotic_pressure_bar']} bar`")
        st.write(f"- **Recommended Pump Feed Pressure:** `{ro_res['recommended_pump_pressure_bar']} bar` ({ro_res['recommended_pump_psi']} PSI)")
        st.write(f"- **Projected Permeate Output:** `{ro_res['pure_permeate_output_m3_day']} m³/day` (70% recovery)")
        st.write(f"- **Projected Permeate TDS:** `{ro_res['projected_permeate_tds_mg_l']} mg/L` (96% rejection)")

        st.markdown("##### Germicidal UV Disinfection Chamber")
        uv_res = dosing_engine.calculate_uv_disinfection_dose(val_turbidity, val_toc)
        st.write(f"- **Estimated UVT% at 254 nm:** `{uv_res['estimated_uvt_percent']}%` ({uv_res['uvt_status']})")
        st.write(f"- **Target Germicidal Fluence:** `{uv_res['target_uv_fluence']}`")
        st.write(f"- **Disinfection Efficacy:** {uv_res['pathogen_log_reduction']}")

    st.markdown("---")
    st.markdown("#### 🛡️ Standard 5-Stage Multi-Barrier Water Treatment Train")
    for stage in recom_res["multi_barrier_train"]:
        st.markdown(f"**Stage {stage['stage_num']}: {stage['stage_name']}**")
        st.write(f"*Filter Type:* {stage['filter_type']} | *Target:* {stage['primary_target']}")
        st.write(f"*Operational Purpose:* {stage['operational_purpose']}")

# =============================================================================
# TAB 6: BATCH STATION ANALYTICS & GEOSPATIAL PROFILING
# =============================================================================
with tabs[5]:
    st.markdown("### 📊 Batch Station Analytics & Geospatial Hydrochemical Profiling")
    st.write("Process and evaluate multiple water quality monitoring stations simultaneously.")

    batch_csv_path = os.path.join(BASE_DIR, "data", "monitoring_stations_50.csv")
    if os.path.exists(batch_csv_path):
        df_batch = pd.read_csv(batch_csv_path)
    else:
        df_batch = None

    uploaded_file = st.file_uploader("Upload Monitoring Stations CSV File (or use bundled 50-station dataset):", type=["csv"])
    if uploaded_file is not None:
        df_batch = pd.read_csv(uploaded_file)

    if df_batch is not None:
        st.success(f"Loaded {len(df_batch)} monitoring stations.")
        
        # Calculate WQI for all rows
        batch_results = []
        for _, row in df_batch.iterrows():
            row_dict = row.to_dict()
            w_res = wqi_engine.calculate_wawqi(row_dict)
            c_res = wqi_engine.calculate_ccme_wqi(row_dict)
            h_res = hydro_engine.calculate_corrosivity_and_scaling(row_dict)
            batch_results.append({
                "Station_ID": row.get("Station_ID", ""),
                "Station_Name": row.get("Station_Name", ""),
                "Source_Type": row.get("Source_Type", "General"),
                "Latitude": row.get("Latitude", 10.78),
                "Longitude": row.get("Longitude", 79.13),
                "WAWQI_Score": w_res["score"],
                "WAWQI_Grade": w_res["grade"],
                "WAWQI_Potability": w_res["potability"],
                "CCME_Score": c_res["score"],
                "CCME_Status": c_res["status"],
                "LSI_Corrosivity": h_res["lsi"],
                "Violations_Count": w_res["violation_count"]
            })

        df_out = pd.DataFrame(batch_results)

        # High-Level Metrics
        b_col1, b_col2, b_col3, b_col4 = st.columns(4)
        with b_col1:
            st.metric("Total Stations Analyzed", f"{len(df_out)}")
        with b_col2:
            potable_n = len(df_out[df_out["WAWQI_Potability"].isin(["Completely Potable", "Potable"])])
            st.metric("Potable Stations", f"{potable_n} ({potable_n / len(df_out) * 100:.1f}%)")
        with b_col3:
            st.metric("Average WAWQI Score", f"{df_out['WAWQI_Score'].mean():.2f}")
        with b_col4:
            st.metric("Average Violations / Station", f"{df_out['Violations_Count'].mean():.1f}")

        # Geospatial Map
        st.markdown("##### 🗺️ Geographic Distribution of Monitoring Stations")
        if "Latitude" in df_out.columns and "Longitude" in df_out.columns:
            st.map(df_out.rename(columns={"Latitude": "lat", "Longitude": "lon"}))

        # Boxplot Comparison by Source Type
        st.markdown("##### 📦 WAWQI Score Distribution by Water Source Typology")
        fig_box, ax_box = plt.subplots(figsize=(8, 3.8))
        sns.boxplot(data=df_out, x="Source_Type", y="WAWQI_Score", palette="Blues_r", ax=ax_box)
        ax_box.axhline(50.0, color="#10B981", linestyle="--", label="Potable Threshold (WQI = 50)")
        ax_box.axhline(100.0, color="#EF4444", linestyle="--", label="Hazardous Threshold (WQI = 100)")
        ax_box.set_ylabel("WAWQI Score", fontweight="bold")
        ax_box.set_title("Water Quality Index Variation Across Aquatic Environments", fontweight="bold")
        ax_box.legend(loc="upper left")
        sns.despine()
        st.pyplot(fig_box)

        # Batch Table & Export
        st.markdown("##### 📋 Batch Monitoring Data Table")
        st.dataframe(df_out, use_container_width=True, hide_index=True)

        csv_data = df_out.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Export Batch Assessment as CSV",
            data=csv_data,
            file_name="AquaSafe_Batch_Assessment_Results.csv",
            mime="text/csv"
        )

# =============================================================================
# TAB 7: HYDROCHEMICAL KNOWLEDGE BASE
# =============================================================================
with tabs[6]:
    st.markdown("### 📚 Hydrochemical Knowledge Base & Regulatory Standards Guide")
    st.write(
        "Scientific documentation of evaluated physical, chemical, and biological water quality parameters, "
        "their environmental occurrence, toxicology, and regulatory thresholds."
    )

    for p_name, p_data in DRINKING_WATER_STANDARDS.items():
        with st.expander(f"📘 {p_data['name']} (Standard: ≤ {p_data['standard']} {p_data['unit']})"):
            st.write(f"**Category:** {p_data['category']}")
            st.write(f"**Ideal Baseline Concentration:** {p_data.get('ideal', 0.0)} {p_data['unit']}")
            st.write(f"**BIS IS 10500:2012 Threshold:** Acceptable: {p_data['bis_acceptable']} | Permissible: {p_data['bis_permissible']} {p_data['unit']}")
            st.write(f"**WHO Guideline:** {p_data['who_guideline']} {p_data['unit']}")
            st.write(f"**Description:** {p_data['description']}")
            st.write(f"**Health & Operational Hazard:** {p_data['hazard']}")

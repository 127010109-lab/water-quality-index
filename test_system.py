"""
Automated Software Verification Test Suite for AquaSafe.
Verifies all computational, hydrochemical, dosing, and PDF compilation engines.
"""

import os
import sys

# Ensure local core packages are importable
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.standards import WATER_PRESETS, DRINKING_WATER_STANDARDS
from core.wqi_calculator import MultiWQIEngine
from core.hydrochemistry import HydrochemistryEngine
from core.dosing_calculator import EngineeringDosingCalculator
from core.recommender import WaterTreatmentRecommender
from core.report_generator import WaterReportGenerator


def test_complete_system():
    print("=" * 60)
    print("AQUASAFE: AUTOMATED SYSTEM VERIFICATION TEST")
    print("=" * 60)

    # 1. Test Standards & Weights
    wqi_engine = MultiWQIEngine()
    assert len(wqi_engine.standards) >= 9, "Standards dictionary incomplete"
    weight_sum = sum(wqi_engine.wawqi_weights.values())
    assert abs(weight_sum - 1.0) < 1e-4, f"Unit weights do not sum to 1.0 (Sum = {weight_sum})"
    print("[PASS] 1. Standards and unit weights verified (Sum = 1.0000).")

    # 2. Test WAWQI & CCME WQI on Pure Bottled Water
    sample_pure = WATER_PRESETS["Commercial Reverse Osmosis (RO) Bottled Water"]
    pure_res = wqi_engine.calculate_wawqi(sample_pure)
    assert pure_res["grade"] == "Grade A", f"Pure water expected Grade A, got {pure_res['grade']}"
    assert pure_res["violation_count"] == 0, f"Pure water expected 0 violations, got {pure_res['violation_count']}"
    ccme_pure = wqi_engine.calculate_ccme_wqi(sample_pure)
    assert ccme_pure["score"] >= 95.0, f"Pure water CCME expected >=95, got {ccme_pure['score']}"
    print(f"[PASS] 2. Pristine water evaluation: WAWQI = {pure_res['score']} (Grade A), CCME = {ccme_pure['score']}.")

    # 3. Test Contaminated Industrial Water
    sample_ind = WATER_PRESETS["Industrial Effluent Contaminated Groundwater"]
    ind_res = wqi_engine.calculate_wawqi(sample_ind)
    assert ind_res["grade"] == "Grade E", f"Industrial water expected Grade E, got {ind_res['grade']}"
    assert ind_res["violation_count"] >= 5, "Industrial water expected multiple violations"
    print(f"[PASS] 3. Contaminated water evaluation: WAWQI = {ind_res['score']} (Grade E), Violations = {ind_res['violation_count']}.")

    # 4. Test Eclipsing Analysis on Borewell Hard Water
    sample_bore = WATER_PRESETS["Deep Borewell Groundwater (Hard Water)"]
    bore_eval = wqi_engine.evaluate_all(sample_bore)
    assert bore_eval["eclipsing"]["is_eclipsed"] is True, "Expected eclipsing detection on borewell water"
    print(f"[PASS] 4. Eclipsing diagnostic engine successfully detected eclipsing paradox (Ratio = {bore_eval['eclipsing']['eclipsing_ratio']}).")

    # 5. Test Hydrochemistry Corrosivity (LSI, RSI)
    hydro_engine = HydrochemistryEngine()
    hydro_res = hydro_engine.calculate_corrosivity_and_scaling(sample_pure, water_temp_c=25.0)
    assert "lsi" in hydro_res and "rsi" in hydro_res, "Hydrochemistry keys missing"
    print(f"[PASS] 5. Hydrochemistry engine verified: LSI = {hydro_res['lsi']} ({hydro_res['lsi_status']}).")

    # 6. Test Engineering Dosing Calculator
    dosing_engine = EngineeringDosingCalculator()
    coag_res = dosing_engine.calculate_coagulant_dose(turbidity_ntu=10.0, flow_rate_m3_day=5.0)
    assert coag_res["alum_dose_mg_l"] > 10.0, "Alum dose calculation error"
    soft_res = dosing_engine.calculate_softener_sizing(hardness_mg_l=400.0, flow_rate_m3_day=5.0)
    assert soft_res["recommended_resin_volume_l"] > 0, "Resin sizing error"
    print(f"[PASS] 6. Engineering dosing calculator verified (Alum = {coag_res['alum_dose_mg_l']} mg/L, Resin = {soft_res['recommended_resin_volume_l']} L).")

    # 7. Test PDF report generation
    pdf_engine = WaterReportGenerator()
    recom_engine = WaterTreatmentRecommender()
    recom_res = recom_engine.generate_recommendations(sample_pure, pure_res)
    pdf_path = pdf_engine.generate_pdf_report(
        sample_dict=sample_pure,
        wawqi_res=pure_res,
        ccme_res=ccme_pure,
        hydro_res=hydro_res,
        recom_res=recom_res,
        sample_id="SYSTEM-TEST-001"
    )
    assert os.path.exists(pdf_path), f"PDF was not generated at {pdf_path}"
    assert os.path.getsize(pdf_path) > 1000, "Generated PDF file is empty or corrupted"
    print(f"[PASS] 7. Automated PDF assessment report successfully compiled ({os.path.getsize(pdf_path)} bytes).")

    print("=" * 60)
    print("ALL 7 SYSTEM VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    test_complete_system()

"""
AquaSafe: Terminal Command-Line Interface (CLI).
Enables automated headless water sample evaluation, multi-index calculation, and PDF report compilation.
"""

import argparse
import json
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


def run_cli():
    parser = argparse.ArgumentParser(description="AquaSafe: Hydrochemical Water Quality Index CLI")
    parser.add_argument("--preset", type=str, choices=list(WATER_PRESETS.keys()), default="Municipal Treated Tap Water", help="Load water preset")
    parser.add_argument("--ph", type=float, default=None, help="pH value")
    parser.add_argument("--hardness", type=float, default=None, help="Total Hardness (mg/L)")
    parser.add_argument("--solids", type=float, default=None, help="Total Dissolved Solids (mg/L)")
    parser.add_argument("--turbidity", type=float, default=None, help="Turbidity (NTU)")
    parser.add_argument("--chloramines", type=float, default=None, help="Chloramines (mg/L)")
    parser.add_argument("--sulfate", type=float, default=None, help="Sulfate (mg/L)")
    parser.add_argument("--conductivity", type=float, default=None, help="Electrical Conductivity (µS/cm)")
    parser.add_argument("--toc", type=float, default=None, help="Total Organic Carbon (mg/L)")
    parser.add_argument("--thms", type=float, default=None, help="Trihalomethanes (µg/L)")
    parser.add_argument("--nitrate", type=float, default=None, help="Nitrate (mg/L)")
    parser.add_argument("--fluoride", type=float, default=None, help="Fluoride (mg/L)")
    parser.add_argument("--temp", type=float, default=25.0, help="Water Temperature (°C)")
    parser.add_argument("--generate_pdf", action="store_true", help="Generate PDF assessment report")
    parser.add_argument("--sample_id", type=str, default="CLI-TEST-001", help="Sample ID for the report")

    args = parser.parse_args()

    # Load baseline from preset
    sample = dict(WATER_PRESETS.get(args.preset, WATER_PRESETS["Municipal Treated Tap Water"]))

    # Override with explicit CLI flags if provided
    if args.ph is not None: sample["pH"] = args.ph
    if args.hardness is not None: sample["Hardness"] = args.hardness
    if args.solids is not None: sample["Solids"] = args.solids
    if args.turbidity is not None: sample["Turbidity"] = args.turbidity
    if args.chloramines is not None: sample["Chloramines"] = args.chloramines
    if args.sulfate is not None: sample["Sulfate"] = args.sulfate
    if args.conductivity is not None: sample["Conductivity"] = args.conductivity
    if args.toc is not None: sample["Organic_carbon"] = args.toc
    if args.thms is not None: sample["Trihalomethanes"] = args.thms
    if args.nitrate is not None: sample["Nitrate"] = args.nitrate
    if args.fluoride is not None: sample["Fluoride"] = args.fluoride

    # Instantiate engines
    wqi_engine = MultiWQIEngine()
    hydro_engine = HydrochemistryEngine()
    recom_engine = WaterTreatmentRecommender()
    pdf_engine = WaterReportGenerator()

    # Compute results
    eval_res = wqi_engine.evaluate_all(sample)
    wawqi_res = eval_res["wawqi"]
    ccme_res = eval_res["ccme"]
    nsf_res = eval_res["nsf"]
    eclip_res = eval_res["eclipsing"]
    hydro_res = hydro_engine.calculate_corrosivity_and_scaling(sample, water_temp_c=args.temp)
    recom_res = recom_engine.generate_recommendations(sample, wawqi_res)

    print("\n" + "=" * 70)
    print("      AQUASAFE WATER QUALITY & HYDROCHEMICAL ASSESSMENT REPORT")
    print("=" * 70)
    print(f"Sample Identifier : {args.sample_id}")
    print(f"Water Source Type : {args.preset}")
    print(f"Water Temperature : {args.temp} °C")
    print("-" * 70)
    print(f"WAWQI Score       : {wawqi_res['score']}  ({wawqi_res['grade']} - {wawqi_res['status']})")
    print(f"WAWQI Potability  : {wawqi_res['potability']}")
    print(f"CCME WQI Score    : {ccme_res['score']}  ({ccme_res['status']})")
    print(f"NSF Additive WQI  : {nsf_res['additive_score']}")
    print(f"LSI Corrosivity   : {hydro_res['lsi']}  ({hydro_res['lsi_status']})")
    print(f"Ryznar Index (RSI): {hydro_res['rsi']}  ({hydro_res['rsi_status']})")
    print(f"Total Violations  : {wawqi_res['violation_count']} breach(es)")
    print("-" * 70)
    print(f"Remediation Plan  : {recom_res['verdict']}")
    print(f"Guidance Notes    : {recom_res['guidance']}")
    
    if eclip_res["is_eclipsed"]:
        print("-" * 70)
        print(f"[!] ECLIPSING WARNING: {eclip_res['eclipsing_severity']}")
        for n in eclip_res["diagnostic_notes"]:
            print(f"    * {n}")

    if args.generate_pdf:
        pdf_path = pdf_engine.generate_pdf_report(
            sample_dict=sample,
            wawqi_res=wawqi_res,
            ccme_res=ccme_res,
            hydro_res=hydro_res,
            recom_res=recom_res,
            sample_id=args.sample_id,
            source_name=args.preset,
            location="Automated CLI Test",
            analyst_name="CLI Automated System"
        )
        print("-" * 70)
        print(f"PDF assessment report compiled successfully at:\n{pdf_path}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_cli()

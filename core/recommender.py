"""
Comprehensive Water Treatment Engineering Recommender & Multi-Barrier Treatment Train Engine.
Maps detected hydrochemical violations to validated environmental engineering unit operations:
  - Coagulation & Flocculation
  - Granular / Catalytic Activated Carbon (GAC/CAC)
  - Membrane Separation (Ultrafiltration, Reverse Osmosis)
  - Ion Exchange Resins (SAC, SBA, WAC)
  - Advanced Oxidation & Germicidal Photolysis (UV/H2O2, UV 254nm)
  - Mineral Neutralization & Remineralization
"""

from .standards import DRINKING_WATER_STANDARDS


class WaterTreatmentRecommender:
    """Diagnoses hydrochemical breaches and formulates targeted multi-barrier treatment strategies."""

    def __init__(self):
        self.solutions_catalog = {
            "pH_acidic": {
                "parameter": "pH",
                "condition": "Acidic pH (< 6.5)",
                "action_title": "Calcite Bed Neutralization & Bicarbonate Buffering",
                "technology": "Slow-Dissolving Calcite (CaCO3) / Corosex (MgO) Media Filter",
                "scientific_mechanism": (
                    "Calcium carbonate reactively neutralizes un-ionized aggressive carbon dioxide (CO2), "
                    "forming soluble calcium bicarbonate [Ca(HCO3)2], naturally elevating pH into the 7.0–7.4 zone."
                ),
                "household_solution": "Point-of-entry automatic backwashing calcite tank or inline remineralization cartridge.",
                "removal_efficiency": "Brings pH to 7.0 – 7.4 (100% acidity neutralization)",
                "urgency": "High"
            },
            "pH_alkaline": {
                "parameter": "pH",
                "condition": "Alkaline pH (> 8.5)",
                "action_title": "Weak Acid Cation Exchange & Acid Dosing",
                "technology": "Weak Acid Cation (WAC) Resin or Dilute Food-Grade Acid Injection",
                "scientific_mechanism": (
                    "Releases hydrogen ions (H+) to react with excess hydroxyl (OH-) alkalinity, "
                    "preventing calcium carbonate scale incrustation and neutralizing bitter taste."
                ),
                "household_solution": "Thin-Film Composite (TFC) Reverse Osmosis purifier with pH balancing filter.",
                "removal_efficiency": "Corrects pH to 7.2 – 7.6",
                "urgency": "Moderate"
            },
            "Hardness": {
                "parameter": "Hardness",
                "condition": "Elevated Hardness (> 300 mg/L)",
                "action_title": "Cation-Exchange Softening (Sodium Cycle)",
                "technology": "Strong Acid Cation (SAC) Polystyrene Sulfonate Resin",
                "scientific_mechanism": (
                    "High-affinity sulfonic acid groups selectively exchange scale-forming bivalent calcium (Ca2+) "
                    "and magnesium (Mg2+) cations for non-scaling sodium (Na+) ions."
                ),
                "household_solution": "Whole-house automatic timer-regenerated water softener with brine tank.",
                "removal_efficiency": "90% – 98% Hardness Reduction",
                "urgency": "Moderate"
            },
            "Solids": {
                "parameter": "Solids",
                "condition": "Elevated Total Dissolved Solids (> 500 mg/L)",
                "action_title": "Thin-Film Composite (TFC) Reverse Osmosis",
                "technology": "High-Pressure Polyamide Membrane Separation (0.0001 µm pore cut-off)",
                "scientific_mechanism": (
                    "Overcomes osmotic pressure to force pure water across a dense polyamide semi-permeable membrane, "
                    "rejecting 95–99% of dissolved inorganic salts, silica, and heavy mineral ions via steric hindrance and charge exclusion."
                ),
                "household_solution": "Under-sink multi-stage Reverse Osmosis (RO) drinking purification system.",
                "removal_efficiency": "95% – 99% TDS Rejection",
                "urgency": "High"
            },
            "Turbidity": {
                "parameter": "Turbidity",
                "condition": "High Turbidity / Cloudiness (> 1.0 – 5.0 NTU)",
                "action_title": "Chemical Coagulation & Dual-Media Depth Filtration",
                "technology": "Alum Coagulation followed by Sand/Anthracite Depth Filter & Spun Polypropylene",
                "scientific_mechanism": (
                    "Trivalent aluminum ions destabilize negatively charged colloidal clays, forming micro-flocs "
                    "that are strained by macro-porous dual-media anthracite-sand bed filters."
                ),
                "household_solution": "5-micron spun polypropylene melt-blown sediment cartridge followed by a 1-micron polished block.",
                "removal_efficiency": "92% – 99% Turbidity Reduction (<0.5 NTU effluent)",
                "urgency": "High"
            },
            "Chloramines": {
                "parameter": "Chloramines",
                "condition": "Residual Chloramines (> 2.0 – 4.0 mg/L)",
                "action_title": "Catalytic Carbon Adsorption & De-chloramination",
                "technology": "Catalytic Activated Carbon (CAC) Bed Filter",
                "scientific_mechanism": (
                    "Engineered catalytic active carbon sites chemically break nitrogen-chlorine bonds, "
                    "catalytically reducing chloramines (NH2Cl) into harmless chloride ions (Cl-) and nitrogen gas (N2)."
                ),
                "household_solution": "Point-of-entry catalytic carbon filter or dual carbon block cartridge.",
                "removal_efficiency": "95% – 99% Chloramine Elimination",
                "urgency": "Moderate"
            },
            "Sulfate": {
                "parameter": "Sulfate",
                "condition": "High Sulfate Concentration (> 250 mg/L)",
                "action_title": "Membrane Demineralization / Strong Base Anion Exchange",
                "technology": "Thin-Film Composite RO or Strong Base Anion (SBA) Chloride-Form Resin",
                "scientific_mechanism": (
                    "Divalent sulfate oxyanions (SO4 2-) possess high hydrated ionic radii and strong electrostatic "
                    "repulsion, facilitating near-complete membrane rejection and resin capture."
                ),
                "household_solution": "Under-sink Reverse Osmosis system with pressurized storage tank.",
                "removal_efficiency": "95% – 98% Sulfate Removal",
                "urgency": "Moderate"
            },
            "Conductivity": {
                "parameter": "Conductivity",
                "condition": "High Electrical Conductivity (> 750 µS/cm)",
                "action_title": "Comprehensive Ionic Desalination",
                "technology": "High-Pressure RO or Mixed-Bed Deionization",
                "scientific_mechanism": (
                    "Removes mobile electrolyte ions, eliminating electrical conductance and preventing galvanic corrosion."
                ),
                "household_solution": "Point-of-use multi-barrier Reverse Osmosis system.",
                "removal_efficiency": "90% – 97% Conductivity Reduction",
                "urgency": "Moderate"
            },
            "Organic_carbon": {
                "parameter": "Organic_carbon",
                "condition": "Elevated Total Organic Carbon (> 2.0 – 4.0 mg/L)",
                "action_title": "Granular Activated Carbon & Advanced Oxidation",
                "technology": "Granular Activated Carbon (GAC) + UV/H2O2 Advanced Oxidation Process (AOP)",
                "scientific_mechanism": (
                    "Micro- and meso-porous activated carbon adsorbs natural organic humic acids; hydroxyl radicals (·OH) "
                    "cleave resistant organic molecules, preventing downstream halogenated carcinogen synthesis."
                ),
                "household_solution": "Dense 5-micron solid extruded coconut-shell carbon block filter.",
                "removal_efficiency": "85% – 95% TOC Adsorption",
                "urgency": "High"
            },
            "Trihalomethanes": {
                "parameter": "Trihalomethanes",
                "condition": "Elevated Carcinogenic THMs (> 80 µg/L)",
                "action_title": "Packed-Tower Air Stripping & Sub-Micron Carbon Chemisorption",
                "technology": "Air Stripping Aeration followed by Extruded Carbon Block Filtration",
                "scientific_mechanism": (
                    "High air-to-water ratio volatilizes organic trihalomethanes into the vapor phase, "
                    "while dense activated carbon chemisorbs residual halogenated fractions."
                ),
                "household_solution": "NSF/ANSI 53 certified VOC/THM carbon block filtration unit.",
                "removal_efficiency": "98% – 99.5% THM Eradication",
                "urgency": "Critical"
            },
            "Nitrate": {
                "parameter": "Nitrate",
                "condition": "Elevated Nitrate (> 45 mg/L)",
                "action_title": "Nitrate-Selective Anion Exchange & Reverse Osmosis",
                "technology": "Macroporous Nitrate-Selective Resin or Polyamide RO",
                "scientific_mechanism": (
                    "Quaternary amine resin with triethylamine functional groups preferentially binds monovalent nitrate (NO3-) "
                    "over divalent sulfate, preventing methemoglobinemia risks."
                ),
                "household_solution": "Point-of-use RO purifier or dedicated nitrate resin cartridge.",
                "removal_efficiency": "88% – 96% Nitrate Removal",
                "urgency": "Critical"
            },
            "Fluoride": {
                "parameter": "Fluoride",
                "condition": "Excess Fluoride (> 1.5 mg/L)",
                "action_title": "Activated Alumina Adsorption & Reverse Osmosis",
                "technology": "Activated Alumina (gamma-Al2O3) Bed or Thin-Film RO",
                "scientific_mechanism": (
                    "Fluoride anions chemisorb strongly to coordination sites on porous amphoteric aluminum oxide surfaces."
                ),
                "household_solution": "Activated alumina defluoridation cartridge or multi-stage domestic RO unit.",
                "removal_efficiency": "90% – 97% Fluoride Removal",
                "urgency": "Critical"
            },
            "Dissolved_oxygen": {
                "parameter": "Dissolved_oxygen",
                "condition": "Deficient Dissolved Oxygen (< 5.0 mg/L)",
                "action_title": "Cascade Spray Aeration & Oxygenation",
                "technology": "Venturi Oxygen Injector or Cascade Aeration Tray",
                "scientific_mechanism": (
                    "Increases air-water interfacial contact area, driving oxygen dissolution to saturation equilibrium."
                ),
                "household_solution": "Aerating tap faucet nozzle or storage tank air-diffuser.",
                "removal_efficiency": "Elevates DO to 7.0 – 9.0 mg/L",
                "urgency": "Moderate"
            }
        }

        # Standard 5-Stage Multi-Barrier Treatment Train
        self.treatment_train = [
            {
                "stage_num": 1,
                "stage_name": "Mechanical Depth Pre-Filtration",
                "filter_type": "5-Micron Melt-Blown Spun Polypropylene Cartridge",
                "primary_target": "Suspended silt, rust particles, sand, and macro-colloidal debris",
                "efficiency": "Removes 99% of particles > 5 microns",
                "operational_purpose": "Protects downstream carbon beds and membranes from premature physical fouling."
            },
            {
                "stage_num": 2,
                "stage_name": "Catalytic & Granular Activated Carbon Adsorption",
                "filter_type": "High-Activity Coconut Shell Catalytic Carbon (Acid-Washed)",
                "primary_target": "Chlorine, chloramines, volatile organic compounds (VOCs), THMs, pesticides, odor",
                "efficiency": "Adsorbs 95–99% of organics and eliminates disinfectant residuals",
                "operational_purpose": "Prevents chlorine degradation of thin-film composite polyamide membranes."
            },
            {
                "stage_num": 3,
                "stage_name": "Advanced Membrane Desalination / Softening",
                "filter_type": "Thin-Film Composite (TFC) Reverse Osmosis Membrane (0.0001 µm)",
                "primary_target": "TDS, heavy metals, nitrate, fluoride, sulfate, microbial viruses and bacteria",
                "efficiency": "Rejects 95–99% of dissolved inorganic minerals and multivalent salts",
                "operational_purpose": "Primary physicochemical barrier delivering purified water permeate."
            },
            {
                "stage_num": 4,
                "stage_name": "Germicidal Ultraviolet Photolytic Disinfection",
                "filter_type": "254 nm Short-Wave Low-Pressure Quartz UV Disinfection Chamber",
                "primary_target": "Bacteria, coliforms, enteric viruses, Cryptosporidium, and Giardia cysts",
                "efficiency": "4-Log (99.99%) microbial inactivation at 40 mJ/cm² dose",
                "operational_purpose": "Non-chemical disinfection that destroys microbial DNA without toxic byproducts."
            },
            {
                "stage_num": 5,
                "stage_name": "Post-Carbon Remineralization & Taste Balancing",
                "filter_type": "Natural Calcite & Dolomite Remineralization Cartridge",
                "primary_target": "pH buffering and essential calcium / magnesium electrolyte balance",
                "efficiency": "Elevates TDS by 30–50 mg/L and stabilizes pH to 7.2 – 7.6",
                "operational_purpose": "Prevents pipe leaching from aggressive RO permeate and optimizes drinking palate."
            }
        ]

    def generate_recommendations(self, sample, wawqi_res):
        """
        Analyzes sample parameter violations and prescribes engineering treatment steps.
        """
        violations = wawqi_res.get("violations", [])
        action_items = []
        seen_keys = set()

        for v in violations:
            p_name = v.get("parameter")
            val = float(v.get("measured", 0.0))

            if p_name == "pH":
                key = "pH_acidic" if val < 6.5 else "pH_alkaline"
            else:
                key = p_name

            if key in self.solutions_catalog and key not in seen_keys:
                seen_keys.add(key)
                sol = dict(self.solutions_catalog[key])
                if v.get("severity") == "Critical":
                    sol["urgency"] = "Critical"
                action_items.append(sol)

        # Determine potability status and operational guidance
        if not action_items:
            verdict = "Potable - Safe for Direct Consumption"
            guidance = "Water complies with all tested physicochemical limits (BIS IS 10500:2012 / WHO). Routine sanitation is sufficient."
            potability_class = "potable"
        elif len(action_items) <= 2 and all(item["urgency"] != "Critical" for item in action_items):
            verdict = "Marginal - Requires Point-of-Use Filtration"
            guidance = f"Detected {len(action_items)} parameter breach(es). Minor corrective filtration is required before direct drinking."
            potability_class = "marginal"
        else:
            verdict = "Non-Potable - Unfit for Consumption Without Multi-Barrier Treatment"
            guidance = f"Detected {len(action_items)} chemical violation(s). Advanced engineering treatment is necessary to avert health risks."
            potability_class = "non-potable"

        return {
            "verdict": verdict,
            "potability_class": potability_class,
            "guidance": guidance,
            "action_items_count": len(action_items),
            "action_items": action_items,
            "multi_barrier_train": self.treatment_train
        }

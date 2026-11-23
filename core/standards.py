"""
Multi-Standard Physicochemical Drinking Water Database and Index Classification Tiers.
Harmonized across:
  - Bureau of Indian Standards (BIS IS 10500:2012, Second Revision)
  - World Health Organization (WHO Guidelines for Drinking-water Quality, 4th Edition)
  - United States Environmental Protection Agency (US EPA National Primary & Secondary Standards)
  - European Union Drinking Water Directive (EU Directive 2020/2184)
"""

# Core water quality parameter definitions, limits, and toxicological / operational significance
DRINKING_WATER_STANDARDS = {
    "pH": {
        "name": "pH (Acidity / Alkalinity)",
        "unit": "pH units",
        "category": "Physicochemical",
        "bis_acceptable": 6.5,
        "bis_permissible": 8.5,
        "who_guideline": 8.5,
        "epa_secondary": 8.5,
        "eu_standard": 9.5,
        "standard": 8.5,
        "acceptable_min": 6.5,
        "acceptable_max": 8.5,
        "ideal": 7.0,
        "description": "Negative logarithm of hydrogen ion activity; indicator of acidic or basic nature.",
        "hazard": "Acidic water (<6.5) corrodes pipes and leaches heavy metals; alkaline water (>8.5) causes incrustation and bitter taste."
    },
    "Hardness": {
        "name": "Total Hardness (as CaCO3)",
        "unit": "mg/L",
        "category": "Mineral Balance",
        "bis_acceptable": 200.0,
        "bis_permissible": 300.0,
        "who_guideline": 300.0,
        "epa_secondary": 250.0,
        "eu_standard": 250.0,
        "standard": 300.0,
        "acceptable_min": 0.0,
        "acceptable_max": 200.0,
        "ideal": 0.0,
        "description": "Total concentration of polyvalent metallic cations, primarily calcium and magnesium.",
        "hazard": "Precipitates mineral scale in pipes and boilers, impairs soap lathering; risk factor for kidney stone formation in sensitive individuals."
    },
    "Solids": {
        "name": "Total Dissolved Solids (TDS)",
        "unit": "mg/L",
        "category": "Mineral Balance",
        "bis_acceptable": 500.0,
        "bis_permissible": 1000.0,
        "who_guideline": 600.0,
        "epa_secondary": 500.0,
        "eu_standard": 1000.0,
        "standard": 500.0,
        "acceptable_min": 0.0,
        "acceptable_max": 500.0,
        "ideal": 0.0,
        "description": "Total combined mass of all dissolved organic and inorganic mineral substances.",
        "hazard": "Imparts bitter, brackish, or salty taste; causes gastrointestinal irritation and high osmotic load."
    },
    "Turbidity": {
        "name": "Turbidity / Cloudiness",
        "unit": "NTU",
        "category": "Physical",
        "bis_acceptable": 1.0,
        "bis_permissible": 5.0,
        "who_guideline": 5.0,
        "epa_secondary": 1.0,
        "eu_standard": 1.0,
        "standard": 5.0,
        "acceptable_min": 0.0,
        "acceptable_max": 1.0,
        "ideal": 0.0,
        "description": "Optical clarity measurement caused by suspended inorganic clay, silt, and colloidal organics.",
        "hazard": "Suspended colloids shield enteric pathogens from UV and chemical disinfection, harboring microbial bacteria."
    },
    "Chloramines": {
        "name": "Chloramines / Disinfectant Residual",
        "unit": "mg/L",
        "category": "Disinfection",
        "bis_acceptable": 2.0,
        "bis_permissible": 4.0,
        "who_guideline": 3.0,
        "epa_secondary": 4.0,
        "eu_standard": 3.0,
        "standard": 4.0,
        "acceptable_min": 0.0,
        "acceptable_max": 2.0,
        "ideal": 0.0,
        "description": "Residual chlorine disinfectant bound with ammonia to maintain distribution line biostability.",
        "hazard": "Elevated concentrations produce strong chlorinous odors, irritate mucous membranes, and present hemolytic risks to dialysis patients."
    },
    "Sulfate": {
        "name": "Sulfate (SO4 2-)",
        "unit": "mg/L",
        "category": "Inorganics",
        "bis_acceptable": 200.0,
        "bis_permissible": 250.0,
        "who_guideline": 250.0,
        "epa_secondary": 250.0,
        "eu_standard": 250.0,
        "standard": 250.0,
        "acceptable_min": 0.0,
        "acceptable_max": 200.0,
        "ideal": 0.0,
        "description": "Major naturally occurring divalent anion formed by leaching of gypsum and sedimentary rock formations.",
        "hazard": "Exerts a distinct laxative and cathartic physiological response in unacclimated consumers, potentially inducing dehydration."
    },
    "Conductivity": {
        "name": "Electrical Conductivity (EC)",
        "unit": "µS/cm",
        "category": "Physical",
        "bis_acceptable": 300.0,
        "bis_permissible": 750.0,
        "who_guideline": 750.0,
        "epa_secondary": 500.0,
        "eu_standard": 2500.0,
        "standard": 750.0,
        "acceptable_min": 0.0,
        "acceptable_max": 300.0,
        "ideal": 0.0,
        "description": "Ability of aqueous solution to conduct electric current, directly proportional to dissolved ionic strength.",
        "hazard": "Reflects elevated mineral salinity, accelerates metallic plumbing galvanic corrosion, and indicates electrolyte imbalance."
    },
    "Organic_carbon": {
        "name": "Total Organic Carbon (TOC)",
        "unit": "mg/L",
        "category": "Organics",
        "bis_acceptable": 2.0,
        "bis_permissible": 4.0,
        "who_guideline": 4.0,
        "epa_secondary": 2.0,
        "eu_standard": 2.0,
        "standard": 4.0,
        "acceptable_min": 0.0,
        "acceptable_max": 2.0,
        "ideal": 0.0,
        "description": "Quantification of all covalently bound organic matter in natural dissolved humic substances.",
        "hazard": "Primary chemical precursor that reacts with chlorine during municipal disinfection to yield toxic, carcinogenic organohalides."
    },
    "Trihalomethanes": {
        "name": "Trihalomethanes (THMs)",
        "unit": "µg/L",
        "category": "Disinfection Byproducts",
        "bis_acceptable": 80.0,
        "bis_permissible": 80.0,
        "who_guideline": 100.0,
        "epa_secondary": 80.0,
        "eu_standard": 100.0,
        "standard": 80.0,
        "acceptable_min": 0.0,
        "acceptable_max": 80.0,
        "ideal": 0.0,
        "description": "Volatile halogenated disinfection byproducts, including chloroform, bromoform, and dibromochloromethane.",
        "hazard": "Known mammalian carcinogens linked with increased statistical incidences of bladder, liver, and colorectal cancers upon chronic exposure."
    },
    "Nitrate": {
        "name": "Nitrate (NO3-)",
        "unit": "mg/L",
        "category": "Inorganics",
        "bis_acceptable": 45.0,
        "bis_permissible": 45.0,
        "who_guideline": 50.0,
        "epa_secondary": 45.0,
        "eu_standard": 50.0,
        "standard": 45.0,
        "acceptable_min": 0.0,
        "acceptable_max": 45.0,
        "ideal": 0.0,
        "description": "Inorganic oxyanion originating from synthetic nitrogen fertilizers, animal feedlots, and domestic septic seepage.",
        "hazard": "Causes methemoglobinemia (infant 'blue baby syndrome') by binding fetal hemoglobin, and forms carcinogenic N-nitroso compounds."
    },
    "Fluoride": {
        "name": "Fluoride (F-)",
        "unit": "mg/L",
        "category": "Inorganics",
        "bis_acceptable": 1.0,
        "bis_permissible": 1.5,
        "who_guideline": 1.5,
        "epa_secondary": 2.0,
        "eu_standard": 1.5,
        "standard": 1.5,
        "acceptable_min": 0.5,
        "acceptable_max": 1.0,
        "ideal": 0.7,
        "description": "Halogen ion beneficial at trace levels for enamel caries resistance, but toxic at higher concentrations.",
        "hazard": "Concentrations above 1.5 mg/L cause irreversible dental fluorosis, while chronic exposure >3.0 mg/L induces severe crippling skeletal fluorosis."
    },
    "Dissolved_oxygen": {
        "name": "Dissolved Oxygen (DO)",
        "unit": "mg/L",
        "category": "Physical",
        "bis_acceptable": 5.0,
        "bis_permissible": 4.0,
        "who_guideline": 5.0,
        "epa_secondary": 5.0,
        "eu_standard": 5.0,
        "standard": 5.0,
        "acceptable_min": 5.0,
        "acceptable_max": 14.0,
        "ideal": 14.6,
        "description": "Concentration of free, non-compound molecular oxygen dissolved in the aqueous phase.",
        "hazard": "Low DO (<4.0 mg/L) indicates high biochemical oxygen demand, organic putrefaction, septic conditions, and anaerobic bacterial growth."
    },
    "Alkalinity": {
        "name": "Total Alkalinity (as CaCO3)",
        "unit": "mg/L",
        "category": "Mineral Balance",
        "bis_acceptable": 200.0,
        "bis_permissible": 600.0,
        "who_guideline": 200.0,
        "epa_secondary": 200.0,
        "eu_standard": 200.0,
        "standard": 200.0,
        "acceptable_min": 30.0,
        "acceptable_max": 200.0,
        "ideal": 100.0,
        "description": "Acid-neutralizing capacity of water, primarily governed by bicarbonate, carbonate, and hydroxide ions.",
        "hazard": "Low alkalinity (<30 mg/L) causes corrosive, unstable water; high alkalinity (>200 mg/L) causes pipe scale and bitter chemical taste."
    },
    "Chloride": {
        "name": "Chloride (Cl-)",
        "unit": "mg/L",
        "category": "Inorganics",
        "bis_acceptable": 250.0,
        "bis_permissible": 1000.0,
        "who_guideline": 250.0,
        "epa_secondary": 250.0,
        "eu_standard": 250.0,
        "standard": 250.0,
        "acceptable_min": 0.0,
        "acceptable_max": 250.0,
        "ideal": 0.0,
        "description": "Prevalent monovalent anion resulting from natural mineral dissolution, seawater intrusion, and highway deicing.",
        "hazard": "Imparts a noticeable salty taste, accelerates pitting corrosion in stainless steel, and increases cardiovascular sodium burden."
    }
}

# Weighted Arithmetic Water Quality Index (WAWQI) Grading Scale
WAWQI_CATEGORIES = [
    {
        "min": 0.0,
        "max": 25.0,
        "grade": "Grade A",
        "status": "Excellent Water Quality",
        "color": "#10B981",
        "badge_class": "badge-excellent",
        "potability": "Completely Potable",
        "suitability": "Pristine drinking source. Safe for direct consumption with minimal disinfection."
    },
    {
        "min": 25.01,
        "max": 50.0,
        "grade": "Grade B",
        "status": "Good Water Quality",
        "color": "#3B82F6",
        "badge_class": "badge-good",
        "potability": "Potable",
        "suitability": "Suitable for municipal consumption and domestic use following conventional filtration."
    },
    {
        "min": 50.01,
        "max": 75.0,
        "grade": "Grade C",
        "status": "Poor Water Quality",
        "color": "#F59E0B",
        "badge_class": "badge-poor",
        "potability": "Doubtful Potability",
        "suitability": "Unsatisfactory for direct drinking. Requires coagulation, flocculation, and dual-media filtration."
    },
    {
        "min": 75.01,
        "max": 100.0,
        "grade": "Grade D",
        "status": "Very Poor Water Quality",
        "color": "#EF4444",
        "badge_class": "badge-very-poor",
        "potability": "Non-Potable",
        "suitability": "Severe contamination. Safe consumption requires advanced membrane separation (Reverse Osmosis)."
    },
    {
        "min": 100.01,
        "max": float("inf"),
        "grade": "Grade E",
        "status": "Unsuitable for Drinking",
        "color": "#7F1D1D",
        "badge_class": "badge-unsuitable",
        "potability": "Hazardous / Toxic",
        "suitability": "Grossly degraded aquatic matrix. Poses acute physiological health risks; unfit for human consumption."
    }
]

# Canadian Council of Ministers of the Environment (CCME) WQI Grading Scale
CCME_CATEGORIES = [
    {
        "min": 95.0,
        "max": 100.0,
        "status": "Excellent",
        "color": "#10B981",
        "description": "Water quality is protected with a virtual absence of threat or impairment; conditions very close to natural or pristine levels."
    },
    {
        "min": 80.0,
        "max": 94.99,
        "status": "Good",
        "color": "#3B82F6",
        "description": "Conditions rarely depart from desirable levels; only minor degree of threat or impairment detected."
    },
    {
        "min": 65.0,
        "max": 79.99,
        "status": "Fair",
        "color": "#F59E0B",
        "description": "Conditions sometimes depart from natural or desirable levels; quality is occasionally compromised."
    },
    {
        "min": 45.0,
        "max": 64.99,
        "status": "Marginal",
        "color": "#F97316",
        "description": "Conditions frequently depart from desirable levels; quality is degraded and potential health threats exist."
    },
    {
        "min": 0.0,
        "max": 44.99,
        "status": "Poor",
        "color": "#EF4444",
        "description": "Conditions persistently depart from acceptable levels; water quality is severely impaired and unpotable."
    }
]

# Realistic Preset Water Samples across Diverse Ecological & Domestic Typologies
WATER_PRESETS = {
    "Municipal Treated Tap Water": {
        "pH": 7.20,
        "Hardness": 180.0,
        "Solids": 320.0,
        "Turbidity": 1.2,
        "Chloramines": 2.10,
        "Sulfate": 180.0,
        "Conductivity": 380.0,
        "Organic_carbon": 2.00,
        "Trihalomethanes": 45.0,
        "Nitrate": 18.0,
        "Fluoride": 0.85,
        "Dissolved_oxygen": 7.4,
        "Alkalinity": 120.0,
        "Chloride": 85.0
    },
    "Deep Borewell Groundwater (Hard Water)": {
        "pH": 7.85,
        "Hardness": 420.0,
        "Solids": 880.0,
        "Turbidity": 2.8,
        "Chloramines": 0.30,
        "Sulfate": 290.0,
        "Conductivity": 820.0,
        "Organic_carbon": 1.60,
        "Trihalomethanes": 12.0,
        "Nitrate": 35.0,
        "Fluoride": 1.80,
        "Dissolved_oxygen": 5.2,
        "Alkalinity": 280.0,
        "Chloride": 210.0
    },
    "Surface River Water (Monsoon High Turbidity)": {
        "pH": 7.40,
        "Hardness": 140.0,
        "Solids": 240.0,
        "Turbidity": 9.8,
        "Chloramines": 0.10,
        "Sulfate": 110.0,
        "Conductivity": 290.0,
        "Organic_carbon": 6.20,
        "Trihalomethanes": 8.0,
        "Nitrate": 22.0,
        "Fluoride": 0.40,
        "Dissolved_oxygen": 6.8,
        "Alkalinity": 95.0,
        "Chloride": 60.0
    },
    "Industrial Effluent Contaminated Groundwater": {
        "pH": 5.15,
        "Hardness": 520.0,
        "Solids": 1780.0,
        "Turbidity": 7.2,
        "Chloramines": 4.90,
        "Sulfate": 490.0,
        "Conductivity": 1350.0,
        "Organic_carbon": 7.80,
        "Trihalomethanes": 125.0,
        "Nitrate": 68.0,
        "Fluoride": 2.40,
        "Dissolved_oxygen": 3.1,
        "Alkalinity": 340.0,
        "Chloride": 480.0
    },
    "Commercial Reverse Osmosis (RO) Bottled Water": {
        "pH": 6.95,
        "Hardness": 45.0,
        "Solids": 75.0,
        "Turbidity": 0.3,
        "Chloramines": 0.05,
        "Sulfate": 25.0,
        "Conductivity": 95.0,
        "Organic_carbon": 0.50,
        "Trihalomethanes": 3.0,
        "Nitrate": 4.0,
        "Fluoride": 0.30,
        "Dissolved_oxygen": 8.2,
        "Alkalinity": 35.0,
        "Chloride": 18.0
    },
    "Coastal Saline Aquifer (Seawater Intrusion)": {
        "pH": 8.10,
        "Hardness": 610.0,
        "Solids": 2150.0,
        "Turbidity": 3.4,
        "Chloramines": 0.20,
        "Sulfate": 420.0,
        "Conductivity": 1980.0,
        "Organic_carbon": 2.80,
        "Trihalomethanes": 22.0,
        "Nitrate": 28.0,
        "Fluoride": 1.20,
        "Dissolved_oxygen": 5.6,
        "Alkalinity": 310.0,
        "Chloride": 920.0
    },
    "Agricultural Runoff (High Nitrate & Organics)": {
        "pH": 7.65,
        "Hardness": 260.0,
        "Solids": 640.0,
        "Turbidity": 5.6,
        "Chloramines": 0.15,
        "Sulfate": 190.0,
        "Conductivity": 620.0,
        "Organic_carbon": 5.40,
        "Trihalomethanes": 16.0,
        "Nitrate": 78.0,
        "Fluoride": 1.10,
        "Dissolved_oxygen": 4.5,
        "Alkalinity": 170.0,
        "Chloride": 140.0
    }
}

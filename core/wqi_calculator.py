"""
Comprehensive Multi-Index Water Quality Modeling & Eclipsing Diagnostic Engine.
Includes:
  1. Weighted Arithmetic Water Quality Index (WAWQI - Brown et al. 1970, Horton 1965)
  2. Canadian Council of Ministers of the Environment WQI (CCME WQI 1.0)
  3. National Sanitation Foundation WQI (NSF-WQI Additive & Multiplicative)
  4. Mathematical Eclipsing & Ambiguity Diagnostic Engine
"""

import math
from .standards import DRINKING_WATER_STANDARDS, WAWQI_CATEGORIES, CCME_CATEGORIES


class MultiWQIEngine:
    """Calculates multiple standardized environmental water quality indices and performs eclipsing analysis."""

    def __init__(self, standards=None):
        self.standards = standards or DRINKING_WATER_STANDARDS
        self.wawqi_weights = self._compute_wawqi_weights()

    def _compute_wawqi_weights(self):
        """
        Calculates unit weights (Wi) inversely proportional to permissible standard limits (Si):
        K = 1 / sum(1 / Si)
        Wi = K / Si, ensuring sum(Wi) = 1.0000
        """
        inv_sum = sum(1.0 / p_info["standard"] for p_info in self.standards.values())
        k = 1.0 / inv_sum if inv_sum > 0 else 1.0
        weights = {}
        for param, p_info in self.standards.items():
            weights[param] = k / p_info["standard"]
        return weights

    @staticmethod
    def normalize_key(key):
        """Normalizes parameter dictionary key names to match internal naming."""
        clean = key.strip().lower().replace(" ", "_").replace("-", "_")
        mapping = {
            "ph": "pH",
            "hardness": "Hardness",
            "total_hardness": "Hardness",
            "solids": "Solids",
            "tds": "Solids",
            "total_dissolved_solids": "Solids",
            "turbidity": "Turbidity",
            "chloramines": "Chloramines",
            "chlorine": "Chloramines",
            "sulfate": "Sulfate",
            "so4": "Sulfate",
            "conductivity": "Conductivity",
            "ec": "Conductivity",
            "electrical_conductivity": "Conductivity",
            "organic_carbon": "Organic_carbon",
            "toc": "Organic_carbon",
            "trihalomethanes": "Trihalomethanes",
            "thms": "Trihalomethanes",
            "nitrate": "Nitrate",
            "no3": "Nitrate",
            "fluoride": "Fluoride",
            "f": "Fluoride",
            "dissolved_oxygen": "Dissolved_oxygen",
            "do": "Dissolved_oxygen",
            "alkalinity": "Alkalinity",
            "total_alkalinity": "Alkalinity",
            "chloride": "Chloride",
            "cl": "Chloride"
        }
        return mapping.get(clean, key)

    def prepare_sample(self, raw_sample):
        """Prepares and validates input parameter values."""
        normalized = {}
        for k, v in raw_sample.items():
            norm_k = self.normalize_key(str(k))
            try:
                normalized[norm_k] = float(v)
            except (ValueError, TypeError):
                continue
        return normalized

    # -------------------------------------------------------------------------
    # 1. WEIGHTED ARITHMETIC WATER QUALITY INDEX (WAWQI)
    # -------------------------------------------------------------------------
    def calculate_wawqi(self, sample):
        """
        Computes the Weighted Arithmetic Water Quality Index (WAWQI).
        
        Returns:
            dict containing:
              - score: Final aggregated index score
              - grade: Grade tier (A to E)
              - category: Matching metadata dict
              - violations: Detailed list of parameter guideline violations
              - sub_indices: Sub-index ratings (qi), unit weights (Wi), and weighted products
        """
        norm_sample = self.prepare_sample(sample)
        sub_indices = {}
        violations = []
        wqi = 0.0

        for param, p_info in self.standards.items():
            std_val = p_info["standard"]
            unit = p_info.get("unit", "")
            val = norm_sample.get(param, p_info.get("ideal", 0.0))
            wi = self.wawqi_weights.get(param, 0.0)

            # Sub-index / Quality Rating (qi)
            if param == "pH":
                # Optimal pH is 7.0; permissible window is 6.5 to 8.5
                if val >= 7.0:
                    qi = ((val - 7.0) / (8.5 - 7.0)) * 100.0
                else:
                    qi = ((7.0 - val) / (7.0 - 6.5)) * 100.0

                if val < 6.5 or val > 8.5:
                    severity = "Critical" if (val < 5.5 or val > 9.5) else "High"
                    violations.append({
                        "parameter": param,
                        "name": p_info["name"],
                        "measured": round(val, 2),
                        "unit": unit,
                        "limit": "6.5 – 8.5",
                        "severity": severity,
                        "hazard": p_info["hazard"]
                    })
            elif param == "Dissolved_oxygen":
                # For DO, higher is better (ideal saturation is 14.6 mg/L, minimum threshold is 5.0 mg/L)
                ideal_do = 14.6
                std_do = 5.0
                qi = ((ideal_do - val) / (ideal_do - std_do)) * 100.0
                if val < 5.0:
                    severity = "Critical" if val < 3.0 else "High"
                    violations.append({
                        "parameter": param,
                        "name": p_info["name"],
                        "measured": round(val, 2),
                        "unit": unit,
                        "limit": "≥ 5.0 mg/L",
                        "severity": severity,
                        "hazard": p_info["hazard"]
                    })
            else:
                qi = (val / std_val) * 100.0
                if val > std_val:
                    if val > (std_val * 2.0):
                        severity = "Critical"
                    elif val > (std_val * 1.3):
                        severity = "High"
                    else:
                        severity = "Moderate"
                    violations.append({
                        "parameter": param,
                        "name": p_info["name"],
                        "measured": round(val, 2),
                        "unit": unit,
                        "limit": f"≤ {std_val} {unit}".strip(),
                        "severity": severity,
                        "hazard": p_info["hazard"]
                    })

            weighted_qi = wi * qi
            wqi += weighted_qi

            sub_indices[param] = {
                "name": p_info["name"],
                "value": round(val, 2),
                "standard": std_val,
                "unit": unit,
                "qi": round(qi, 2),
                "wi": round(wi, 5),
                "weighted_qi": round(weighted_qi, 3)
            }

        wqi = round(wqi, 2)

        # Match category grade
        matched_cat = WAWQI_CATEGORIES[-1]
        for cat in WAWQI_CATEGORIES:
            if cat["min"] <= wqi <= cat["max"]:
                matched_cat = cat
                break

        return {
            "score": wqi,
            "grade": matched_cat["grade"],
            "status": matched_cat["status"],
            "color": matched_cat["color"],
            "potability": matched_cat["potability"],
            "suitability": matched_cat["suitability"],
            "violation_count": len(violations),
            "violations": violations,
            "sub_indices": sub_indices
        }

    # -------------------------------------------------------------------------
    # 2. CANADIAN COUNCIL OF MINISTERS OF THE ENVIRONMENT (CCME) WQI
    # -------------------------------------------------------------------------
    def calculate_ccme_wqi(self, sample):
        """
        Calculates the CCME Water Quality Index using the official 3-factor formulation:
          F1 (Scope): % of failed variables
          F2 (Frequency): % of failed tests
          F3 (Amplitude): normalized sum of excursions (nse)
          CCME WQI = 100 - [ sqrt(F1^2 + F2^2 + F3^2) / 1.732 ]
        """
        norm_sample = self.prepare_sample(sample)
        total_tests = len(self.standards)
        failed_tests = 0
        excursions = []

        for param, p_info in self.standards.items():
            std_val = p_info["standard"]
            val = norm_sample.get(param, p_info.get("ideal", 0.0))

            if param == "pH":
                if val > 8.5:
                    excursion = (val / 8.5) - 1.0
                    excursions.append(excursion)
                    failed_tests += 1
                elif val < 6.5:
                    excursion = (6.5 / max(val, 0.1)) - 1.0
                    excursions.append(excursion)
                    failed_tests += 1
            elif param == "Dissolved_oxygen":
                if val < 5.0:
                    excursion = (5.0 / max(val, 0.1)) - 1.0
                    excursions.append(excursion)
                    failed_tests += 1
            else:
                if val > std_val:
                    excursion = (val / std_val) - 1.0
                    excursions.append(excursion)
                    failed_tests += 1

        # Scope: F1
        f1 = (failed_tests / total_tests) * 100.0 if total_tests > 0 else 0.0
        # Frequency: F2 (for a single multi-parameter grab sample, F2 equals F1)
        f2 = f1
        # Amplitude: F3
        if excursions:
            nse = sum(excursions) / total_tests
            f3 = (nse / (0.01 * nse + 0.01))
            f3 = min(f3, 100.0)
        else:
            f3 = 0.0

        vector_length = math.sqrt((f1 ** 2) + (f2 ** 2) + (f3 ** 2))
        ccme_score = round(100.0 - (vector_length / 1.732), 2)
        ccme_score = max(0.0, min(100.0, ccme_score))

        # Match CCME category
        matched_ccme = CCME_CATEGORIES[-1]
        for cat in CCME_CATEGORIES:
            if cat["min"] <= ccme_score <= cat["max"]:
                matched_ccme = cat
                break

        return {
            "score": ccme_score,
            "status": matched_ccme["status"],
            "color": matched_ccme["color"],
            "description": matched_ccme["description"],
            "f1_scope": round(f1, 2),
            "f2_frequency": round(f2, 2),
            "f3_amplitude": round(f3, 2),
            "failed_tests": failed_tests,
            "total_tests": total_tests
        }

    # -------------------------------------------------------------------------
    # 3. NATIONAL SANITATION FOUNDATION (NSF) WQI
    # -------------------------------------------------------------------------
    def calculate_nsf_wqi(self, sample):
        """
        Calculates the NSF-WQI using standard sub-index quality curves and normalized weights.
        Returns additive (0-100) and multiplicative scores.
        """
        norm_sample = self.prepare_sample(sample)
        
        # NSF parameter weights (normalized for available parameters)
        nsf_weights = {
            "pH": 0.11,
            "Turbidity": 0.08,
            "Dissolved_oxygen": 0.17,
            "Solids": 0.07,
            "Nitrate": 0.10,
            "Sulfate": 0.07,
            "Hardness": 0.08,
            "Chloramines": 0.10,
            "Conductivity": 0.08,
            "Organic_carbon": 0.14
        }
        total_w = sum(nsf_weights.values())
        norm_weights = {k: v / total_w for k, v in nsf_weights.items()}

        additive_score = 0.0
        multiplicative_score = 1.0

        for param, w in norm_weights.items():
            val = norm_sample.get(param, 0.0)
            
            # Approximate standard NSF sub-index curve mapping (0 to 100)
            if param == "pH":
                # Curve peaks at 7.0-7.5 (100) and drops sharply below 5 and above 9
                deviation = abs(val - 7.2)
                qi = max(10.0, 100.0 - (deviation * 28.0))
            elif param == "Dissolved_oxygen":
                # 100% saturation (~9-10 mg/L) gives near 100
                qi = min(100.0, val * 10.5)
            elif param == "Turbidity":
                qi = max(10.0, 100.0 - (val * 9.5))
            elif param == "Solids":
                qi = max(10.0, 100.0 - (val / 12.0))
            elif param == "Nitrate":
                qi = max(10.0, 100.0 - (val * 1.5))
            else:
                std_val = self.standards[param]["standard"]
                ratio = val / std_val
                qi = max(10.0, 100.0 - (ratio * 40.0))

            qi = max(1.0, min(100.0, qi))
            additive_score += w * qi
            multiplicative_score *= (qi ** w)

        return {
            "additive_score": round(additive_score, 2),
            "multiplicative_score": round(multiplicative_score, 2)
        }

    # -------------------------------------------------------------------------
    # 4. ECLIPSING & AMBIGUITY DIAGNOSTIC ENGINE
    # -------------------------------------------------------------------------
    def analyze_eclipsing_and_ambiguity(self, sample, wawqi_res, ccme_res):
        """
        Mathematically diagnoses two classic environmental indexing paradoxes:
          1. Eclipsing: An aggregate index shows 'Good' or 'Acceptable' water quality,
             even though one or more dangerous contaminants severely breach critical limits.
          2. Ambiguity: An aggregate index penalizes water into 'Poor' status, even though
             no single chemical parameter exceeds statutory thresholds.
        """
        violations = wawqi_res.get("violations", [])
        wawqi_score = wawqi_res.get("score", 0.0)
        grade = wawqi_res.get("grade", "")
        critical_violations = [v for v in violations if v.get("severity") == "Critical"]
        high_violations = [v for v in violations if v.get("severity") == "High"]

        is_eclipsed = False
        eclipsing_severity = "None"
        eclipsing_notes = []

        # Calculate max parameter sub-index (qi) and Eclipsing Ratio
        max_qi = 0.0
        max_param = ""
        for p, data in wawqi_res.get("sub_indices", {}).items():
            if data["qi"] > max_qi:
                max_qi = data["qi"]
                max_param = data.get("name", p)

        eclipsing_ratio = round(max_qi / max(wawqi_score, 1.0), 2)

        # Condition for Eclipsing:
        # Case 1: Grade A or B, but has violations
        # Case 2: Grade C or D, but individual critical breach exceeds limit by >50% (qi > 150) with high eclipsing ratio
        if grade in ["Grade A", "Grade B"] and len(violations) > 0:
            is_eclipsed = True
            if len(critical_violations) > 0:
                eclipsing_severity = "Severe Eclipsing Hazard"
                eclipsing_notes.append(
                    f"CRITICAL ECLIPSING: Water is indexed as '{grade} ({wawqi_res['status']})', "
                    f"yet possesses {len(critical_violations)} Critical breach(es) "
                    f"({', '.join(v['parameter'] for v in critical_violations)}). "
                    f"The low arithmetic unit weight assigned to high-threshold parameters hides true toxicity."
                )
            else:
                eclipsing_severity = "Moderate Eclipsing"
                eclipsing_notes.append(
                    f"MODERATE ECLIPSING: Water is ranked '{grade}', but violates "
                    f"{len(violations)} parameter(s) ({', '.join(v['parameter'] for v in violations)}). "
                    f"Composite averaging masks single-analyte non-compliance."
                )
        elif len(violations) > 0 and (max_qi >= 150.0 or eclipsing_ratio >= 1.8):
            is_eclipsed = True
            eclipsing_severity = "Parameter Excursion Eclipsing"
            eclipsing_notes.append(
                f"PARAMETER ECLIPSING: Individual contaminant ({max_param}) rating reaches qi = {max_qi:.1f}, "
                f"which is significantly higher than the composite WAWQI of {wawqi_score:.1f} (Eclipsing Ratio: {eclipsing_ratio}). "
                f"Arithmetic averaging dilutes the acute severity of the dominant contaminant."
            )

        # Condition for Ambiguity: Grade D or E, but zero or only 1 minor violation
        is_ambiguous = False
        if grade in ["Grade D", "Grade E"] and len(violations) <= 1:
            is_ambiguous = True
            eclipsing_notes.append(
                f"INDEX AMBIGUITY: Water scored high index ({wawqi_score}) due to cumulative minor shifts, "
                f"despite only {len(violations)} guideline violation(s)."
            )

        return {
            "is_eclipsed": is_eclipsed,
            "is_ambiguous": is_ambiguous,
            "eclipsing_severity": eclipsing_severity,
            "eclipsing_ratio": eclipsing_ratio,
            "max_parameter_sub_index": max_qi,
            "max_parameter_name": max_param,
            "diagnostic_notes": eclipsing_notes
        }

    # -------------------------------------------------------------------------
    # UNIFIED EXECUTION
    # -------------------------------------------------------------------------
    def evaluate_all(self, sample):
        """Runs the complete multi-index pipeline and diagnostic checks."""
        wawqi_res = self.calculate_wawqi(sample)
        ccme_res = self.calculate_ccme_wqi(sample)
        nsf_res = self.calculate_nsf_wqi(sample)
        eclipsing_res = self.analyze_eclipsing_and_ambiguity(sample, wawqi_res, ccme_res)

        return {
            "wawqi": wawqi_res,
            "ccme": ccme_res,
            "nsf": nsf_res,
            "eclipsing": eclipsing_res
        }

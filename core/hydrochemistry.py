"""
Hydrochemical Water Stability, Corrosivity, and Mineral Scaling Diagnostic Engine.
Calculates established environmental chemical indices:
  1. Langelier Saturation Index (LSI) - Carbonate equilibrium and corrosion tendency
  2. Ryznar Stability Index (RSI) - Empirical scaling vs corrosion predictor
  3. Puckorius Scaling Index (PSI) - High-buffering equilibrium index
  4. Aggressiveness Index (AI) - Asbestos-cement and metal conduit corrosion
  5. Sodium Adsorption Ratio (SAR) - Irrigation and soil permeability hazard
  6. Magnesium Adsorption Ratio / Hazard (MAR) - Divalent cation imbalance
"""

import math


class HydrochemistryEngine:
    """Computes water chemical stability, corrosivity, and mineral precipitation potential."""

    def __init__(self):
        pass

    def calculate_corrosivity_and_scaling(self, sample, water_temp_c=25.0):
        """
        Calculates LSI, RSI, PSI, and AI based on standard carbonate equilibrium formulas.

        Args:
            sample (dict): Water parameters containing pH, Solids (TDS), Hardness, Alkalinity.
            water_temp_c (float): Water temperature in degrees Celsius (default: 25°C).

        Returns:
            dict containing calculated indices, interpretation, and mitigation recommendations.
        """
        ph = float(sample.get("pH", 7.2))
        tds = max(float(sample.get("Solids", 350.0)), 10.0)
        total_hardness = max(float(sample.get("Hardness", 180.0)), 10.0)
        alkalinity = max(float(sample.get("Alkalinity", 120.0)), 10.0)

        # Standard approximation: Calcium hardness constitutes ~70% of total hardness in typical natural waters
        calcium_hardness = total_hardness * 0.70

        # Calculation of pHs (saturation pH for CaCO3):
        # pHs = (9.3 + A + B) - (C + D)
        # Factor A: (log10(TDS) - 1) / 10
        factor_a = (math.log10(tds) - 1.0) / 10.0

        # Factor B: Temperature correction factor
        # B = -13.12 * log10(Temp_C + 273.15) + 34.55
        temp_k = water_temp_c + 273.15
        factor_b = -13.12 * math.log10(temp_k) + 34.55

        # Factor C: log10(Calcium as CaCO3) - 0.4
        factor_c = math.log10(max(calcium_hardness, 1.0)) - 0.4

        # Factor D: log10(Total Alkalinity as CaCO3)
        factor_d = math.log10(max(alkalinity, 1.0))

        ph_s = (9.3 + factor_a + factor_b) - (factor_c + factor_d)
        ph_s = round(ph_s, 2)

        # 1. Langelier Saturation Index (LSI)
        lsi = round(ph - ph_s, 2)
        if lsi > 0.5:
            lsi_status = "Scale-Forming (Supersaturated)"
            lsi_color = "#EF4444"
            lsi_action = "Water will precipitate calcium carbonate, coating pipes, heating elements, and water heaters."
        elif lsi < -0.5:
            lsi_status = "Corrosive / Aggressive (Undersaturated)"
            lsi_color = "#F59E0B"
            lsi_action = "Water dissolves protective mineral lining, leaching toxic heavy metals (Pb, Cu, Fe) from plumbing into drinking water."
        else:
            lsi_status = "Balanced / Non-Corrosive"
            lsi_color = "#10B981"
            lsi_action = "Water is in chemical equilibrium with calcium carbonate; minimal scaling or corrosion expected."

        # 2. Ryznar Stability Index (RSI)
        rsi = round(2.0 * ph_s - ph, 2)
        if rsi < 5.5:
            rsi_status = "Heavy Scale Formation"
            rsi_color = "#EF4444"
        elif 5.5 <= rsi < 6.2:
            rsi_status = "Moderate Scaling Tendency"
            rsi_color = "#F59E0B"
        elif 6.2 <= rsi <= 6.8:
            rsi_status = "Stable / Balanced Water"
            rsi_color = "#10B981"
        elif 6.8 < rsi <= 8.5:
            rsi_status = "Corrosive to Metallic Conduits"
            rsi_color = "#F97316"
        else:
            rsi_status = "Extremely Aggressive & Corrosive"
            rsi_color = "#7F1D1D"

        # 3. Puckorius Scaling Index (PSI)
        # pHeq = 1.465 * log10(Alkalinity) + 4.54
        ph_eq = 1.465 * math.log10(max(alkalinity, 1.0)) + 4.54
        psi = round(2.0 * ph_s - ph_eq, 2)

        # 4. Aggressiveness Index (AI)
        # AI = pH + log10(Hardness * Alkalinity)
        ai = round(ph + math.log10(max(total_hardness * alkalinity, 1.0)), 2)
        if ai < 10.0:
            ai_status = "Highly Aggressive"
        elif 10.0 <= ai < 12.0:
            ai_status = "Moderately Aggressive"
        else:
            ai_status = "Non-Aggressive"

        return {
            "water_temp_c": water_temp_c,
            "ph_s": ph_s,
            "lsi": lsi,
            "lsi_status": lsi_status,
            "lsi_color": lsi_color,
            "lsi_action": lsi_action,
            "rsi": rsi,
            "rsi_status": rsi_status,
            "rsi_color": rsi_color,
            "psi": psi,
            "ai": ai,
            "ai_status": ai_status
        }

    def calculate_irrigation_suitability(self, sample):
        """
        Calculates Sodium Adsorption Ratio (SAR) and Magnesium Hazard (MAR)
        to determine secondary domestic and garden irrigation potability.
        """
        # Approximations from TDS, Hardness, and Conductivity when ion chromatography is unavailable
        hardness = float(sample.get("Hardness", 200.0))
        solids = float(sample.get("Solids", 450.0))

        # Ionic estimates in meq/L:
        # Ca2+ ~ 70% of hardness, Mg2+ ~ 30% of hardness
        ca_meq = (hardness * 0.70) / 20.04
        mg_meq = (hardness * 0.30) / 12.15
        
        # Na+ estimated from remaining cations in TDS
        na_mg = max(solids * 0.18, 10.0)
        na_meq = na_mg / 23.0

        # SAR = Na / sqrt((Ca + Mg) / 2)
        denom = math.sqrt(max((ca_meq + mg_meq) / 2.0, 0.001))
        sar = round(na_meq / denom, 2)

        if sar < 10.0:
            sar_status = "Excellent (Low Sodium Hazard)"
        elif 10.0 <= sar < 18.0:
            sar_status = "Good (Medium Sodium Hazard)"
        elif 18.0 <= sar < 26.0:
            sar_status = "Doubtful (High Sodium Hazard)"
        else:
            sar_status = "Unsuitable (Very High Sodium Hazard)"

        # MAR = [Mg / (Ca + Mg)] * 100
        mar = round((mg_meq / max(ca_meq + mg_meq, 0.001)) * 100.0, 2)
        mar_status = "Harmful to Soil & Flora (>50%)" if mar > 50.0 else "Safe / Balanced (<50%)"

        return {
            "sar": sar,
            "sar_status": sar_status,
            "mar": mar,
            "mar_status": mar_status,
            "ca_meq": round(ca_meq, 2),
            "mg_meq": round(mg_meq, 2),
            "na_meq": round(na_meq, 2)
        }

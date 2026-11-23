"""
Environmental Engineering Chemical Dosing & Water Treatment Unit Sizing Calculator.
Provides quantitative design calculations for:
  1. Coagulant Dosing (Alum / Polyaluminum Chloride) for Turbidity Removal
  2. Chemical Neutralization Dosing (Lime / Acid) for pH Balancing
  3. Cation-Exchange Resin Volume & Salt Regeneration Demand for Hardness
  4. Reverse Osmosis (RO) Osmotic Pressure, Net Driving Pressure & Permeate Recovery
  5. Germicidal UV Disinfection Fluence & Transmittance (UVT%) Estimation
"""

import math


class EngineeringDosingCalculator:
    """Calculates chemical dosages, equipment sizing, and consumable demands for water purification."""

    def __init__(self):
        pass

    def calculate_coagulant_dose(self, turbidity_ntu, flow_rate_m3_day=5.0):
        """
        Estimates alum [Al2(SO4)3·14H2O] dosage for colloidal destabilization.
        Typical empirical dosage: Dose (mg/L) = 10 + 0.6 * Turbidity.
        """
        turbidity = max(float(turbidity_ntu), 0.1)
        alum_dose_mg_l = round(10.0 + (0.6 * turbidity), 2)
        daily_mass_kg = round((flow_rate_m3_day * 1000.0 * alum_dose_mg_l) / 1e6, 3)

        return {
            "alum_dose_mg_l": alum_dose_mg_l,
            "daily_alum_demand_kg": daily_mass_kg,
            "recommended_coagulant": "Commercial Grade Filter Alum or Polyaluminum Chloride (PAC)",
            "flocculation_retention_time_min": "15 – 25 minutes rapid mix followed by slow paddle flocculation",
            "sludge_volume_estimate_l_day": round(daily_mass_kg * 3.5, 2)
        }

    def calculate_neutralization_dose(self, ph_val, flow_rate_m3_day=5.0):
        """
        Estimates neutralizing agent mass to correct acidic or alkaline water.
        """
        ph = float(ph_val)
        if ph < 6.5:
            delta_ph = 7.2 - ph
            # Hydrated lime Ca(OH)2 empirical requirement ~ 8 mg/L per 0.5 pH deficit
            lime_dose_mg_l = round(max(delta_ph * 16.0, 5.0), 2)
            daily_lime_kg = round((flow_rate_m3_day * 1000.0 * lime_dose_mg_l) / 1e6, 3)
            return {
                "condition": "Acidic Water (Plumbing Corrosive)",
                "chemical": "Hydrated Lime [Ca(OH)2] or Sodium Carbonate (Soda Ash)",
                "dose_mg_l": lime_dose_mg_l,
                "daily_consumption_kg": daily_lime_kg,
                "target_ph": "7.0 – 7.4"
            }
        elif ph > 8.5:
            delta_ph = ph - 7.5
            # Food-grade citric or sulfuric acid dosing
            acid_dose_mg_l = round(max(delta_ph * 12.0, 4.0), 2)
            daily_acid_kg = round((flow_rate_m3_day * 1000.0 * acid_dose_mg_l) / 1e6, 3)
            return {
                "condition": "Alkaline Water (Scaling & Bitter)",
                "chemical": "Dilute Food-Grade Acid (Citric Acid or H2SO4)",
                "dose_mg_l": acid_dose_mg_l,
                "daily_consumption_kg": daily_acid_kg,
                "target_ph": "7.2 – 7.6"
            }
        else:
            return {
                "condition": "Neutral / Balanced pH",
                "chemical": "None required",
                "dose_mg_l": 0.0,
                "daily_consumption_kg": 0.0,
                "target_ph": "Current pH complies with statutory limits"
            }

    def calculate_softener_sizing(self, hardness_mg_l, flow_rate_m3_day=5.0):
        """
        Sizes a cation-exchange water softening unit.
        Resin exchange capacity ~ 1.8 eq/L (approx 90 g CaCO3/L resin).
        Salt for regeneration ~ 160 g NaCl / L resin.
        """
        hardness = max(float(hardness_mg_l), 0.0)
        target_hardness = 100.0  # mg/L residual hardness desirable
        hardness_to_remove = max(hardness - target_hardness, 0.0)

        # Daily hardness load in grams of CaCO3
        daily_hardness_load_g = (flow_rate_m3_day * 1000.0 * hardness_to_remove) / 1000.0
        
        # Resin volume needed for 3-day operating cycle before regeneration
        operating_days = 3.0
        resin_capacity_g_l = 85.0  # g CaCO3 per liter of cross-linked resin
        resin_volume_liters = round((daily_hardness_load_g * operating_days) / resin_capacity_g_l, 1)
        resin_volume_liters = max(resin_volume_liters, 15.0)  # standard minimum bed

        # Salt required per regeneration cycle
        salt_demand_kg = round(resin_volume_liters * 0.160, 2)

        return {
            "hardness_to_remove_mg_l": round(hardness_to_remove, 1),
            "recommended_resin_volume_l": resin_volume_liters,
            "resin_type": "Strong Acid Cation (SAC) Resin (Gel Type, 8% Crosslinked Polystyrene)",
            "cycle_duration_days": operating_days,
            "salt_per_regeneration_kg": salt_demand_kg,
            "brine_concentration": "10 – 12% Saturated Sodium Chloride Solution"
        }

    def calculate_ro_membrane_performance(self, tds_mg_l, flow_rate_m3_day=5.0):
        """
        Estimates Reverse Osmosis membrane operating parameters:
        Osmotic pressure: Pi ~ 0.007 * TDS (bar)
        Membrane feed pressure ~ 2.0 * Pi + hydraulic net driving pressure.
        """
        tds = max(float(tds_mg_l), 50.0)
        # Approximate osmotic pressure in bar
        osmotic_pressure_bar = round(0.007 * tds, 2)
        net_driving_pressure_bar = 8.5
        operating_feed_pressure_bar = round(osmotic_pressure_bar + net_driving_pressure_bar, 2)

        # Standard recovery rate (65% to 75% for modern brackish water elements)
        recovery_ratio = 0.70
        permeate_flow_m3_day = round(flow_rate_m3_day * recovery_ratio, 2)
        reject_brine_m3_day = round(flow_rate_m3_day * (1.0 - recovery_ratio), 2)
        expected_permeate_tds = round(tds * 0.04, 1)  # 96% rejection rate

        return {
            "raw_tds_mg_l": tds,
            "osmotic_pressure_bar": osmotic_pressure_bar,
            "recommended_pump_pressure_bar": operating_feed_pressure_bar,
            "recommended_pump_psi": round(operating_feed_pressure_bar * 14.5038, 1),
            "permeate_recovery_percent": 70.0,
            "pure_permeate_output_m3_day": permeate_flow_m3_day,
            "concentrate_brine_output_m3_day": reject_brine_m3_day,
            "projected_permeate_tds_mg_l": expected_permeate_tds,
            "salt_rejection_percent": 96.0
        }

    def calculate_uv_disinfection_dose(self, turbidity_ntu, toc_mg_l):
        """
        Estimates Ultraviolet Transmittance at 254 nm (UVT%) and required UV Fluence.
        Standard for drinking water is 40 mJ/cm2 (NSF/ANSI 55 Class A standard).
        """
        turbidity = max(float(turbidity_ntu), 0.1)
        toc = max(float(toc_mg_l), 0.1)

        # UVT% diminishes with higher TOC (UV absorption) and Turbidity (scattering)
        uvt_estimate = round(max(20.0, 98.0 - (toc * 4.5) - (turbidity * 2.8)), 1)
        uvt_estimate = min(98.0, uvt_estimate)

        if uvt_estimate >= 85.0:
            uvt_status = "Excellent Water Clarity (High UV Penetration)"
            lamp_power_w_m3 = 18.0
        elif 70.0 <= uvt_estimate < 85.0:
            uvt_status = "Moderate UV Clarity (Requires Quartz Sleeve Maintenance)"
            lamp_power_w_m3 = 28.0
        else:
            uvt_status = "Poor UV Transmittance (Pre-filtration / Carbon required before UV)"
            lamp_power_w_m3 = 45.0

        return {
            "estimated_uvt_percent": uvt_estimate,
            "uvt_status": uvt_status,
            "target_uv_fluence": "40.0 mJ/cm² (NSF 55 Class A Standard)",
            "pathogen_log_reduction": "4-Log (99.99%) inactivation of E. coli, Giardia lamblia, and Cryptosporidium",
            "recommended_lamp": "Low-Pressure High-Output (LPHO) Germicidal 254 nm UV Lamp",
            "estimated_power_density_w": lamp_power_w_m3
        }

"""
Dynamic Postural Stability Index (DPSI) & Jump-Landing Shock Attenuation Engine.
Provides deterministic, zero-dependency calculation of Anterior-Posterior (APSI),
Medial-Lateral (MLSI), Vertical (VSI), and composite DPSI from ground reaction force (GRF) series.
"""

import math
from typing import Dict, Any, List, Optional


class DynamicPosturalStabilityClient:
    """
    Deterministic client for calculating Dynamic Postural Stability Index (DPSI) from force platform data.
    Pure Python standard library implementation based on Wikstrom et al. biomechanical protocols.
    """

    def __init__(self):
        pass

    def calculate_dpsi(
        self,
        grf_ap_newtons: List[float],
        grf_ml_newtons: List[float],
        grf_vertical_newtons: List[float],
        body_weight_newtons: float,
        landing_duration_sec: float = 3.0
    ) -> Dict[str, Any]:
        """
        Calculates DPSI and directional stability indices:
        APSI = sqrt( sum(GRF_x^2) / (N * BW^2) )
        MLSI = sqrt( sum(GRF_y^2) / (N * BW^2) )
        VSI = sqrt( sum((GRF_z - BW)^2) / (N * BW^2) )
        DPSI = sqrt( (sum(GRF_x^2) + sum(GRF_y^2) + sum((GRF_z - BW)^2)) / (N * BW^2) )
        """
        n = min(len(grf_ap_newtons), len(grf_ml_newtons), len(grf_vertical_newtons))
        if n < 10 or body_weight_newtons <= 0:
            return {"error": "Invalid inputs: at least 10 samples and positive body weight required"}

        bw_sq = body_weight_newtons * body_weight_newtons
        sum_ap_sq = sum(fx * fx for fx in grf_ap_newtons[:n])
        sum_ml_sq = sum(fy * fy for fy in grf_ml_newtons[:n])
        sum_vert_sq = sum((fz - body_weight_newtons) ** 2 for fz in grf_vertical_newtons[:n])

        apsi = math.sqrt(sum_ap_sq / (n * bw_sq))
        mlsi = math.sqrt(sum_ml_sq / (n * bw_sq))
        vsi = math.sqrt(sum_vert_sq / (n * bw_sq))
        dpsi = math.sqrt((sum_ap_sq + sum_ml_sq + sum_vert_sq) / (n * bw_sq))

        peak_vertical_grf = max(grf_vertical_newtons[:n])
        impact_load_multiplier = round(peak_vertical_grf / body_weight_newtons, 2)

        # Time to stabilization (TTS): time in seconds until vertical GRF stays within +/- 5% BW for >= 0.5s
        sample_dt = landing_duration_sec / n
        tts_sec = landing_duration_sec
        settled_target_lo = body_weight_newtons * 0.95
        settled_target_hi = body_weight_newtons * 1.05
        settle_window = max(3, int(0.5 / sample_dt))

        for i in range(n - settle_window):
            if all(settled_target_lo <= grf_vertical_newtons[k] <= settled_target_hi for k in range(i, i + settle_window)):
                tts_sec = round(i * sample_dt, 2)
                break

        # Dynamic Stability Score (0 - 100):
        # Elite DPSI is ~ 0.28 - 0.35. Scores above 0.45 indicate sluggish shock attenuation.
        dpsi_penalty = min(60.0, max(0.0, (dpsi - 0.25) / 0.25) * 60.0)
        impact_penalty = min(40.0, max(0.0, (impact_load_multiplier - 1.5) / 2.0) * 40.0)
        dpsi_score = round(max(5.0, min(100.0, 100.0 - dpsi_penalty - impact_penalty + 10.0)), 1)

        if dpsi <= 0.33 and impact_load_multiplier <= 2.2:
            status = "OPTIMAL_DYNAMIC_ATTENUATION"
            guidance = "Exceptional kinetic energy absorption with rapid sagittal/frontal plane stabilization."
        elif dpsi <= 0.40:
            status = "ADEQUATE_NEUROMUSCULAR_CONTROL"
            guidance = "Normal dynamic stability; routine jump-landing force dampening without excessive joint loading."
        elif dpsi <= 0.48:
            status = "ELEVATED_GROUND_IMPACT_SPIKE"
            guidance = "Elevated ground impact spike or prolonged stabilization latency. Train eccentric quadriceps and gluteal deceleration."
        else:
            status = "HIGH_DYNAMIC_INSTABILITY"
            guidance = "Marked landing force dispersion deficiency; heightened ACL/patellar tendon mechanical strain risk. Implement plyometric jump-landing mechanics retraining."

        return {
            "sample_count": n,
            "body_weight_newtons": body_weight_newtons,
            "apsi": round(apsi, 4),
            "mlsi": round(mlsi, 4),
            "vsi": round(vsi, 4),
            "dpsi": round(dpsi, 4),
            "peak_vertical_grf_newtons": round(peak_vertical_grf, 1),
            "impact_load_multiplier": impact_load_multiplier,
            "time_to_stabilization_sec": tts_sec,
            "dynamic_stability_score": dpsi_score,
            "status": status,
            "biomechanical_guidance": guidance
        }

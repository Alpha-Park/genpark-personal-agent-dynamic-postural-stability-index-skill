"""
Example usage for Dynamic Postural Stability Index (DPSI) Skill.
Demonstrates analyzing jump-landing ground reaction force (GRF) data.
"""

import math
from client import DynamicPosturalStabilityClient


def generate_synthetic_landing(bw: float = 700.0, n_pts: int = 150):
    ap_forces = []
    ml_forces = []
    vert_forces = []
    for i in range(n_pts):
        t = i / 50.0  # 50 Hz, 3.0 seconds
        # Exponentially decaying impact transient
        decay = math.exp(-t / 0.45)
        # Vertical impact spikes to ~2.1x BW then settles to BW
        fz = bw + (bw * 1.15 * decay * math.sin(math.pi * min(1.0, t / 0.15))) + (15.0 * math.cos(4.0 * t) * decay)
        # Shear forces fluctuate around 0
        fx = (bw * 0.25 * decay * math.sin(6.0 * t)) + (5.0 * math.sin(2.0 * t))
        fy = (bw * 0.18 * decay * math.cos(7.0 * t)) + (4.0 * math.cos(2.0 * t))

        ap_forces.append(round(fx, 2))
        ml_forces.append(round(fy, 2))
        vert_forces.append(round(fz, 2))
    return ap_forces, ml_forces, vert_forces


def main():
    client = DynamicPosturalStabilityClient()
    bw_n = 720.0  # ~73.4 kg subject

    print("=== 1. Calculating Dynamic Postural Stability Index (Jump-Landing) ===")
    fx, fy, fz = generate_synthetic_landing(bw=bw_n, n_pts=150)
    res = client.calculate_dpsi(fx, fy, fz, body_weight_newtons=bw_n, landing_duration_sec=3.0)

    print(f"APSI: {res['apsi']} | MLSI: {res['mlsi']} | VSI: {res['vsi']}")
    print(f"Composite DPSI: {res['dpsi']}")
    print(f"Peak Vertical Force: {res['peak_vertical_grf_newtons']} N ({res['impact_load_multiplier']}x BW)")
    print(f"Time to Stabilization: {res['time_to_stabilization_sec']} s")
    print(f"Dynamic Stability Score: {res['dynamic_stability_score']} / 100")
    print(f"Status: {res['status']}")
    print(f"Biomechanical Guidance: {res['biomechanical_guidance']}")


if __name__ == "__main__":
    main()

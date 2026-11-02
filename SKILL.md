---
name: genpark-personal-agent-dynamic-postural-stability-index-skill
description: Deterministic evaluation of Dynamic Postural Stability Index (DPSI), triaxial ground reaction force (GRF) shock attenuation, and time to stabilization.
version: 1.0.0
author: GenPark Autonomous Agents Ecosystem
license: MIT
tags:
  - personal-agent
  - ai-agent
  - openclaw
  - genpark
  - mcp
  - mcp-server
  - model-context-protocol
  - python
  - zero-dependency
  - wellness
  - productivity
  - production-ready
---

# Dynamic Postural Stability Index (DPSI) Skill

## Overview
The `genpark-personal-agent-dynamic-postural-stability-index-skill` brings clinical biomechanical shock attenuation analytics to sovereign personal agents. Assessing how an individual absorbs ground reaction forces (GRF) during dynamic jump-landings or single-leg deceleration reveals neuromuscular fatigue, lower-extremity stiffness regulation, and non-contact ligament injury risk (e.g. ACL strain). This skill computes directional stability indices (APSI, MLSI, VSI), composite DPSI, peak impact load multipliers ($BW$), and time to stabilization (TTS).

## Physiological Model & Mathematics
1. **Directional Stability Indices**:
   $$\text{APSI} = \sqrt{\frac{\sum GRF_{x}^2}{N \cdot BW^2}}, \quad \text{MLSI} = \sqrt{\frac{\sum GRF_{y}^2}{N \cdot BW^2}}$$
   $$\text{VSI} = \sqrt{\frac{\sum (GRF_{z} - BW)^2}{N \cdot BW^2}}$$
2. **Composite Dynamic Postural Stability Index ($DPSI$)**:
   $$DPSI = \sqrt{\frac{\sum GRF_x^2 + \sum GRF_y^2 + \sum (GRF_z - BW)^2}{N \cdot BW^2}}$$
   - **Elite Shock Attenuation**: $DPSI \le 0.33$.
   - **Normal Dynamic Control**: $0.34 - 0.40$.
   - **Elevated Impact / Instability**: $> 0.45$.
3. **Time to Stabilization ($TTS$)**:
   Elapsed time in seconds post-initial contact until vertical GRF oscillations damp permanently within $\pm 5\%$ of static body weight.

## Tools & Endpoints
- `calculate_dpsi`: Computes APSI, MLSI, VSI, DPSI, impact load multiplier, and time to stabilization.

"""
MCP Server for Dynamic Postural Stability Index (DPSI) & Jump-Landing Shock Attenuation.
Exposes JSON-RPC endpoints for computing directional stability indices and time to stabilization.
"""

import json
import sys
from client import DynamicPosturalStabilityClient

client = DynamicPosturalStabilityClient()


def handle_request(request: dict) -> dict:
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "calculate_dpsi",
                        "description": "Calculates Dynamic Postural Stability Index (DPSI, APSI, MLSI, VSI), impact load multiplier, and time to stabilization from jump-landing ground reaction force (GRF) data.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "grf_ap_newtons": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Anterior-posterior shear force samples in Newtons"
                                },
                                "grf_ml_newtons": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Medial-lateral shear force samples in Newtons"
                                },
                                "grf_vertical_newtons": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Vertical ground reaction force samples in Newtons"
                                },
                                "body_weight_newtons": {
                                    "type": "number",
                                    "description": "Subject body weight in Newtons (mass_kg * 9.81)"
                                },
                                "landing_duration_sec": {
                                    "type": "number",
                                    "default": 3.0,
                                    "description": "Total duration of landing recording in seconds"
                                }
                            },
                            "required": ["grf_ap_newtons", "grf_ml_newtons", "grf_vertical_newtons", "body_weight_newtons"]
                        }
                    }
                ]
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "calculate_dpsi":
            res = client.calculate_dpsi(
                grf_ap_newtons=args.get("grf_ap_newtons", []),
                grf_ml_newtons=args.get("grf_ml_newtons", []),
                grf_vertical_newtons=args.get("grf_vertical_newtons", []),
                body_weight_newtons=args.get("body_weight_newtons", 700.0),
                landing_duration_sec=args.get("landing_duration_sec", 3.0)
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method {tool_name} not found"}
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32600, "message": "Invalid Request"}
    }


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()

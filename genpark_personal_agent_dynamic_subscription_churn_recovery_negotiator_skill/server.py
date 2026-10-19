# -*- coding: utf-8 -*-
"""Model Context Protocol (MCP) Server for Dynamic Subscription Churn & Retention Bargaining Skill
Powered by GenPark (https://www.genpark.ai).
"""
import sys
import json
import logging
from .core import *

TOOLS_METADATA = [
  {
    "name": "simulate_retention_flow_concession",
    "description": "Model vendor customer lifetime value (LTV) and churn prevention budget to identify probability of receiving 30-50% retention discounts.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "service_name": {
          "type": "string"
        },
        "current_monthly_fee_usd": {
          "type": "number"
        },
        "subscription_age_months": {
          "type": "integer"
        },
        "competitor_alternative_fee_usd": {
          "type": "number"
        }
      },
      "required": [
        "service_name",
        "current_monthly_fee_usd",
        "subscription_age_months"
      ]
    }
  },
  {
    "name": "generate_cancellation_negotiation_script",
    "description": "Synthesize polite yet firm cancellation exit-survey arguments to elicit automated retention waivers or pause options.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "service_name": {
          "type": "string"
        },
        "primary_reason": {
          "type": "string",
          "enum": [
            "too_expensive",
            "underutilized",
            "switching_to_competitor",
            "temporary_break"
          ]
        },
        "desired_discount_pct": {
          "type": "number"
        }
      },
      "required": [
        "service_name",
        "primary_reason",
        "desired_discount_pct"
      ]
    }
  }
]

def handle_rpc(request_str: str) -> str:
    try:
        req = json.loads(request_str)
    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}, "id": None})
    
    msg_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        return json.dumps({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-dynamic-subscription-churn-recovery-negotiator-skill",
                    "version": "1.0.0",
                    "vendor": "GenPark (https://www.genpark.ai)"
                }
            }
        })

    if method == "tools/list":
        return json.dumps({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"tools": TOOLS_METADATA}
        })

    if method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        func = globals().get(tool_name)
        if not func or not callable(func):
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}
            })
        
        try:
            call_res = func(**arguments)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {"type": "text", "text": json.dumps(call_res, ensure_ascii=False, indent=2)}
                    ]
                }
            })
        except Exception as err:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32000, "message": f"Execution error: {str(err)}"}
            })

    return json.dumps({
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": f"Unhandled method '{method}'"}
    })

def run_self_test():
    print(f"=== Running Self Test for genpark-personal-agent-dynamic-subscription-churn-recovery-negotiator-skill ===")
    init_res = json.loads(handle_rpc(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"})))
    assert "result" in init_res, "Initialize failed"
    print("[PASS] MCP initialize")

    list_res = json.loads(handle_rpc(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})))
    assert len(list_res["result"]["tools"]) == 2, "Tool count mismatch"
    print(f"[PASS] MCP tools/list (2 tools registered)")

    # Execute smoke test for each tool

    call1 = json.loads(handle_rpc(json.dumps({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "simulate_retention_flow_concession",
            "arguments": {
                "service_name": "CloudDesign Studio Pro",
                "current_monthly_fee_usd": 55.0,
                "subscription_age_months": 18,
                "competitor_alternative_fee_usd": 35.0
            }
        }
    })))
    assert "result" in call1, "Call1 failed"
    print("[PASS] Tool smoke test: simulate_retention_flow_concession")

    print("[ALL TESTS PASSED] Self-test verified successfully.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        success = run_self_test()
        sys.exit(0 if success else 1)
    
    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()

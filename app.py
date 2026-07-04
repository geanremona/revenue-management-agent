"""
app.py
------
Minimal web wrapper around the Revenue Management Agent so it can run as a
hosted service (e.g. on a Vultr instance) instead of only as a CLI script.

Routes:
  GET  /                -> HTML view of the latest brief
  GET  /api/brief       -> JSON: recommendations, anomalies, channel results
  POST /api/run         -> re-runs the agent against /data and regenerates the brief
  GET  /healthz         -> health check for load balancers / uptime monitors
"""
import os
import sys
import markdown as md
from flask import Flask, jsonify, Response

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from agent import RevenueManagementAgent  # noqa: E402

BASE = os.path.dirname(__file__)
BRIEF_PATH = os.path.join(BASE, "revenue_strategy_brief.md")

app = Flask(__name__)


def build_agent():
    return RevenueManagementAgent(
        bookings_path=os.path.join(BASE, "data/bookings.csv"),
        competitor_path=os.path.join(BASE, "data/competitor_rates.csv"),
        events_path=os.path.join(BASE, "data/events.json"),
        occupancy_history_path=os.path.join(BASE, "data/occupancy_history.csv"),
        property_name=os.environ.get("PROPERTY_NAME", "Harborview Grand (Demo)"),
        auto_push_critical_anomalies=False,
    )


def run_and_cache():
    result = build_agent().run()
    with open(BRIEF_PATH, "w") as f:
        f.write(result["brief_markdown"])
    return result


@app.get("/healthz")
def healthz():
    return jsonify({"status": "ok"})


@app.get("/")
def home():
    if not os.path.exists(BRIEF_PATH):
        run_and_cache()
    with open(BRIEF_PATH) as f:
        content = f.read()
    html_body = md.markdown(content, extensions=["tables"])
    page = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Revenue Strategy Brief</title>
  <style>
    body {{ font-family: -apple-system, Helvetica, Arial, sans-serif; max-width: 900px;
            margin: 40px auto; padding: 0 20px; line-height: 1.5; color: #1a1a1a; }}
    table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
    th, td {{ border: 1px solid #ddd; padding: 6px 10px; text-align: left; font-size: 14px; }}
    th {{ background: #f4f4f4; }}
    h1, h2 {{ border-bottom: 1px solid #eee; padding-bottom: 6px; }}
    .rerun {{ display: inline-block; margin: 12px 0; padding: 8px 14px; background: #1a1a1a;
              color: white; text-decoration: none; border-radius: 6px; font-size: 14px; }}
  </style>
</head>
<body>
  <a class="rerun" href="/run">Re-run agent</a>
  {html_body}
</body>
</html>"""
    return Response(page, mimetype="text/html")


@app.get("/run")
def run_via_browser():
    run_and_cache()
    return Response('<meta http-equiv="refresh" content="0; url=/">', mimetype="text/html")


@app.post("/api/run")
def api_run():
    result = run_and_cache()
    return jsonify({
        "recommendations": [r.__dict__ for r in result["recommendations"]],
        "anomalies": [a.__dict__ for a in result["anomalies"]],
        "held_back_dates": result["held_back_dates"],
        "channel_results_count": len(result["channel_results"]),
    })


@app.get("/api/brief")
def api_brief():
    if not os.path.exists(BRIEF_PATH):
        run_and_cache()
    with open(BRIEF_PATH) as f:
        return jsonify({"brief_markdown": f.read()})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

"""
app.py
------
Minimal web wrapper around the Revenue Management Agent so it can run as a
hosted service (e.g. on a Vultr instance) instead of only as a CLI script.

Routes:
  GET  /                -> Premium dashboard UI (Revenue Pilot)
  GET  /api/data        -> JSON: structured dashboard data (summary, recs, anomalies, channels, intel)
  GET  /api/brief       -> JSON: raw brief markdown (backward-compat)
  POST /api/run         -> re-runs the agent against /data and regenerates the brief
  GET  /healthz         -> health check for load balancers / uptime monitors
"""
import os
import sys
from datetime import datetime
from flask import Flask, jsonify, Response, render_template, request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from agent import RevenueManagementAgent  # noqa: E402

BASE = os.path.dirname(__file__)
BRIEF_PATH = os.path.join(BASE, "revenue_strategy_brief.md")

app = Flask(
    __name__,
    template_folder=os.path.join(BASE, "templates"),
    static_folder=os.path.join(BASE, "static"),
)

# In-memory cache of the last agent run result
_last_result = None


def build_agent():
    return RevenueManagementAgent(
        bookings_path=os.path.join(BASE, "data/bookings.csv"),
        competitor_path=os.path.join(BASE, "data/competitor_rates.csv"),
        events_path=os.path.join(BASE, "data/events.json"),
        occupancy_history_path=os.path.join(BASE, "data/occupancy_history.csv"),
        property_name=os.environ.get("PROPERTY_NAME", "Harborview Grand (Demo)"),
        auto_push_critical_anomalies=False,
        cloudflare_account_id=os.environ.get("CLOUDFLARE_ACCOUNT_ID"),
        cloudflare_api_token=os.environ.get("CLOUDFLARE_API_TOKEN"),
    )


def run_and_cache():
    global _last_result
    result = build_agent().run()
    with open(BRIEF_PATH, "w") as f:
        f.write(result["brief_markdown"])
    _last_result = result
    return result


def get_result():
    """Return cached result or run the agent if none exists."""
    global _last_result
    if _last_result is None:
        run_and_cache()
    return _last_result


def serialize_result(result):
    """Convert agent result dict into structured JSON for the dashboard."""
    recommendations = result["recommendations"]
    anomalies = result["anomalies"]
    channel_results = result["channel_results"]
    competitor_rates = result.get("competitor_rates", [])
    events = result.get("events", [])

    n_up = sum(1 for r in recommendations if r.change_pct > 0)
    n_down = sum(1 for r in recommendations if r.change_pct < 0)
    n_flat = len(recommendations) - n_up - n_down
    critical = [a for a in anomalies if a.severity == "critical"]
    failed = [c for c in channel_results if c.status == "failed"]
    revenue_impact = result.get("revenue_impact", 0)

    return {
        "property_name": os.environ.get("PROPERTY_NAME", "Harborview Grand (Demo)"),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "summary": {
            "dates_reviewed": len(recommendations),
            "increases": n_up,
            "decreases": n_down,
            "holds": n_flat,
            "anomaly_count": len(anomalies),
            "critical_count": len(critical),
            "channel_success": len(channel_results) - len(failed),
            "channel_total": len(channel_results),
            "channel_failures": len(failed),
            "revenue_impact": round(revenue_impact, 2),
        },
        "recommendations": [
            {
                "stay_date": r.stay_date,
                "current_rate": r.current_rate,
                "recommended_rate": r.recommended_rate,
                "change_pct": r.change_pct,
                "market_index": r.market_index,
                "occupancy_pct": r.occupancy_pct,
                "event": r.event,
                "rationale": r.rationale,
            }
            for r in recommendations
        ],
        "anomalies": [
            {
                "stay_date": a.stay_date,
                "metric": a.metric,
                "current_value": a.current_value,
                "baseline_value": a.baseline_value,
                "delta_pct": a.delta_pct,
                "severity": a.severity,
                "note": a.note,
            }
            for a in anomalies
        ],
        "channel_results": [
            {
                "stay_date": c.stay_date,
                "channel": c.channel,
                "rate_pushed": c.rate_pushed,
                "status": c.status,
                "detail": c.detail,
            }
            for c in channel_results
        ],
        "competitor_rates": [
            {
                "stay_date": c.stay_date,
                "competitor": c.competitor,
                "rate": c.rate,
                "source": c.source,
            }
            for c in competitor_rates
        ],
        "events": [
            {
                "event": e.event,
                "start_date": e.start_date,
                "end_date": e.end_date,
                "expected_attendance": e.expected_attendance,
                "demand_impact": e.demand_impact,
                "source": e.source,
            }
            for e in events
        ],
        "held_back_dates": result["held_back_dates"],
    }


@app.get("/healthz")
def healthz():
    return jsonify({"status": "ok"})


@app.get("/")
def home():
    property_name = os.environ.get("PROPERTY_NAME", "Harborview Grand (Demo)")
    return render_template("index.html", property_name=property_name)


@app.get("/api/data")
def api_data():
    result = get_result()
    return jsonify(serialize_result(result))


@app.get("/run")
def run_via_browser():
    run_and_cache()
    return Response('<meta http-equiv="refresh" content="0; url=/">', mimetype="text/html")


@app.post("/api/run")
def api_run():
    result = run_and_cache()
    return jsonify(serialize_result(result))


@app.post("/api/override/approve")
def api_override_approve():
    data = request.get_json() or {}
    stay_date = data.get("stay_date")
    rate = data.get("rate")
    if not stay_date or not rate:
        return jsonify({"status": "error", "message": "Missing stay_date or rate"}), 400

    agent = build_agent()
    # Manually push rate to channels
    results = agent.channel_updater.push_all(stay_date, float(rate))

    # Update memory cache in app.py if it exists
    global _last_result
    if _last_result:
        # Extend current logs
        _last_result["channel_results"].extend(results)
        # Remove from held_back list
        if stay_date in _last_result["held_back_dates"]:
            _last_result["held_back_dates"].remove(stay_date)

    return jsonify({"status": "success", "results": [r.__dict__ for r in results]})


@app.post("/api/override/dismiss")
def api_override_dismiss():
    data = request.get_json() or {}
    stay_date = data.get("stay_date")
    if not stay_date:
        return jsonify({"status": "error", "message": "Missing stay_date"}), 400

    global _last_result
    if _last_result:
        # Remove from held_back list so it is no longer flagged as held-back
        if stay_date in _last_result["held_back_dates"]:
            _last_result["held_back_dates"].remove(stay_date)

    return jsonify({"status": "success"})


@app.get("/api/brief")
def api_brief():
    if not os.path.exists(BRIEF_PATH):
        run_and_cache()
    with open(BRIEF_PATH) as f:
        return jsonify({"brief_markdown": f.read()})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

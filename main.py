"""
main.py
-------
Runs the Revenue Management Agent end-to-end against the sample data in
/data and writes the resulting brief to revenue_strategy_brief.md.

Usage:
    python main.py
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from agent import RevenueManagementAgent  # noqa: E402


def main():
    base = os.path.dirname(__file__)
    agent = RevenueManagementAgent(
        bookings_path=os.path.join(base, "data/bookings.csv"),
        competitor_path=os.path.join(base, "data/competitor_rates.csv"),
        events_path=os.path.join(base, "data/events.json"),
        occupancy_history_path=os.path.join(base, "data/occupancy_history.csv"),
        property_name="Harborview Grand (Demo)",
        auto_push_critical_anomalies=False,
    )

    result = agent.run()

    out_path = os.path.join(base, "revenue_strategy_brief.md")
    with open(out_path, "w") as f:
        f.write(result["brief_markdown"])

    print(f"Brief written to: {out_path}\n")
    print(f"Recommendations: {len(result['recommendations'])}")
    print(f"Anomalies flagged: {len(result['anomalies'])}")
    print(f"Held back from auto-push (critical anomalies): {result['held_back_dates']}")
    print(f"Channel pushes attempted: {len(result['channel_results'])}")


if __name__ == "__main__":
    main()

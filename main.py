"""
main.py
-------
CLI entry point for the Revenue Management Agent. Runs the full
perceive → analyze → plan → act → report cycle and writes a Markdown
Revenue Strategy Brief.

Usage (no args — uses bundled sample data in /data):
    python main.py

Usage (with your own files):
    python main.py \\
        --bookings path/to/bookings.csv \\
        --competitor path/to/competitor_rates.csv \\
        --events path/to/events.json \\
        --occupancy-history path/to/occupancy_history.csv \\
        --property-name "My Hotel" \\
        --out revenue_strategy_brief.md

Any --path flag can be omitted — the script falls back to bundled sample
data in /data/ for that input, so it's always runnable end-to-end even
before the user's real files are ready.

Expected input schemas (see references/data_schemas.md for full detail):
  bookings.csv           : stay_date, bookings_on_the_books, rooms_available,
                           current_adr, avg_length_of_stay, pickup_last_7d
  competitor_rates.csv   : stay_date, competitor, rate, source
  events.json            : [{event, start_date, end_date, expected_attendance,
                           demand_impact, source}, ...]
  occupancy_history.csv  : stay_date_ly, occupancy_pct_ly, adr_ly, revpar_ly
"""
import argparse
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

sys.path.insert(0, os.path.join(BASE_DIR, "src"))
from agent import RevenueManagementAgent  # noqa: E402


def main():
    p = argparse.ArgumentParser(description="Run the Revenue Management Agent pipeline.")
    p.add_argument("--bookings",
                   default=os.path.join(DATA_DIR, "bookings.csv"),
                   help="Path to bookings CSV (default: data/bookings.csv)")
    p.add_argument("--competitor",
                   default=os.path.join(DATA_DIR, "competitor_rates.csv"),
                   help="Path to competitor rates CSV (default: data/competitor_rates.csv)")
    p.add_argument("--events",
                   default=os.path.join(DATA_DIR, "events.json"),
                   help="Path to events JSON (default: data/events.json)")
    p.add_argument("--occupancy-history",
                   default=os.path.join(DATA_DIR, "occupancy_history.csv"),
                   help="Path to occupancy history CSV (default: data/occupancy_history.csv)")
    p.add_argument("--property-name",
                   default=os.environ.get("PROPERTY_NAME", "Harborview Grand (Demo)"),
                   help="Property name shown in the brief and dashboard")
    p.add_argument("--out",
                   default=os.path.join(BASE_DIR, "revenue_strategy_brief.md"),
                   help="Output path for the Markdown brief")
    p.add_argument("--auto-push-critical",
                   action="store_true",
                   help="Push rates for critical-anomaly dates too (default: hold for review)")
    args = p.parse_args()

    # Report which inputs fell back to bundled sample data
    using_samples = []
    for flag, path in [
        ("bookings", args.bookings),
        ("competitor", args.competitor),
        ("events", args.events),
        ("occupancy-history", args.occupancy_history),
    ]:
        if os.path.abspath(path).startswith(DATA_DIR):
            using_samples.append(flag)

    agent = RevenueManagementAgent(
        bookings_path=args.bookings,
        competitor_path=args.competitor,
        events_path=args.events,
        occupancy_history_path=args.occupancy_history,
        property_name=args.property_name,
        auto_push_critical_anomalies=args.auto_push_critical,
    )
    result = agent.run()

    with open(args.out, "w") as f:
        f.write(result["brief_markdown"])

    if using_samples:
        print(f"NOTE: used bundled sample data for: {', '.join(using_samples)} "
              f"(no custom path supplied for these).")
    print(f"Brief written to: {args.out}")
    print(f"Recommendations: {len(result['recommendations'])}")
    print(f"Anomalies flagged: {len(result['anomalies'])}")
    print(f"Held back from auto-push (critical anomalies): {result['held_back_dates']}")
    print(f"Channel pushes attempted: {len(result['channel_results'])}")
    print(f"Revenue impact: ${result.get('revenue_impact', 0):+.2f}")


if __name__ == "__main__":
    main()

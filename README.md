# Revenue Management Agent

An end-to-end dynamic pricing agent for hotels/short-term rentals. It reads
booking pace, competitor pricing, and event calendars; retrieves historical
occupancy; computes rate recommendations; flags demand anomalies; pushes
approved rates across distribution channels; and produces a cited Revenue
Strategy Brief for human sign-off.

## Pipeline (`src/agent.py`)

```
PERCEIVE            ANALYZE               PLAN                  ACT                    REPORT
------------        ----------------      ----------------      ----------------       ----------------
bookings.csv    ->  AnomalyDetector   ->  DynamicPricingEngine  ChannelRateUpdater  ->  RevenueBriefGenerator
competitor_rates.csv   (vs. LY occupancy,     (occupancy +          (pushes to OTAs,        (Markdown, cited
events.json             pickup pace)          pace + comp set       direct engine, GDS;      market intel,
occupancy_history.csv)                        + events, with        holds back critical-     anomaly log,
                                               guardrails)           anomaly dates)            channel log)
```

## Files

| File | Role |
|---|---|
| `src/connectors.py` | Ingestion adapters for bookings, competitor rates, event calendar, historical occupancy |
| `src/anomaly.py` | Flags sudden demand spikes/drops vs. pace baseline and vs. same period last year |
| `src/pricing_engine.py` | Rule-based dynamic rate recommendation engine with explainable rationale + guardrails |
| `src/channel_updater.py` | Simulated multi-channel rate push ("tool calls") — swap for a real channel-manager API |
| `src/report.py` | Builds the cited Markdown Revenue Strategy Brief |
| `src/agent.py` | Orchestrator that runs the full perceive→analyze→plan→act→report cycle |
| `main.py` | Demo entry point, runs against sample data in `/data` |
| `data/*.csv`, `data/*.json` | Mock booking, competitor, event, and occupancy history data |

## Run it (CLI)

```bash
python3 main.py
```

Produces `revenue_strategy_brief.md` and prints a summary to stdout.

## Run it (web app)

```bash
pip install -r requirements.txt
python3 app.py
```

Visit `http://localhost:8080/` for the rendered brief, or `GET /api/brief`
for JSON. `POST /api/run` re-runs the agent.

## Deploying to a Vultr instance + publishing to GitHub

See **[DEPLOY.md](DEPLOY.md)** for the full step-by-step: provisioning the
instance, running as a systemd service or via Docker, putting Nginx in
front, and pushing this repo to a public GitHub repo for submission.

**Live demo:** _add your Vultr URL here once deployed_

## Design choices worth knowing about

- **Explainable, not black-box.** The pricing engine is rule-based (occupancy
  factor × pace factor × event factor, blended with the competitor index) so
  every recommended rate ships with a plain-English rationale a revenue
  manager can audit. Swap in an ML/elasticity model behind the same
  `DynamicPricingEngine.recommend()` interface if you want to upgrade later.
- **Guardrails are hard-coded, not learned.** Max ±15% rate move per cycle and
  a $120–$320 floor/ceiling prevent runaway pricing from a bad data point.
- **Critical anomalies block auto-push.** If a stay date's demand signal is a
  severe outlier vs. history (e.g. the "Regional Tech Summit" spike in the
  demo), the agent holds that date out of the automated channel push and
  flags it for human review instead of repricing blind. Set
  `auto_push_critical_anomalies=True` in `RevenueManagementAgent` to change
  that behavior.
- **Every market-intelligence claim in the brief is sourced.** Competitor
  rates and event data carry their originating feed name so the brief reads
  as cited intelligence, not an opaque number.

## Wiring to real systems

| Component | Swap in |
|---|---|
| `BookingDataConnector` | PMS API (Opera, Mews, Cloudbeds, etc.) |
| `CompetitorPricingConnector` | Rate-shopping tool (RateGain, OTA Insight, Lighthouse) |
| `EventCalendarConnector` | City/convention bureau API, PredictHQ, Ticketmaster |
| `OccupancyHistoryConnector` | Your data warehouse / BI store |
| `ChannelRateUpdater.push_rate` | Channel manager API (SiteMinder, RateGain, Cloudbeds Channel Manager) |

Each connector/tool keeps the same interface, so `agent.py` doesn't change
when you point it at production systems.

---
name: revenue-agent
description: Run or scaffold a dynamic revenue-management / pricing agent that reads booking patterns, competitor pricing sheets, and event calendars, retrieves historical occupancy data, computes explainable rate recommendations, flags demand anomalies (like sudden spikes tied to events), simulates pushing rates across distribution channels, and produces a cited Revenue Strategy Brief in Markdown. Use this any time the user mentions revenue management, dynamic pricing, rate optimization, RevPAR/ADR/occupancy analysis, competitor rate shopping, demand forecasting for time-varying-price inventory (hotels, short-term rentals, event ticketing, car rental fleets), or asks to build/extend/run a "revenue agent" or "pricing agent" — even without those exact words. If the user has their own data files, run the bundled pipeline on them directly. Otherwise, or for a non-hospitality domain, scaffold an adapted version instead of starting from scratch.
---

# Revenue Management Agent

A five-stage pipeline — **perceive → analyze → plan → act → report** — that
turns booking, competitor, and event data into explainable dynamic pricing
recommendations and a cited strategy brief. Fully rule-based (no LLM calls in
the core loop), so recommendations are auditable and the pipeline runs in
milliseconds, not seconds.

## When to run vs. when to scaffold

**Run the bundled pipeline** when the user has (or can point to) real or
sample data files — CSV/JSON for bookings, competitor rates, events, and
historical occupancy. This is the common case; default to this.

**Scaffold a new/adapted version** when:
- The user is starting a new project from this pattern (e.g. "build me a
  revenue management agent" with no existing data)
- The domain isn't hospitality (event ticketing, car rentals, SaaS seats)
- The user wants to modify pipeline internals, not just run it

Both paths use the same bundled code — scaffolding just means copying
`scripts/` into the user's project and adapting it (see
`references/data_schemas.md`) rather than running it in place.

## Running the pipeline

```bash
python scripts/run_pipeline.py \
  --bookings <path/to/bookings.csv> \
  --competitor <path/to/competitor_rates.csv> \
  --events <path/to/events.json> \
  --occupancy-history <path/to/occupancy_history.csv> \
  --property-name "<name>" \
  --out revenue_strategy_brief.md
```

Any `--path` flag can be omitted — the script falls back to bundled sample
data in `assets/sample_data/` for that input, so it's always runnable
end-to-end even before the user's real files are ready (useful for a first
demo run, or to show the expected output shape before mapping their data).

If the user's files don't match the expected column names (see
`references/data_schemas.md`), **adapt `scripts/connectors.py` to their
actual schema** rather than asking them to reformat their files — mapping
column names in code is almost always less friction for the user.

After running, read the generated brief and summarize the headline findings
in the chat response (top rate moves, anomaly count, any held-back dates) —
don't just say "done, see the file."

## What the pipeline does, stage by stage

1. **Perceive** (`connectors.py`) — reads bookings, competitor rates, event
   calendar, and historical occupancy through adapter classes with a
   consistent `fetch()` interface.
2. **Analyze** (`anomaly.py`) — flags demand anomalies two ways: sudden
   pickup-pace spikes/drops vs. the trailing set's average, and occupancy
   vs. the same date last year. Severity is `info` / `watch` / `critical`.
3. **Plan** (`pricing_engine.py`) — computes a recommended rate per date by
   combining an occupancy factor, a pickup-pace factor, and an event-impact
   factor, then blends 70/30 toward the competitor market index. Hard
   guardrails clamp the result to a max ±15% move per cycle and an absolute
   floor/ceiling. Every recommendation carries a plain-English rationale.
4. **Act** (`channel_updater.py`) — simulates pushing approved rates to
   distribution channels (direct engine, OTAs, GDS). Dates with a
   `critical`-severity anomaly are held back from this push by default —
   the agent recommends, it doesn't blindly reprice on an unexplained spike.
5. **Report** (`report.py`) — assembles a Markdown brief: executive summary,
   the rate-recommendation table with rationale, the anomaly log, the
   channel push log, and cited market intelligence (every competitor rate
   and event carries its source feed).

## Extending or tuning

Don't rewrite the pipeline from scratch for common asks. Point changes at
the right layer instead:

| User asks for... | Change this |
|---|---|
| Different data source (real PMS/API) | `connectors.py` — swap the connector's `fetch()` body |
| Tighter/looser anomaly sensitivity | `anomaly.py::AnomalyDetector(watch_threshold=, critical_threshold=)` |
| Different pricing logic/curve | `pricing_engine.py::DynamicPricingEngine` factor methods |
| Auto-push through anomalies | `agent.py::RevenueManagementAgent(auto_push_critical_anomalies=True)` |
| Real channel-manager integration | `channel_updater.py::ChannelRateUpdater.push_rate` |
| Non-hotel domain | See "Domain adaptation" in `references/data_schemas.md` |

Full column-level schemas and a domain-adaptation walkthrough are in
`references/data_schemas.md` — read it before adapting connectors or
scaffolding a new domain.

## Deploying a scaffolded instance

If the user wants the scaffolded/run project hosted (not just run locally),
that's a separate concern from this skill — help them wrap `agent.py` in a
small web server (Flask is sufficient: one route to render the brief, one
to re-run) and deploy it with standard Linux server practices (systemd or
Docker, Nginx in front, firewall rules). Don't fold deployment concerns into
the pipeline code itself.

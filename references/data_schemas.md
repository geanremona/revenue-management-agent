# Data Schemas & Extension Points

## Input file schemas

### bookings.csv (required columns)
| Column | Type | Meaning |
|---|---|---|
| stay_date | YYYY-MM-DD | The night being priced |
| bookings_on_the_books | int | Rooms already booked for that date |
| rooms_available | int | Total sellable inventory for that date |
| current_adr | float | Current average daily rate on file |
| avg_length_of_stay | float | Average nights per booking touching this date |
| pickup_last_7d | int | Rooms picked up in the trailing 7 days for this date |

### competitor_rates.csv (required columns)
| Column | Type | Meaning |
|---|---|---|
| stay_date | YYYY-MM-DD | Must align with bookings.csv dates to be used |
| competitor | string | Competitor name |
| rate | float | Their rate for that date |
| source | string | Where this was captured — shown as a citation in the brief |

### events.json (array of objects)
```json
[{"event": "...", "start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD",
  "expected_attendance": 12000, "demand_impact": "high|medium|low",
  "source": "..."}]
```

### occupancy_history.csv (required columns)
| Column | Type | Meaning |
|---|---|---|
| stay_date_ly | YYYY-MM-DD | The comparable date ~364 days prior |
| occupancy_pct_ly | float | Occupancy % achieved that date last year |
| adr_ly | float | ADR achieved that date last year |
| revpar_ly | float | RevPAR achieved that date last year |

> If the user's real data doesn't match these columns, adapt `connectors.py`
> rather than asking the user to reformat their files — mapping their actual
> column names is almost always less work for them.

---

## Extension points

| Component | File | Swap in |
|---|---|---|
| Booking data source | `src/connectors.py::BookingDataConnector` | PMS API (Opera, Mews, Cloudbeds) |
| Competitor pricing | `src/connectors.py::CompetitorPricingConnector` | Rate-shopping tool (RateGain, OTA Insight) |
| Event calendar | `src/connectors.py::EventCalendarConnector` | City/convention bureau API, PredictHQ, Ticketmaster |
| Occupancy history | `src/connectors.py::OccupancyHistoryConnector` | Data warehouse / BI store |
| Channel push | `src/channel_updater.py::ChannelRateUpdater.push_rate` | Real channel-manager API (SiteMinder, RateGain) |
| Dashboard API | `app.py::serialize_result` | Extend JSON keys for new dashboard panels |
| Manual overrides | `app.py::/api/override/approve` | Wire to real channel-manager API call |

Each connector/tool has the same `fetch()`/`push_rate()` interface, so
`src/agent.py` doesn't need to change when the underlying source changes —
only the connector's internals do.

---

## Tuning knobs

- `src/pricing_engine.py::DynamicPricingEngine(min_rate, max_rate, max_step_pct)`
  — hard floor/ceiling and per-cycle move cap. **Defaults: $120–$320, ±15%.**
- `src/anomaly.py::AnomalyDetector(watch_threshold, critical_threshold)`
  — % deviation from baseline that triggers "watch" vs "critical". **Defaults: 60% / 120%.**
  If a domain has less natural weekday/weekend swing than hotels
  (e.g. a stable B2B SaaS pricing use case), lower these — the hotel
  defaults are deliberately loose so normal cyclicality isn't over-flagged.
- `src/agent.py::RevenueManagementAgent(auto_push_critical_anomalies=False)`
  — set `True` to let anomalous dates auto-push instead of holding for review.
  Or trigger per-date from the dashboard using the **Approve & Push** UI button.

---

## Domain adaptation (non-hotel use)

The same five-stage pipeline (perceive → analyze → plan → act → report)
applies to any inventory with time-varying demand and competitor pricing —
e.g. short-term rentals, event ticketing, car rental fleets, or SaaS seat
pricing. To scaffold a new domain:

1. Redefine what "occupancy" means for that inventory (e.g. seats sold,
   fleet utilization %).
2. Rewrite the four connectors' field names to match the new domain's data.
3. Re-tune the pricing engine's factor tables (`_occupancy_factor`,
   `_pace_factor`, `_event_factor`) — the shape of the curve, not just the
   thresholds, may need to change for a domain with different elasticity.
4. Keep the guardrail/anomaly/report structure as-is — it's domain-agnostic.
5. The web dashboard (`app.py`, `templates/index.html`) is also domain-agnostic
   and requires no changes — it reads whatever `serialize_result()` emits.

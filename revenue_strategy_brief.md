# Revenue Strategy Brief — Revenue Pilot Test
*Generated 2026-07-04 21:10 by Revenue Management Agent*

## Executive Summary
- Reviewed **15** stay dates. Recommending **9 rate increases**, **6 decreases**, **0 holds**.
- **9 demand anomalies** flagged (3 critical) — see Section 3 before approving pushes.
- Channel sync: **47/48** rate pushes confirmed live, **1 queued for retry**.

## 1. Dynamic Rate Recommendations
| Stay Date | Current | Recommended | Δ% | Occupancy | Event |
|---|---|---|---|---|---|
| 2026-07-10 | $189.00 | **$193.65** | ▲ +2.5% | 78.9% | — |
| 2026-07-11 | $189.00 | **$192.78** | ▲ +2.0% | 83.3% | — |
| 2026-07-12 | $195.00 | **$224.25** | ▲ +15.0% | 88.9% | Riverside Music Festival |
| 2026-07-13 | $205.00 | **$235.75** | ▲ +15.0% | 95.0% | Riverside Music Festival |
| 2026-07-14 | $175.00 | **$163.18** | ▼ -6.8% | 32.2% | Mid-week lull (no events) |
| 2026-07-15 | $175.00 | **$161.26** | ▼ -7.9% | 33.3% | Mid-week lull (no events) |
| 2026-07-16 | $178.00 | **$164.03** | ▼ -7.8% | 35.0% | Mid-week lull (no events) |
| 2026-07-17 | $215.00 | **$247.25** | ▲ +15.0% | 98.3% | Regional Tech Summit |
| 2026-07-18 | $225.00 | **$258.75** | ▲ +15.0% | 99.4% | Regional Tech Summit |
| 2026-07-19 | $199.00 | **$202.98** | ▲ +2.0% | 77.8% | — |
| 2026-07-20 | $195.00 | **$198.90** | ▲ +2.0% | 73.3% | — |
| 2026-07-21 | $180.00 | **$168.31** | ▼ -6.5% | 38.9% | — |
| 2026-07-22 | $178.00 | **$164.03** | ▼ -7.8% | 37.8% | — |
| 2026-07-23 | $177.00 | **$163.11** | ▼ -7.8% | 36.7% | — |
| 2026-07-24 | $205.00 | **$211.96** | ▲ +3.4% | 83.3% | — |

**Rationale detail:**
- **2026-07-10** ($189.00 → $193.65):
    - Occupancy on the books: 78.9% (factor x1.02).
    - 7-day pickup pace: 18 rooms (factor x1.00).
    - No material event on the calendar for this date.
    - Competitor set average: $195.67. Blended 70/30 toward demand-driven target vs. market index.
- **2026-07-11** ($189.00 → $192.78):
    - Occupancy on the books: 83.3% (factor x1.02).
    - 7-day pickup pace: 22 rooms (factor x1.00).
    - No material event on the calendar for this date.
- **2026-07-12** ($195.00 → $224.25):
    - Occupancy on the books: 88.9% (factor x1.07).
    - 7-day pickup pace: 26 rooms (factor x1.03).
    - Event on calendar: 'Riverside Music Festival' (medium impact, factor x1.07).
    - Guardrail applied: raw model output $229.95 clamped to $224.25 (max ±15% per cycle, floor $120/ceiling $320).
- **2026-07-13** ($205.00 → $235.75):
    - Occupancy on the books: 95.0% (factor x1.12).
    - 7-day pickup pace: 31 rooms (factor x1.03).
    - Event on calendar: 'Riverside Music Festival' (medium impact, factor x1.07).
    - Guardrail applied: raw model output $253.04 clamped to $235.75 (max ±15% per cycle, floor $120/ceiling $320).
- **2026-07-14** ($175.00 → $163.18):
    - Occupancy on the books: 32.2% (factor x0.95).
    - 7-day pickup pace: 6 rooms (factor x0.97).
    - Event on calendar: 'Mid-week lull (no events)' (low impact, factor x1.00).
    - Competitor set average: $167.67. Blended 70/30 toward demand-driven target vs. market index.
- **2026-07-15** ($175.00 → $161.26):
    - Occupancy on the books: 33.3% (factor x0.95).
    - 7-day pickup pace: 5 rooms (factor x0.97).
    - Event on calendar: 'Mid-week lull (no events)' (low impact, factor x1.00).
- **2026-07-16** ($178.00 → $164.03):
    - Occupancy on the books: 35.0% (factor x0.95).
    - 7-day pickup pace: 4 rooms (factor x0.97).
    - Event on calendar: 'Mid-week lull (no events)' (low impact, factor x1.00).
- **2026-07-17** ($215.00 → $247.25):
    - Occupancy on the books: 98.3% (factor x1.12).
    - 7-day pickup pace: 64 rooms (factor x1.08).
    - Event on calendar: 'Regional Tech Summit' (high impact, factor x1.15).
    - Competitor set average: $239.00. Blended 70/30 toward demand-driven target vs. market index.
    - Guardrail applied: raw model output $281.05 clamped to $247.25 (max ±15% per cycle, floor $120/ceiling $320).
- **2026-07-18** ($225.00 → $258.75):
    - Occupancy on the books: 99.4% (factor x1.12).
    - 7-day pickup pace: 71 rooms (factor x1.08).
    - Event on calendar: 'Regional Tech Summit' (high impact, factor x1.15).
    - Competitor set average: $250.00. Blended 70/30 toward demand-driven target vs. market index.
    - Guardrail applied: raw model output $294.09 clamped to $258.75 (max ±15% per cycle, floor $120/ceiling $320).
- **2026-07-19** ($199.00 → $202.98):
    - Occupancy on the books: 77.8% (factor x1.02).
    - 7-day pickup pace: 20 rooms (factor x1.00).
    - No material event on the calendar for this date.
- **2026-07-20** ($195.00 → $198.90):
    - Occupancy on the books: 73.3% (factor x1.02).
    - 7-day pickup pace: 17 rooms (factor x1.00).
    - No material event on the calendar for this date.
- **2026-07-21** ($180.00 → $168.31):
    - Occupancy on the books: 38.9% (factor x0.95).
    - 7-day pickup pace: 9 rooms (factor x0.97).
    - No material event on the calendar for this date.
    - Competitor set average: $174.00. Blended 70/30 toward demand-driven target vs. market index.
- **2026-07-22** ($178.00 → $164.03):
    - Occupancy on the books: 37.8% (factor x0.95).
    - 7-day pickup pace: 8 rooms (factor x0.97).
    - No material event on the calendar for this date.
- **2026-07-23** ($177.00 → $163.11):
    - Occupancy on the books: 36.7% (factor x0.95).
    - 7-day pickup pace: 7 rooms (factor x0.97).
    - No material event on the calendar for this date.
- **2026-07-24** ($205.00 → $211.96):
    - Occupancy on the books: 83.3% (factor x1.02).
    - 7-day pickup pace: 25 rooms (factor x1.03).
    - No material event on the calendar for this date.
    - Competitor set average: $204.00. Blended 70/30 toward demand-driven target vs. market index.

## 2. Demand Anomalies Flagged
| Stay Date | Metric | Current | Baseline | Δ% | Severity | Note |
|---|---|---|---|---|---|---|
| 2026-07-18 | 7-day pickup pace | 71 | 22.2 | +219.8% | **CRITICAL** | Spike in bookings-in-last-7-days vs the trailing set average — investigate before repricing. |
| 2026-07-17 | 7-day pickup pace | 64 | 22.2 | +188.3% | **CRITICAL** | Spike in bookings-in-last-7-days vs the trailing set average — investigate before repricing. |
| 2026-07-13 | Occupancy vs. same period last year | 95.0 | 34.0 | +179.4% | **CRITICAL** | Demand materially ahead of last year's comparable date. |
| 2026-07-20 | Occupancy vs. same period last year | 73.3 | 40.0 | +83.2% | **WATCH** | Demand materially ahead of last year's comparable date. |
| 2026-07-16 | 7-day pickup pace | 4 | 22.2 | -82.0% | **WATCH** | Pickup pace lagging the set average — potential soft spot. |
| 2026-07-15 | 7-day pickup pace | 5 | 22.2 | -77.5% | **WATCH** | Pickup pace lagging the set average — potential soft spot. |
| 2026-07-14 | 7-day pickup pace | 6 | 22.2 | -73.0% | **WATCH** | Pickup pace lagging the set average — potential soft spot. |
| 2026-07-23 | 7-day pickup pace | 7 | 22.2 | -68.5% | **WATCH** | Pickup pace lagging the set average — potential soft spot. |
| 2026-07-22 | 7-day pickup pace | 8 | 22.2 | -64.0% | **WATCH** | Pickup pace lagging the set average — potential soft spot. |

## 3. Channel Distribution Log
| Stay Date | Channel | Rate Pushed | Status | Detail |
|---|---|---|---|---|
| 2026-07-10 | Direct Booking Engine | $193.65 | ✅ success | Rate confirmed live on channel. |
| 2026-07-10 | Booking.com | $193.65 | ✅ success | Rate confirmed live on channel. |
| 2026-07-10 | Expedia | $193.65 | ✅ success | Rate confirmed live on channel. |
| 2026-07-10 | GDS | $193.65 | ✅ success | Rate confirmed live on channel. |
| 2026-07-11 | Direct Booking Engine | $192.78 | ✅ success | Rate confirmed live on channel. |
| 2026-07-11 | Booking.com | $192.78 | ✅ success | Rate confirmed live on channel. |
| 2026-07-11 | Expedia | $192.78 | ✅ success | Rate confirmed live on channel. |
| 2026-07-11 | GDS | $192.78 | ✅ success | Rate confirmed live on channel. |
| 2026-07-12 | Direct Booking Engine | $224.25 | ✅ success | Rate confirmed live on channel. |
| 2026-07-12 | Booking.com | $224.25 | ✅ success | Rate confirmed live on channel. |
| 2026-07-12 | Expedia | $224.25 | ✅ success | Rate confirmed live on channel. |
| 2026-07-12 | GDS | $224.25 | ✅ success | Rate confirmed live on channel. |
| 2026-07-14 | Direct Booking Engine | $163.18 | ✅ success | Rate confirmed live on channel. |
| 2026-07-14 | Booking.com | $163.18 | ✅ success | Rate confirmed live on channel. |
| 2026-07-14 | Expedia | $163.18 | ✅ success | Rate confirmed live on channel. |
| 2026-07-14 | GDS | $163.18 | ✅ success | Rate confirmed live on channel. |
| 2026-07-15 | Direct Booking Engine | $161.26 | ✅ success | Rate confirmed live on channel. |
| 2026-07-15 | Booking.com | $161.26 | ✅ success | Rate confirmed live on channel. |
| 2026-07-15 | Expedia | $161.26 | ✅ success | Rate confirmed live on channel. |
| 2026-07-15 | GDS | $161.26 | ✅ success | Rate confirmed live on channel. |
| 2026-07-16 | Direct Booking Engine | $164.03 | ✅ success | Rate confirmed live on channel. |
| 2026-07-16 | Booking.com | $164.03 | ✅ success | Rate confirmed live on channel. |
| 2026-07-16 | Expedia | $164.03 | ✅ success | Rate confirmed live on channel. |
| 2026-07-16 | GDS | $164.03 | ✅ success | Rate confirmed live on channel. |
| 2026-07-19 | Direct Booking Engine | $202.98 | ✅ success | Rate confirmed live on channel. |
| 2026-07-19 | Booking.com | $202.98 | ✅ success | Rate confirmed live on channel. |
| 2026-07-19 | Expedia | $202.98 | ✅ success | Rate confirmed live on channel. |
| 2026-07-19 | GDS | $202.98 | ✅ success | Rate confirmed live on channel. |
| 2026-07-20 | Direct Booking Engine | $198.90 | ✅ success | Rate confirmed live on channel. |
| 2026-07-20 | Booking.com | $198.90 | ✅ success | Rate confirmed live on channel. |
| 2026-07-20 | Expedia | $198.90 | ✅ success | Rate confirmed live on channel. |
| 2026-07-20 | GDS | $198.90 | ✅ success | Rate confirmed live on channel. |
| 2026-07-21 | Direct Booking Engine | $168.31 | ✅ success | Rate confirmed live on channel. |
| 2026-07-21 | Booking.com | $168.31 | ✅ success | Rate confirmed live on channel. |
| 2026-07-21 | Expedia | $168.31 | ✅ success | Rate confirmed live on channel. |
| 2026-07-21 | GDS | $168.31 | ✅ success | Rate confirmed live on channel. |
| 2026-07-22 | Direct Booking Engine | $164.03 | ✅ success | Rate confirmed live on channel. |
| 2026-07-22 | Booking.com | $164.03 | ✅ success | Rate confirmed live on channel. |
| 2026-07-22 | Expedia | $164.03 | ✅ success | Rate confirmed live on channel. |
| 2026-07-22 | GDS | $164.03 | ✅ success | Rate confirmed live on channel. |
| 2026-07-23 | Direct Booking Engine | $163.11 | ✅ success | Rate confirmed live on channel. |
| 2026-07-23 | Booking.com | $163.11 | ⚠️ failed | Timeout from channel endpoint — queued for retry. |
| 2026-07-23 | Expedia | $163.11 | ✅ success | Rate confirmed live on channel. |
| 2026-07-23 | GDS | $163.11 | ✅ success | Rate confirmed live on channel. |
| 2026-07-24 | Direct Booking Engine | $211.96 | ✅ success | Rate confirmed live on channel. |
| 2026-07-24 | Booking.com | $211.96 | ✅ success | Rate confirmed live on channel. |
| 2026-07-24 | Expedia | $211.96 | ✅ success | Rate confirmed live on channel. |
| 2026-07-24 | GDS | $211.96 | ✅ success | Rate confirmed live on channel. |

## 4. Cited Market Intelligence
**Competitor rate shopping:**
- **2026-07-10**: Harbor Grand Hotel $199.00, Riverside Suites $179.00, Metro Plaza $209.00  _(source: extranet_scrape)_
- **2026-07-14**: Harbor Grand Hotel $169.00, Riverside Suites $159.00, Metro Plaza $175.00  _(source: extranet_scrape)_
- **2026-07-17**: Harbor Grand Hotel $239.00, Riverside Suites $229.00, Metro Plaza $249.00  _(source: extranet_scrape)_
- **2026-07-18**: Harbor Grand Hotel $255.00, Riverside Suites $235.00, Metro Plaza $260.00  _(source: extranet_scrape)_
- **2026-07-21**: Harbor Grand Hotel $175.00, Riverside Suites $165.00, Metro Plaza $182.00  _(source: extranet_scrape)_
- **2026-07-24**: Harbor Grand Hotel $205.00, Riverside Suites $195.00, Metro Plaza $212.00  _(source: extranet_scrape)_

**Event calendar catalysts:**
- **Regional Tech Summit** (2026-07-17 to 2026-07-18), expected attendance ~12,000, demand impact: high  _(source: city_convention_bureau_feed)_
- **Riverside Music Festival** (2026-07-12 to 2026-07-13), expected attendance ~8,000, demand impact: medium  _(source: city_events_api)_
- **Mid-week lull (no events)** (2026-07-14 to 2026-07-16), expected attendance ~0, demand impact: low  _(source: city_events_api)_

---
*All recommendations are advisory. Rates above are held to a ±15% per-cycle guardrail and a $120–$320 floor/ceiling; a human revenue manager should confirm before any critical-severity anomaly date goes live.*
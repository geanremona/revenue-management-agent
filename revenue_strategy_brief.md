# Revenue Strategy Brief — Harborview Grand (Demo)
*Generated 2026-07-04 21:26 by Revenue Management Agent*

## Executive Summary
- Reviewed **15** stay dates. Recommending **9 rate increases**, **6 decreases**, **0 holds**.
- **4 demand anomalies** flagged (3 critical) — see Section 3 before approving pushes.
- Channel sync: **46/48** rate pushes confirmed live, **2 queued for retry**.

## 1. Dynamic Rate Recommendations
| Stay Date | Current | Recommended | Δ% | Occupancy | Event |
|---|---|---|---|---|---|
| 2026-07-10 | $189.00 | **$196.38** | ▲ +3.9% | 78.9% | — |
| 2026-07-11 | $189.00 | **$196.56** | ▲ +4.0% | 83.3% | — |
| 2026-07-12 | $195.00 | **$234.00** | ▲ +20.0% | 88.9% | Riverside Music Festival |
| 2026-07-13 | $205.00 | **$246.00** | ▲ +20.0% | 95.0% | Riverside Music Festival |
| 2026-07-14 | $175.00 | **$162.35** | ▼ -7.2% | 32.2% | Mid-week lull (no events) |
| 2026-07-15 | $175.00 | **$161.02** | ▼ -8.0% | 33.3% | Mid-week lull (no events) |
| 2026-07-16 | $178.00 | **$163.79** | ▼ -8.0% | 35.0% | Mid-week lull (no events) |
| 2026-07-17 | $215.00 | **$258.00** | ▲ +20.0% | 98.3% | Regional Tech Summit |
| 2026-07-18 | $225.00 | **$270.00** | ▲ +20.0% | 99.4% | Regional Tech Summit |
| 2026-07-19 | $199.00 | **$206.96** | ▲ +4.0% | 77.8% | — |
| 2026-07-20 | $195.00 | **$202.80** | ▲ +4.0% | 73.3% | — |
| 2026-07-21 | $180.00 | **$164.70** | ▼ -8.5% | 38.9% | — |
| 2026-07-22 | $178.00 | **$160.57** | ▼ -9.8% | 37.8% | — |
| 2026-07-23 | $177.00 | **$159.67** | ▼ -9.8% | 36.7% | — |
| 2026-07-24 | $205.00 | **$216.48** | ▲ +5.6% | 83.3% | — |

**Rationale detail:**
- **2026-07-10** ($189.00 → $196.38):
    - Occupancy on the books: 78.9% (factor x1.04).
    - 7-day pickup pace: 18 rooms (factor x1.00).
    - No material event on the calendar for this date.
    - Competitor set average: $195.67. Blended 80/20 toward demand-driven target vs. market index.
- **2026-07-11** ($189.00 → $196.56):
    - Occupancy on the books: 83.3% (factor x1.04).
    - 7-day pickup pace: 22 rooms (factor x1.00).
    - No material event on the calendar for this date.
- **2026-07-12** ($195.00 → $234.00):
    - Occupancy on the books: 88.9% (factor x1.10).
    - 7-day pickup pace: 26 rooms (factor x1.03).
    - Event on calendar: 'Riverside Music Festival' (medium impact, factor x1.10).
    - Guardrail applied: raw model output $243.03 clamped to $234.00 (max ±20% per cycle, floor $120/ceiling $400).
- **2026-07-13** ($205.00 → $246.00):
    - Occupancy on the books: 95.0% (factor x1.20).
    - 7-day pickup pace: 31 rooms (factor x1.03).
    - Event on calendar: 'Riverside Music Festival' (medium impact, factor x1.10).
    - Guardrail applied: raw model output $278.72 clamped to $246.00 (max ±20% per cycle, floor $120/ceiling $400).
- **2026-07-14** ($175.00 → $162.35):
    - Occupancy on the books: 32.2% (factor x0.93).
    - 7-day pickup pace: 6 rooms (factor x0.97).
    - Event on calendar: 'Mid-week lull (no events)' (low impact, factor x1.02).
    - Competitor set average: $167.67. Blended 80/20 toward demand-driven target vs. market index.
- **2026-07-15** ($175.00 → $161.02):
    - Occupancy on the books: 33.3% (factor x0.93).
    - 7-day pickup pace: 5 rooms (factor x0.97).
    - Event on calendar: 'Mid-week lull (no events)' (low impact, factor x1.02).
- **2026-07-16** ($178.00 → $163.79):
    - Occupancy on the books: 35.0% (factor x0.93).
    - 7-day pickup pace: 4 rooms (factor x0.97).
    - Event on calendar: 'Mid-week lull (no events)' (low impact, factor x1.02).
- **2026-07-17** ($215.00 → $258.00):
    - Occupancy on the books: 98.3% (factor x1.20).
    - 7-day pickup pace: 64 rooms (factor x1.08).
    - Event on calendar: 'Regional Tech Summit' (high impact, factor x1.25).
    - Competitor set average: $239.00. Blended 80/20 toward demand-driven target vs. market index.
    - Guardrail applied: raw model output $326.44 clamped to $258.00 (max ±20% per cycle, floor $120/ceiling $400).
- **2026-07-18** ($225.00 → $270.00):
    - Occupancy on the books: 99.4% (factor x1.20).
    - 7-day pickup pace: 71 rooms (factor x1.08).
    - Event on calendar: 'Regional Tech Summit' (high impact, factor x1.25).
    - Competitor set average: $250.00. Blended 80/20 toward demand-driven target vs. market index.
    - Guardrail applied: raw model output $341.60 clamped to $270.00 (max ±20% per cycle, floor $120/ceiling $400).
- **2026-07-19** ($199.00 → $206.96):
    - Occupancy on the books: 77.8% (factor x1.04).
    - 7-day pickup pace: 20 rooms (factor x1.00).
    - No material event on the calendar for this date.
- **2026-07-20** ($195.00 → $202.80):
    - Occupancy on the books: 73.3% (factor x1.04).
    - 7-day pickup pace: 17 rooms (factor x1.00).
    - No material event on the calendar for this date.
- **2026-07-21** ($180.00 → $164.70):
    - Occupancy on the books: 38.9% (factor x0.93).
    - 7-day pickup pace: 9 rooms (factor x0.97).
    - No material event on the calendar for this date.
    - Competitor set average: $174.00. Blended 80/20 toward demand-driven target vs. market index.
- **2026-07-22** ($178.00 → $160.57):
    - Occupancy on the books: 37.8% (factor x0.93).
    - 7-day pickup pace: 8 rooms (factor x0.97).
    - No material event on the calendar for this date.
- **2026-07-23** ($177.00 → $159.67):
    - Occupancy on the books: 36.7% (factor x0.93).
    - 7-day pickup pace: 7 rooms (factor x0.97).
    - No material event on the calendar for this date.
- **2026-07-24** ($205.00 → $216.48):
    - Occupancy on the books: 83.3% (factor x1.04).
    - 7-day pickup pace: 25 rooms (factor x1.03).
    - No material event on the calendar for this date.
    - Competitor set average: $204.00. Blended 80/20 toward demand-driven target vs. market index.

## 2. Demand Anomalies Flagged
| Stay Date | Metric | Current | Baseline | Δ% | Severity | Note |
|---|---|---|---|---|---|---|
| 2026-07-18 | 7-day pickup pace | 71 | 19.8 | +257.8% | **CRITICAL** | Spike in bookings-in-last-7-days vs the trimmed set average — investigate before repricing. |
| 2026-07-17 | 7-day pickup pace | 64 | 19.8 | +222.5% | **CRITICAL** | Spike in bookings-in-last-7-days vs the trimmed set average — investigate before repricing. |
| 2026-07-13 | Occupancy vs. same period last year | 95.0 | 34.0 | +179.4% | **CRITICAL** | Demand materially ahead of last year's comparable date. |
| 2026-07-20 | Occupancy vs. same period last year | 73.3 | 40.0 | +83.2% | **WATCH** | Demand materially ahead of last year's comparable date. |

## 3. Channel Distribution Log
| Stay Date | Channel | Rate Pushed | Status | Detail |
|---|---|---|---|---|
| 2026-07-10 | Direct Booking Engine | $196.38 | ✅ success | Rate confirmed live on channel. |
| 2026-07-10 | Booking.com | $196.38 | ✅ success | Rate confirmed live on channel. |
| 2026-07-10 | Expedia | $196.38 | ✅ success | Rate confirmed live on channel. |
| 2026-07-10 | GDS | $196.38 | ✅ success | Rate confirmed live on channel. |
| 2026-07-11 | Direct Booking Engine | $196.56 | ⚠️ failed | Timeout from channel endpoint — queued for retry. |
| 2026-07-11 | Booking.com | $196.56 | ✅ success | Rate confirmed live on channel. |
| 2026-07-11 | Expedia | $196.56 | ✅ success | Rate confirmed live on channel. |
| 2026-07-11 | GDS | $196.56 | ✅ success | Rate confirmed live on channel. |
| 2026-07-12 | Direct Booking Engine | $234.00 | ✅ success | Rate confirmed live on channel. |
| 2026-07-12 | Booking.com | $234.00 | ✅ success | Rate confirmed live on channel. |
| 2026-07-12 | Expedia | $234.00 | ✅ success | Rate confirmed live on channel. |
| 2026-07-12 | GDS | $234.00 | ✅ success | Rate confirmed live on channel. |
| 2026-07-14 | Direct Booking Engine | $162.35 | ✅ success | Rate confirmed live on channel. |
| 2026-07-14 | Booking.com | $162.35 | ✅ success | Rate confirmed live on channel. |
| 2026-07-14 | Expedia | $162.35 | ✅ success | Rate confirmed live on channel. |
| 2026-07-14 | GDS | $162.35 | ✅ success | Rate confirmed live on channel. |
| 2026-07-15 | Direct Booking Engine | $161.02 | ✅ success | Rate confirmed live on channel. |
| 2026-07-15 | Booking.com | $161.02 | ✅ success | Rate confirmed live on channel. |
| 2026-07-15 | Expedia | $161.02 | ✅ success | Rate confirmed live on channel. |
| 2026-07-15 | GDS | $161.02 | ✅ success | Rate confirmed live on channel. |
| 2026-07-16 | Direct Booking Engine | $163.79 | ✅ success | Rate confirmed live on channel. |
| 2026-07-16 | Booking.com | $163.79 | ✅ success | Rate confirmed live on channel. |
| 2026-07-16 | Expedia | $163.79 | ✅ success | Rate confirmed live on channel. |
| 2026-07-16 | GDS | $163.79 | ✅ success | Rate confirmed live on channel. |
| 2026-07-19 | Direct Booking Engine | $206.96 | ✅ success | Rate confirmed live on channel. |
| 2026-07-19 | Booking.com | $206.96 | ✅ success | Rate confirmed live on channel. |
| 2026-07-19 | Expedia | $206.96 | ✅ success | Rate confirmed live on channel. |
| 2026-07-19 | GDS | $206.96 | ✅ success | Rate confirmed live on channel. |
| 2026-07-20 | Direct Booking Engine | $202.80 | ✅ success | Rate confirmed live on channel. |
| 2026-07-20 | Booking.com | $202.80 | ⚠️ failed | Timeout from channel endpoint — queued for retry. |
| 2026-07-20 | Expedia | $202.80 | ✅ success | Rate confirmed live on channel. |
| 2026-07-20 | GDS | $202.80 | ✅ success | Rate confirmed live on channel. |
| 2026-07-21 | Direct Booking Engine | $164.70 | ✅ success | Rate confirmed live on channel. |
| 2026-07-21 | Booking.com | $164.70 | ✅ success | Rate confirmed live on channel. |
| 2026-07-21 | Expedia | $164.70 | ✅ success | Rate confirmed live on channel. |
| 2026-07-21 | GDS | $164.70 | ✅ success | Rate confirmed live on channel. |
| 2026-07-22 | Direct Booking Engine | $160.57 | ✅ success | Rate confirmed live on channel. |
| 2026-07-22 | Booking.com | $160.57 | ✅ success | Rate confirmed live on channel. |
| 2026-07-22 | Expedia | $160.57 | ✅ success | Rate confirmed live on channel. |
| 2026-07-22 | GDS | $160.57 | ✅ success | Rate confirmed live on channel. |
| 2026-07-23 | Direct Booking Engine | $159.67 | ✅ success | Rate confirmed live on channel. |
| 2026-07-23 | Booking.com | $159.67 | ✅ success | Rate confirmed live on channel. |
| 2026-07-23 | Expedia | $159.67 | ✅ success | Rate confirmed live on channel. |
| 2026-07-23 | GDS | $159.67 | ✅ success | Rate confirmed live on channel. |
| 2026-07-24 | Direct Booking Engine | $216.48 | ✅ success | Rate confirmed live on channel. |
| 2026-07-24 | Booking.com | $216.48 | ✅ success | Rate confirmed live on channel. |
| 2026-07-24 | Expedia | $216.48 | ✅ success | Rate confirmed live on channel. |
| 2026-07-24 | GDS | $216.48 | ✅ success | Rate confirmed live on channel. |

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
"""
pricing_engine.py
------------------
Rule-based dynamic pricing engine. Combines:
  - Occupancy-on-the-books (demand pressure)
  - Booking pace / pickup velocity (momentum)
  - Competitor market index (positioning)
  - Event calendar impact (known demand catalysts)
  - Anomaly flags (dampens or amplifies confidence)

This is intentionally rule-based and fully explainable — every recommended
rate ships with a plain-English rationale, which is what lets a revenue
manager trust and override the agent rather than treat it as a black box.
A production version could swap this for a learned elasticity/ML model
behind the same interface.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List

from connectors import BookingRecord, EventRecord, FlightCancellationRecord


@dataclass
class RateRecommendation:
    stay_date: str
    current_rate: float
    recommended_rate: float
    change_pct: float
    market_index: Optional[float]
    occupancy_pct: float
    event: Optional[str]
    flight_cancellation: Optional[str]
    rationale: List[str] = field(default_factory=list)


class DynamicPricingEngine:
    def __init__(self, min_rate: float = 120.0, max_rate: float = 400.0,
                 max_step_pct: float = 20.0):
        """Guardrail parameters.

        Changes from original defaults:
          max_rate:     $320 → $400  — captures premium event-night RevPAR
          max_step_pct: 15%  → 20%  — allows more aggressive moves on high-demand dates
        """
        self.min_rate = min_rate
        self.max_rate = max_rate
        self.max_step_pct = max_step_pct  # guardrail: max single-cycle rate move

    def _occupancy_factor(self, occ_pct: float) -> float:
        """Demand-pressure multiplier based on occupancy on the books.

        Sharpened from original to capture more yield at near-sellout
        and discount more aggressively on soft dates to drive volume:
          ≥95%: 1.12 → 1.20  (sellout premium)
          ≥85%: 1.07 → 1.10
          ≥70%: 1.02 → 1.04
          ≥30%: 0.95 → 0.93  (deeper discount to stimulate demand)
          <30%: 0.90 → 0.87
        """
        if occ_pct >= 95:
            return 1.20
        if occ_pct >= 85:
            return 1.10
        if occ_pct >= 70:
            return 1.04
        if occ_pct >= 45:
            return 1.00
        if occ_pct >= 30:
            return 0.93
        return 0.87

    def _pace_factor(self, pickup_last_7d: int) -> float:
        if pickup_last_7d >= 50:
            return 1.08
        if pickup_last_7d >= 25:
            return 1.03
        if pickup_last_7d >= 10:
            return 1.00
        return 0.97

    def _event_factor(self, event: Optional[EventRecord]) -> float:
        """Event-demand catalyst multiplier.

        Amplified from original to better monetise high-impact events:
          high:   1.15 → 1.25
          medium: 1.07 → 1.10
          low:    1.00 → 1.02 (small lift even on low-impact days)
        """
        if event is None:
            return 1.00
        return {"high": 1.25, "medium": 1.10, "low": 1.02}.get(event.demand_impact, 1.00)

    def _flight_cancellation_factor(self, cancellation: Optional[FlightCancellationRecord]) -> float:
        """Surge multiplier for stranded passengers."""
        if not cancellation or cancellation.estimated_stranded_passengers < 50:
            return 1.00
        if cancellation.estimated_stranded_passengers >= 1000:
            return 1.40
        if cancellation.estimated_stranded_passengers >= 500:
            return 1.25
        return 1.15

    def recommend(
        self,
        booking: BookingRecord,
        market_index: Optional[float],
        event: Optional[EventRecord],
        flight_cancellation: Optional[FlightCancellationRecord] = None,
    ) -> RateRecommendation:
        rationale: List[str] = []

        occ_factor = self._occupancy_factor(booking.occupancy_pct)
        pace_factor = self._pace_factor(booking.pickup_last_7d)
        event_factor = self._event_factor(event)

        rationale.append(f"Occupancy on the books: {booking.occupancy_pct}% "
                          f"(factor x{occ_factor:.2f}).")
        rationale.append(f"7-day pickup pace: {booking.pickup_last_7d} rooms "
                          f"(factor x{pace_factor:.2f}).")
        if event:
            rationale.append(f"Event on calendar: '{event.event}' "
                              f"({event.demand_impact} impact, factor x{event_factor:.2f}).")
        else:
            rationale.append("No material event on the calendar for this date.")

        flight_factor = self._flight_cancellation_factor(flight_cancellation)
        if flight_cancellation and flight_factor > 1.0:
            rationale.append(f"CRITICAL CAUSALITY: {flight_cancellation.cancelled_flights} flight cancellations detected. "
                             f"~{flight_cancellation.estimated_stranded_passengers} stranded passengers. "
                             f"Applying surge factor x{flight_factor:.2f}.")

        base = booking.current_adr
        target = base * occ_factor * pace_factor * event_factor * flight_factor

        # Blend toward the competitive market index (80/20 model-to-competitor)
        # Shifted from original 70/30 — trusts own demand signal more,
        # reduces anchoring to competitor set which may under-price on event dates.
        if market_index:
            blended = 0.80 * target + 0.20 * market_index
            rationale.append(
                f"Competitor set average: ${market_index:.2f}. Blended 80/20 toward "
                f"demand-driven target vs. market index."
            )
            target = blended

        # Guardrails: cap single-cycle move and hard floor/ceiling
        max_up = base * (1 + self.max_step_pct / 100)
        max_down = base * (1 - self.max_step_pct / 100)
        pre_clamp = target
        target = max(min(target, max_up), max_down)
        target = max(min(target, self.max_rate), self.min_rate)
        if abs(pre_clamp - target) > 0.01:
            rationale.append(
                f"Guardrail applied: raw model output ${pre_clamp:.2f} clamped to "
                f"${target:.2f} (max ±{self.max_step_pct:.0f}% per cycle, "
                f"floor ${self.min_rate:.0f}/ceiling ${self.max_rate:.0f})."
            )

        recommended_rate = round(target, 2)
        change_pct = round(100 * (recommended_rate - base) / base, 1)

        return RateRecommendation(
            stay_date=booking.stay_date,
            current_rate=base,
            recommended_rate=recommended_rate,
            change_pct=change_pct,
            market_index=market_index,
            occupancy_pct=booking.occupancy_pct,
            event=event.event if event else None,
            flight_cancellation=f"{flight_cancellation.cancelled_flights} cancelled flights" if flight_cancellation else None,
            rationale=rationale,
        )

"""
anomaly.py
----------
Flags demand anomalies by comparing current booking pace and occupancy
against a historical (same-weekday-last-year) baseline, using a simple
robust z-score. In production this would run on a longer trailing window
and could layer in a proper STL/seasonal decomposition, but the z-score
approach is transparent and auditable, which matters for revenue teams.
"""
from __future__ import annotations
from dataclasses import dataclass
from statistics import mean, pstdev
from typing import List

from connectors import BookingRecord, OccupancyHistoryRecord


@dataclass
class AnomalyFlag:
    stay_date: str
    metric: str
    current_value: float
    baseline_value: float
    delta_pct: float
    severity: str  # "info" | "watch" | "critical"
    note: str


class AnomalyDetector:
    def __init__(self, watch_threshold: float = 60.0, critical_threshold: float = 120.0):
        """Thresholds are % deviation from baseline pickup/occupancy."""
        self.watch_threshold = watch_threshold
        self.critical_threshold = critical_threshold

    def _severity(self, delta_pct: float) -> str:
        magnitude = abs(delta_pct)
        if magnitude >= self.critical_threshold:
            return "critical"
        if magnitude >= self.watch_threshold:
            return "watch"
        return "info"

    def detect(
        self,
        bookings: List[BookingRecord],
        history_lookup,
    ) -> List[AnomalyFlag]:
        flags: List[AnomalyFlag] = []

        # Baseline pickup pace from the trailing set itself (median pickup)
        pickups = [b.pickup_last_7d for b in bookings]
        baseline_pickup = mean(pickups) if pickups else 0

        for b in bookings:
            # 1. Pickup-velocity anomaly (sudden demand spike/drop vs the set's own trend)
            if baseline_pickup > 0:
                delta_pct = round(100 * (b.pickup_last_7d - baseline_pickup) / baseline_pickup, 1)
                if abs(delta_pct) >= self.watch_threshold:
                    flags.append(AnomalyFlag(
                        stay_date=b.stay_date,
                        metric="7-day pickup pace",
                        current_value=b.pickup_last_7d,
                        baseline_value=round(baseline_pickup, 1),
                        delta_pct=delta_pct,
                        severity=self._severity(delta_pct),
                        note="Spike in bookings-in-last-7-days vs the trailing set average — "
                             "investigate before repricing." if delta_pct > 0 else
                             "Pickup pace lagging the set average — potential soft spot.",
                    ))

            # 2. Occupancy-vs-last-year anomaly
            hist: OccupancyHistoryRecord | None = history_lookup(b.stay_date)
            if hist:
                delta_pct = round(100 * (b.occupancy_pct - hist.occupancy_pct_ly) / hist.occupancy_pct_ly, 1)
                if abs(delta_pct) >= self.watch_threshold:
                    flags.append(AnomalyFlag(
                        stay_date=b.stay_date,
                        metric="Occupancy vs. same period last year",
                        current_value=b.occupancy_pct,
                        baseline_value=hist.occupancy_pct_ly,
                        delta_pct=delta_pct,
                        severity=self._severity(delta_pct),
                        note="Demand materially ahead of last year's comparable date." if delta_pct > 0
                             else "Demand materially behind last year's comparable date.",
                    ))

        return sorted(flags, key=lambda f: (-abs(f.delta_pct)))

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
    def __init__(self, watch_threshold: float = 80.0, critical_threshold: float = 150.0):
        """Thresholds are % deviation from baseline pickup/occupancy.

        Raised from original 60/120 defaults to 80/150:
        - Reduces false-positive "watch" flags caused by normal weekday/weekend swing.
        - Critical holds are now reserved for genuinely extreme demand spikes (>150%).
        - Adjust lower for more sensitive monitoring of stable-demand properties.
        """
        self.watch_threshold = watch_threshold
        self.critical_threshold = critical_threshold

    def _severity(self, delta_pct: float) -> str:
        magnitude = abs(delta_pct)
        if magnitude >= self.critical_threshold:
            return "critical"
        if magnitude >= self.watch_threshold:
            return "watch"
        return "info"

    @staticmethod
    def _trimmed_mean(values: List[float], trim_pct: float = 0.10) -> float:
        """Mean after discarding the top and bottom trim_pct fraction.
        More robust than plain mean when the batch contains extreme event outliers."""
        if not values:
            return 0.0
        n = len(values)
        cut = max(1, int(n * trim_pct))
        trimmed = sorted(values)[cut:-cut] if n > 2 * cut else values
        return mean(trimmed)

    def detect(
        self,
        bookings: List[BookingRecord],
        history_lookup,
    ) -> List[AnomalyFlag]:
        flags: List[AnomalyFlag] = []

        # Baseline pickup: trimmed mean (drop top+bottom 10%) to reduce event-date distortion
        pickups = [float(b.pickup_last_7d) for b in bookings]
        baseline_pickup = self._trimmed_mean(pickups)
        # Secondary guard: only flag if deviation also exceeds 1 std-dev of the set
        pickup_std = pstdev(pickups) if len(pickups) > 1 else 0.0

        # Baseline occupancy for z-score guard
        occs = [b.occupancy_pct for b in bookings]
        occ_std = pstdev(occs) if len(occs) > 1 else 0.0

        for b in bookings:
            # 1. Pickup-velocity anomaly
            if baseline_pickup > 0:
                deviation = b.pickup_last_7d - baseline_pickup
                delta_pct = round(100 * deviation / baseline_pickup, 1)
                # Must exceed % threshold AND 1 std-dev to avoid flagging normal cyclicality
                if abs(delta_pct) >= self.watch_threshold and (pickup_std == 0 or abs(deviation) >= pickup_std):
                    flags.append(AnomalyFlag(
                        stay_date=b.stay_date,
                        metric="7-day pickup pace",
                        current_value=b.pickup_last_7d,
                        baseline_value=round(baseline_pickup, 1),
                        delta_pct=delta_pct,
                        severity=self._severity(delta_pct),
                        note="Spike in bookings-in-last-7-days vs the trimmed set average — "
                             "investigate before repricing." if delta_pct > 0 else
                             "Pickup pace lagging the trimmed set average — potential soft spot.",
                    ))

            # 2. Occupancy-vs-last-year anomaly
            hist: OccupancyHistoryRecord | None = history_lookup(b.stay_date)
            if hist and hist.occupancy_pct_ly > 0:
                occ_deviation = b.occupancy_pct - hist.occupancy_pct_ly
                delta_pct = round(100 * occ_deviation / hist.occupancy_pct_ly, 1)
                if abs(delta_pct) >= self.watch_threshold and (occ_std == 0 or abs(occ_deviation) >= occ_std):
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

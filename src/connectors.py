"""
connectors.py
--------------
Ingestion layer. Each connector is a thin adapter with a `fetch()` method.
In production, swap the CSV/JSON readers for real integrations:
  - BookingDataConnector      -> PMS API (Opera, Mews, Cloudbeds...)
  - CompetitorPricingConnector-> rate-shopping tool (RateGain, OTA Insight...)
  - EventCalendarConnector    -> city/convention bureau API, Ticketmaster, PredictHQ
  - OccupancyHistoryConnector -> data warehouse / BI store

Keeping the interface identical means the orchestration agent (agent.py)
never needs to change when a data source is swapped out.
"""
from __future__ import annotations
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict


@dataclass
class BookingRecord:
    stay_date: str
    bookings_on_the_books: int
    rooms_available: int
    current_adr: float
    avg_length_of_stay: float
    pickup_last_7d: int

    @property
    def occupancy_pct(self) -> float:
        return round(100 * self.bookings_on_the_books / self.rooms_available, 1)


@dataclass
class CompetitorRate:
    stay_date: str
    competitor: str
    rate: float
    source: str


@dataclass
class EventRecord:
    event: str
    start_date: str
    end_date: str
    expected_attendance: int
    demand_impact: str
    source: str


@dataclass
class OccupancyHistoryRecord:
    stay_date_ly: str
    occupancy_pct_ly: float
    adr_ly: float
    revpar_ly: float


class BookingDataConnector:
    def __init__(self, path: str):
        self.path = Path(path)

    def fetch(self) -> List[BookingRecord]:
        with open(self.path, newline="") as f:
            reader = csv.DictReader(f)
            return [
                BookingRecord(
                    stay_date=row["stay_date"],
                    bookings_on_the_books=int(row["bookings_on_the_books"]),
                    rooms_available=int(row["rooms_available"]),
                    current_adr=float(row["current_adr"]),
                    avg_length_of_stay=float(row["avg_length_of_stay"]),
                    pickup_last_7d=int(row["pickup_last_7d"]),
                )
                for row in reader
            ]


class CompetitorPricingConnector:
    def __init__(self, path: str):
        self.path = Path(path)

    def fetch(self) -> List[CompetitorRate]:
        with open(self.path, newline="") as f:
            reader = csv.DictReader(f)
            return [
                CompetitorRate(
                    stay_date=row["stay_date"],
                    competitor=row["competitor"],
                    rate=float(row["rate"]),
                    source=row["source"],
                )
                for row in reader
            ]

    def market_index_by_date(self) -> Dict[str, float]:
        """Average competitor set rate per stay date -> our benchmark price point."""
        rates = self.fetch()
        by_date: Dict[str, List[float]] = {}
        for r in rates:
            by_date.setdefault(r.stay_date, []).append(r.rate)
        return {d: round(sum(v) / len(v), 2) for d, v in by_date.items()}


class EventCalendarConnector:
    def __init__(self, path: str):
        self.path = Path(path)

    def fetch(self) -> List[EventRecord]:
        with open(self.path) as f:
            raw = json.load(f)
        return [EventRecord(**item) for item in raw]

    def impact_by_date(self) -> Dict[str, EventRecord]:
        """Expand each event's date range into a per-day impact lookup."""
        from datetime import date, timedelta
        out: Dict[str, EventRecord] = {}
        for ev in self.fetch():
            y1, m1, d1 = map(int, ev.start_date.split("-"))
            y2, m2, d2 = map(int, ev.end_date.split("-"))
            cur, end = date(y1, m1, d1), date(y2, m2, d2)
            while cur <= end:
                out[cur.isoformat()] = ev
                cur += timedelta(days=1)
        return out


class OccupancyHistoryConnector:
    def __init__(self, path: str):
        self.path = Path(path)

    def fetch(self) -> List[OccupancyHistoryRecord]:
        with open(self.path, newline="") as f:
            reader = csv.DictReader(f)
            return [
                OccupancyHistoryRecord(
                    stay_date_ly=row["stay_date_ly"],
                    occupancy_pct_ly=float(row["occupancy_pct_ly"]),
                    adr_ly=float(row["adr_ly"]),
                    revpar_ly=float(row["revpar_ly"]),
                )
                for row in reader
            ]

    def by_current_date(self, current_stay_date: str) -> OccupancyHistoryRecord | None:
        """Map a current stay date to its same-weekday-last-year counterpart (~364 days back)."""
        from datetime import date, timedelta
        y, m, d = map(int, current_stay_date.split("-"))
        ly_date = (date(y, m, d) - timedelta(days=364)).isoformat()
        for rec in self.fetch():
            if rec.stay_date_ly == ly_date:
                return rec
        return None


@dataclass
class FlightCancellationRecord:
    stay_date: str
    cancelled_flights: int
    estimated_stranded_passengers: int
    source: str


class FlightCancellationConnector:
    def __init__(self):
        pass

    def fetch_live_cancellations(self) -> FlightCancellationRecord | None:
        """Simulate a live API pull from local airport showing a major storm today."""
        # For the hackathon demo, we hardcode "tonight" as 2026-07-10
        return FlightCancellationRecord(
            stay_date="2026-07-10",
            cancelled_flights=42,
            estimated_stranded_passengers=1250,
            source="airport_live_status_api"
        )

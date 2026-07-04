"""
agent.py
--------
The RevenueManagementAgent orchestrates the full cycle:

  1. PERCEIVE  — read bookings, competitor rates, event calendar, occupancy history
  2. ANALYZE   — flag demand anomalies against historical baselines
  3. PLAN      — compute per-date rate recommendations via the pricing engine
  4. ACT       — push approved rates across distribution channels (tool calls)
  5. REPORT    — generate a cited revenue strategy brief for human review

Anomalies of "critical" severity are held back from auto-push and routed
to human review instead — the agent recommends, it doesn't blindly act
on unexplained demand spikes.
"""
from __future__ import annotations
from typing import List, Dict

from connectors import (
    BookingDataConnector, CompetitorPricingConnector,
    EventCalendarConnector, OccupancyHistoryConnector,
)
from anomaly import AnomalyDetector, AnomalyFlag
from pricing_engine import DynamicPricingEngine, RateRecommendation
from channel_updater import ChannelRateUpdater, ChannelUpdateResult
from report import RevenueBriefGenerator


class RevenueManagementAgent:
    def __init__(
        self,
        bookings_path: str,
        competitor_path: str,
        events_path: str,
        occupancy_history_path: str,
        property_name: str = "Sample Property",
        auto_push_critical_anomalies: bool = False,
        cloudflare_account_id: str | None = None,
        cloudflare_api_token: str | None = None,
    ):
        self.booking_connector = BookingDataConnector(bookings_path)
        self.competitor_connector = CompetitorPricingConnector(competitor_path)
        self.event_connector = EventCalendarConnector(events_path)
        self.history_connector = OccupancyHistoryConnector(occupancy_history_path)

        self.anomaly_detector = AnomalyDetector()
        self.pricing_engine = DynamicPricingEngine()
        self.channel_updater = ChannelRateUpdater()
        self.report_generator = RevenueBriefGenerator(
            property_name=property_name,
            cloudflare_account_id=cloudflare_account_id,
            cloudflare_api_token=cloudflare_api_token,
        )

        self.auto_push_critical_anomalies = auto_push_critical_anomalies

    def run(self) -> Dict:
        # 1. PERCEIVE
        bookings = self.booking_connector.fetch()
        competitor_rates = self.competitor_connector.fetch()
        market_index = self.competitor_connector.market_index_by_date()
        events = self.event_connector.fetch()
        event_by_date = self.event_connector.impact_by_date()

        # 2. ANALYZE — anomaly detection
        anomalies: List[AnomalyFlag] = self.anomaly_detector.detect(
            bookings, history_lookup=self.history_connector.by_current_date
        )
        critical_dates = {a.stay_date for a in anomalies if a.severity == "critical"}

        # 3. PLAN — rate recommendations
        recommendations: List[RateRecommendation] = []
        for b in bookings:
            rec = self.pricing_engine.recommend(
                booking=b,
                market_index=market_index.get(b.stay_date),
                event=event_by_date.get(b.stay_date),
            )
            recommendations.append(rec)

        # 4. ACT — push to channels, holding back critical-anomaly dates unless overridden
        push_dates = {
            r.stay_date: r.recommended_rate
            for r in recommendations
            if r.stay_date not in critical_dates or self.auto_push_critical_anomalies
        }
        held_back = [r.stay_date for r in recommendations if r.stay_date in critical_dates
                     and not self.auto_push_critical_anomalies]
        channel_results: List[ChannelUpdateResult] = self.channel_updater.push_batch(push_dates)

        # 5. REPORT
        brief_md = self.report_generator.build(
            recommendations=recommendations,
            anomalies=anomalies,
            channel_results=channel_results,
            competitor_rates=competitor_rates,
            events=events,
        )

        # Revenue impact: total delta from current to recommended across all dates
        revenue_impact = sum(
            r.recommended_rate - r.current_rate for r in recommendations
        )

        return {
            "recommendations": recommendations,
            "anomalies": anomalies,
            "channel_results": channel_results,
            "held_back_dates": held_back,
            "brief_markdown": brief_md,
            "revenue_impact": round(revenue_impact, 2),
            "competitor_rates": competitor_rates,
            "events": events,
        }

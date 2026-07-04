"""
channel_updater.py
-------------------
Simulates the "tool call" layer that pushes approved rate changes out to
distribution channels (channel manager, OTAs, direct booking engine, GDS).

In production, `push_rate` would be a real API call, e.g. to a channel
manager like SiteMinder/RateGain/Cloudbeds Channel Manager, which then
fans out to each connected OTA. The interface here (one call per channel,
structured result, retry-friendly) is designed to map directly onto that.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict
import random
import logging
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@dataclass
class ChannelUpdateResult:
    stay_date: str
    channel: str
    rate_pushed: float
    status: str  # "success" | "failed"
    detail: str


class ChannelRateUpdater:
    DEFAULT_CHANNELS = ["Direct Booking Engine", "Booking.com", "Expedia", "GDS"]

    def __init__(self, channels: List[str] | None = None, simulate_failures: bool = True):
        self.channels = channels or self.DEFAULT_CHANNELS
        self.simulate_failures = simulate_failures

    def push_rate(self, stay_date: str, rate: float, channel: str) -> ChannelUpdateResult:
        """Simulated API call. Replace body with a real channel-manager API call."""
        if rate < 120.0 or rate > 400.0:
            logger.error(json.dumps({"event": "guardrail_violation", "stay_date": stay_date, "rate": rate, "channel": channel}))
            raise ValueError(f"Rate {rate} violates absolute safety guardrails ($120 - $400). Push aborted.")
            
        failed = self.simulate_failures and random.random() < 0.05  # ~5% transient failure rate
        
        log_payload = {
            "event": "channel_push",
            "stay_date": stay_date,
            "rate_pushed": rate,
            "channel": channel,
            "status": "failed" if failed else "success"
        }
        logger.info(json.dumps(log_payload))

        if failed:
            return ChannelUpdateResult(
                stay_date=stay_date, channel=channel, rate_pushed=rate,
                status="failed", detail="Timeout from channel endpoint — queued for retry.",
            )
        return ChannelUpdateResult(
            stay_date=stay_date, channel=channel, rate_pushed=rate,
            status="success", detail="Rate confirmed live on channel.",
        )

    def push_all(self, stay_date: str, rate: float) -> List[ChannelUpdateResult]:
        return [self.push_rate(stay_date, rate, ch) for ch in self.channels]

    def push_batch(self, rate_by_date: Dict[str, float]) -> List[ChannelUpdateResult]:
        results: List[ChannelUpdateResult] = []
        for stay_date, rate in rate_by_date.items():
            results.extend(self.push_all(stay_date, rate))
        return results

"""
report.py
---------
Assembles the final Revenue Strategy Brief: a Markdown document combining
rate recommendations, anomaly flags, channel push results, and cited
market intelligence (competitor rates + event calendar), so the human
revenue manager can review, sanity-check, and sign off in one place.
"""
from __future__ import annotations
from datetime import datetime
from typing import List, Dict

from pricing_engine import RateRecommendation
from anomaly import AnomalyFlag
from channel_updater import ChannelUpdateResult
from connectors import CompetitorRate, EventRecord


def _fmt_money(x: float) -> str:
    return f"${x:,.2f}"


class RevenueBriefGenerator:
    def __init__(self, property_name: str = "Sample Property"):
        self.property_name = property_name

    def build(
        self,
        recommendations: List[RateRecommendation],
        anomalies: List[AnomalyFlag],
        channel_results: List[ChannelUpdateResult],
        competitor_rates: List[CompetitorRate],
        events: List[EventRecord],
    ) -> str:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        lines: List[str] = []

        lines.append(f"# Revenue Strategy Brief — {self.property_name}")
        lines.append(f"*Generated {now} by Revenue Management Agent*\n")

        # --- Executive summary ---
        n_up = sum(1 for r in recommendations if r.change_pct > 0)
        n_down = sum(1 for r in recommendations if r.change_pct < 0)
        n_flat = len(recommendations) - n_up - n_down
        critical = [a for a in anomalies if a.severity == "critical"]
        lines.append("## Executive Summary")
        lines.append(
            f"- Reviewed **{len(recommendations)}** stay dates. Recommending "
            f"**{n_up} rate increases**, **{n_down} decreases**, **{n_flat} holds**."
        )
        lines.append(
            f"- **{len(anomalies)} demand anomalies** flagged "
            f"({len(critical)} critical) — see Section 3 before approving pushes."
        )
        failed_pushes = [c for c in channel_results if c.status == "failed"]
        lines.append(
            f"- Channel sync: **{len(channel_results) - len(failed_pushes)}/"
            f"{len(channel_results)}** rate pushes confirmed live"
            + (f", **{len(failed_pushes)} queued for retry**." if failed_pushes else ".")
        )
        lines.append("")

        # --- Rate recommendations ---
        lines.append("## 1. Dynamic Rate Recommendations")
        lines.append("| Stay Date | Current | Recommended | Δ% | Occupancy | Event |")
        lines.append("|---|---|---|---|---|---|")
        for r in recommendations:
            arrow = "▲" if r.change_pct > 0 else ("▼" if r.change_pct < 0 else "→")
            lines.append(
                f"| {r.stay_date} | {_fmt_money(r.current_rate)} | "
                f"**{_fmt_money(r.recommended_rate)}** | {arrow} {r.change_pct:+.1f}% | "
                f"{r.occupancy_pct}% | {r.event or '—'} |"
            )
        lines.append("")
        lines.append("**Rationale detail:**")
        for r in recommendations:
            lines.append(f"- **{r.stay_date}** ({_fmt_money(r.current_rate)} → "
                          f"{_fmt_money(r.recommended_rate)}):")
            for note in r.rationale:
                lines.append(f"    - {note}")
        lines.append("")

        # --- Anomalies ---
        lines.append("## 2. Demand Anomalies Flagged")
        if not anomalies:
            lines.append("No anomalies exceeded threshold this cycle.")
        else:
            lines.append("| Stay Date | Metric | Current | Baseline | Δ% | Severity | Note |")
            lines.append("|---|---|---|---|---|---|---|")
            for a in anomalies:
                lines.append(
                    f"| {a.stay_date} | {a.metric} | {a.current_value} | "
                    f"{a.baseline_value} | {a.delta_pct:+.1f}% | "
                    f"**{a.severity.upper()}** | {a.note} |"
                )
        lines.append("")

        # --- Channel push log ---
        lines.append("## 3. Channel Distribution Log")
        lines.append("| Stay Date | Channel | Rate Pushed | Status | Detail |")
        lines.append("|---|---|---|---|---|")
        for c in channel_results:
            status_flag = "✅" if c.status == "success" else "⚠️"
            lines.append(
                f"| {c.stay_date} | {c.channel} | {_fmt_money(c.rate_pushed)} | "
                f"{status_flag} {c.status} | {c.detail} |"
            )
        lines.append("")

        # --- Market intelligence, cited ---
        lines.append("## 4. Cited Market Intelligence")
        lines.append("**Competitor rate shopping:**")
        by_date: Dict[str, List[CompetitorRate]] = {}
        for c in competitor_rates:
            by_date.setdefault(c.stay_date, []).append(c)
        for d, rates in sorted(by_date.items()):
            rate_str = ", ".join(f"{r.competitor} {_fmt_money(r.rate)}" for r in rates)
            sources = ", ".join(sorted(set(r.source for r in rates)))
            lines.append(f"- **{d}**: {rate_str}  _(source: {sources})_")
        lines.append("")
        lines.append("**Event calendar catalysts:**")
        for e in events:
            lines.append(
                f"- **{e.event}** ({e.start_date} to {e.end_date}), "
                f"expected attendance ~{e.expected_attendance:,}, "
                f"demand impact: {e.demand_impact}  _(source: {e.source})_"
            )
        lines.append("")

        lines.append("---")
        lines.append(
            "*All recommendations are advisory. Rates above are held to a ±15% "
            "per-cycle guardrail and a $120–$320 floor/ceiling; a human revenue "
            "manager should confirm before any critical-severity anomaly date goes live.*"
        )

        return "\n".join(lines)

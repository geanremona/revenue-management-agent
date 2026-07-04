/* ============================================================
   Revenue Pilot — Dashboard Interactivity
   ============================================================ */

let chartInstance = null;

// --- Bootstrap ---
document.addEventListener('DOMContentLoaded', () => {
  fetchDashboardData();
});

// --- Data Fetching ---
async function fetchDashboardData() {
  try {
    const res = await fetch('/api/data');
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    const data = await res.json();
    renderAll(data);
  } catch (err) {
    console.error('Failed to fetch dashboard data:', err);
  }
}

function renderAll(data) {
  renderKPICards(data.summary);
  renderRateChart(data.recommendations);
  renderAnomalies(data.anomalies);
  renderEvents(data.events);
  renderChannels(data.channel_results);
  renderMarketIntel(data.competitor_rates, data.events);
  document.getElementById('generated-at').textContent = `Generated ${data.generated_at}`;
}

// --- Animated Counter ---
function animateValue(el, start, end, duration, prefix, suffix) {
  prefix = prefix || '';
  suffix = suffix || '';
  const range = end - start;
  const startTime = performance.now();

  function step(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = start + range * eased;
    if (Number.isInteger(end)) {
      el.textContent = prefix + Math.round(current).toLocaleString() + suffix;
    } else {
      el.textContent = prefix + current.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',') + suffix;
    }
    if (progress < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

// --- KPI Cards ---
function renderKPICards(s) {
  const revEl = document.getElementById('kpi-revenue-value');
  const impact = s.revenue_impact || 0;
  const sign = impact >= 0 ? '+$' : '-$';
  animateValue(revEl, 0, Math.abs(impact), 900, sign, '');

  const datesEl = document.getElementById('kpi-dates-value');
  animateValue(datesEl, 0, s.dates_reviewed, 600, '', '');
  document.getElementById('kpi-dates-sub').textContent =
    `${s.increases} ▲  ${s.decreases} ▼  ${s.holds} →`;

  const anomEl = document.getElementById('kpi-anomalies-value');
  animateValue(anomEl, 0, s.anomaly_count, 600, '', '');
  document.getElementById('kpi-anomalies-badges').innerHTML =
    `<span class="badge badge--critical">${s.critical_count} critical</span>`;

  const syncEl = document.getElementById('kpi-sync-value');
  syncEl.textContent = `${s.channel_success}/${s.channel_total}`;
  const failText = s.channel_failures > 0 ? `${s.channel_failures} queued for retry` : 'All confirmed';
  document.getElementById('kpi-sync-sub').textContent = failText;

  // Progress ring
  const pct = s.channel_total > 0 ? s.channel_success / s.channel_total : 1;
  const circ = 2 * Math.PI * 20; // r=20
  const offset = circ * (1 - pct);
  const ring = document.getElementById('sync-ring-fill');
  setTimeout(() => { ring.style.strokeDashoffset = offset; }, 200);
}

// --- Rate Chart ---
function renderRateChart(recommendations) {
  const ctx = document.getElementById('rate-chart').getContext('2d');
  const labels = recommendations.map(r => r.stay_date.slice(5)); // "07-10"
  const currentRates = recommendations.map(r => r.current_rate);
  const recRates = recommendations.map(r => r.recommended_rate);

  const recColors = recommendations.map(r =>
    r.change_pct > 0 ? 'rgba(45, 212, 191, 0.85)' : 'rgba(249, 112, 102, 0.85)'
  );
  const recBorders = recommendations.map(r =>
    r.change_pct > 0 ? '#2dd4bf' : '#f97066'
  );

  if (chartInstance) chartInstance.destroy();

  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'Current Rate',
          data: currentRates,
          backgroundColor: 'rgba(100, 116, 139, 0.35)',
          borderColor: 'rgba(100, 116, 139, 0.5)',
          borderWidth: 1,
          borderRadius: 4,
        },
        {
          label: 'Recommended Rate',
          data: recRates,
          backgroundColor: recColors,
          borderColor: recBorders,
          borderWidth: 1,
          borderRadius: 4,
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 800, easing: 'easeOutQuart' },
      interaction: { mode: 'index', intersect: false },
      scales: {
        x: {
          grid: { color: 'rgba(100,116,139,0.08)' },
          ticks: { color: '#64748b', font: { family: 'Inter', size: 11 } }
        },
        y: {
          beginAtZero: false,
          grid: { color: 'rgba(100,116,139,0.08)' },
          ticks: {
            color: '#64748b',
            font: { family: 'Inter', size: 11 },
            callback: v => '$' + v
          }
        }
      },
      plugins: {
        legend: {
          labels: {
            color: '#94a3b8',
            font: { family: 'Inter', size: 12 },
            usePointStyle: true,
            pointStyle: 'rectRounded',
            padding: 20
          }
        },
        tooltip: {
          backgroundColor: 'rgba(10, 15, 30, 0.95)',
          titleColor: '#f1f5f9',
          bodyColor: '#cbd5e1',
          borderColor: 'rgba(99,179,237,0.2)',
          borderWidth: 1,
          cornerRadius: 10,
          padding: 14,
          titleFont: { family: 'Inter', weight: '600' },
          bodyFont: { family: 'Inter', size: 12 },
          callbacks: {
            afterBody: function(context) {
              const idx = context[0].dataIndex;
              const rec = recommendations[idx];
              const lines = [];
              const arrow = rec.change_pct > 0 ? '▲' : (rec.change_pct < 0 ? '▼' : '→');
              lines.push(`${arrow} ${rec.change_pct > 0 ? '+' : ''}${rec.change_pct}%`);
              lines.push(`Occupancy: ${rec.occupancy_pct}%`);
              if (rec.event) lines.push(`Event: ${rec.event}`);
              if (rec.rationale && rec.rationale.length > 0) {
                lines.push('');
                rec.rationale.forEach(r => lines.push('• ' + r));
              }
              return lines;
            }
          }
        }
      }
    }
  });

  document.getElementById('chart-count').textContent =
    `${recommendations.length} stay dates`;
}

// --- Anomalies ---
function renderAnomalies(anomalies) {
  const container = document.getElementById('anomaly-list');
  document.getElementById('anomalies-count').textContent = `${anomalies.length} flagged`;

  if (anomalies.length === 0) {
    container.innerHTML = '<div style="padding:16px;color:#64748b;font-size:0.85rem;">No anomalies exceeded threshold this cycle.</div>';
    return;
  }

  container.innerHTML = anomalies.map(a => {
    const sev = a.severity.toLowerCase();
    const deltaSign = a.delta_pct > 0 ? '+' : '';
    const deltaClass = a.delta_pct > 0 ? 'delta--positive' : 'delta--negative';
    return `
      <div class="anomaly-item anomaly-item--${sev}">
        <div class="anomaly-item__body">
          <div class="anomaly-item__date">
            ${a.stay_date}
            <span class="badge badge--${sev}" style="margin-left:8px">${a.severity}</span>
          </div>
          <div class="anomaly-item__metric">${a.metric} — current: ${a.current_value} vs baseline: ${a.baseline_value}</div>
          <div class="anomaly-item__note">${a.note}</div>
        </div>
        <div class="anomaly-item__delta ${deltaClass}">${deltaSign}${a.delta_pct}%</div>
      </div>`;
  }).join('');
}

// --- Events ---
function renderEvents(events) {
  const container = document.getElementById('event-list');
  container.innerHTML = events.map(e => {
    const impact = e.demand_impact.toLowerCase();
    return `
      <div class="event-item event-item--${impact}">
        <div class="event-item__name">
          <span class="impact-dot impact-dot--${impact}"></span>
          ${e.event}
        </div>
        <div class="event-item__dates">${e.start_date} → ${e.end_date}</div>
        <div class="event-item__meta">
          <span>Attendance: ~${e.expected_attendance.toLocaleString()}</span>
          <span>Impact: ${e.demand_impact}</span>
          <span><em>${e.source}</em></span>
        </div>
      </div>`;
  }).join('');
}

// --- Channels ---
function renderChannels(results) {
  const tbody = document.getElementById('channel-tbody');
  const success = results.filter(r => r.status === 'success').length;
  const failed = results.length - success;
  document.getElementById('channel-count').textContent =
    `${success} success${failed > 0 ? `, ${failed} failed` : ''}`;

  tbody.innerHTML = results.map(r => {
    const icon = r.status === 'success'
      ? '<span class="status-icon status-icon--success">✅</span>'
      : '<span class="status-icon status-icon--failed">⚠️</span>';
    return `
      <tr>
        <td>${icon}</td>
        <td>${r.stay_date}</td>
        <td>${r.channel}</td>
        <td>$${r.rate_pushed.toFixed(2)}</td>
        <td>${r.detail}</td>
      </tr>`;
  }).join('');
}

// --- Market Intelligence ---
function renderMarketIntel(competitorRates, events) {
  // Competitor rates grouped by date
  const compList = document.getElementById('intel-comp-list');
  const byDate = {};
  competitorRates.forEach(c => {
    if (!byDate[c.stay_date]) byDate[c.stay_date] = [];
    byDate[c.stay_date].push(c);
  });

  compList.innerHTML = Object.keys(byDate).sort().map(date => {
    const rates = byDate[date];
    const rateStr = rates.map(r => `${r.competitor} $${r.rate.toFixed(2)}`).join(', ');
    const sources = [...new Set(rates.map(r => r.source))].join(', ');
    return `<div class="intel-item"><strong>${date}</strong>: ${rateStr} <em>(${sources})</em></div>`;
  }).join('');

  // Event catalysts
  const eventList = document.getElementById('intel-event-list');
  eventList.innerHTML = events.map(e =>
    `<div class="intel-item"><strong>${e.event}</strong> (${e.start_date} to ${e.end_date}), ` +
    `~${e.expected_attendance.toLocaleString()} attendees, impact: ${e.demand_impact} ` +
    `<em>(${e.source})</em></div>`
  ).join('');
}

// --- Rerun ---
async function handleRerun() {
  const btn = document.getElementById('btn-rerun');
  const overlay = document.getElementById('loading-overlay');

  btn.classList.add('loading');
  overlay.classList.add('active');

  try {
    const res = await fetch('/api/run', { method: 'POST' });
    if (!res.ok) throw new Error('Re-run failed');
    await fetchDashboardData();
  } catch (err) {
    console.error('Rerun error:', err);
    alert('Agent re-run failed. Check server logs.');
  } finally {
    btn.classList.remove('loading');
    overlay.classList.remove('active');
  }
}

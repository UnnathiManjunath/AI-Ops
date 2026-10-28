import os

JS_PATH = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\static\js\app.js"

with open(JS_PATH, "r", encoding="utf-8") as f:
    text = f.read()

start_marker = "async function injectFault(fault_type, sub_type) {"
end_marker = "// -------------------------------------------------------------------------\n// 5."

p1 = text.find(start_marker)
p2 = text.find(end_marker, p1)

if p1 != -1 and p2 != -1:
    new_code = """async function injectFault(fault_type, sub_type) {
  try {
    const res = await fetch('/api/inject-fault', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ fault_type, sub_type })
    });
    const data = await res.json();
    if (data.success) {
      currentIncidentId = data.incident_id;
      await fetchMetrics();
      await fetchIncidents(true); // select newly injected fault
      
      // Highlight the active incident
      const card = document.getElementById('diagnosisCard');
      if (card) {
        card.classList.add('ring-2', 'ring-sky-500');
        setTimeout(() => card.classList.remove('ring-2', 'ring-sky-500'), 1500);
      }

      const isUncritical = ['routine_hygiene', 'routine_gc_trim', 'routine_queue_balance', 'routine_audit_check'].includes(sub_type);
      const isCritical = ['core_dump', 'db_exhaustion', 'poison_pill', 'root_ca_broken'].includes(sub_type);

      if (isUncritical) {
        showToast('🟢 Uncritical Event Triggered', 'Routine maintenance: zero engineer wake-up. System resolving in background...', 'success');
        // Auto-diagnose and immediately auto-remediate without disturbing anyone
        setTimeout(async () => {
          await runAIDiagnosis();
          setTimeout(async () => {
            await executeRemediationPlan(false);
          }, 700);
        }, 400);
      } else if (isCritical) {
        showToast('🔴 Critical Emergency Triggered', 'High blast radius: Human Authorization Gate is MANDATORY!', 'error');
        setTimeout(async () => {
          await runAIDiagnosis();
        }, 400);
      } else {
        showToast('Fault Injected in Telemetry', data.message, 'warning');
        // Standard scenario: check autonomous mode
        if (typeof autonomousNightMode !== 'undefined' && autonomousNightMode) {
          setTimeout(async () => {
            await runAIDiagnosis();
            setTimeout(async () => {
              await executeRemediationPlan(false);
            }, 600);
          }, 400);
        } else {
          setTimeout(async () => {
            await runAIDiagnosis();
          }, 400);
        }
      }
    }
  } catch (err) {
    showToast('Injection Error', err.message, 'error');
  }
}

// Filter Scenario Cards in Sandbox (All, Uncritical, Critical)
function filterScenarioCards(filterType) {
  const btnAll = document.getElementById('filterBtn-all');
  const btnUncrit = document.getElementById('filterBtn-uncritical');
  const btnCrit = document.getElementById('filterBtn-critical');

  if (btnAll) btnAll.className = 'px-2.5 py-1 rounded text-xs font-semibold font-mono text-slate-400 hover:text-white transition';
  if (btnUncrit) btnUncrit.className = 'px-2.5 py-1 rounded text-xs font-semibold font-mono text-emerald-400 hover:bg-emerald-500/20 transition';
  if (btnCrit) btnCrit.className = 'px-2.5 py-1 rounded text-xs font-semibold font-mono text-rose-400 hover:bg-rose-500/20 transition';

  if (filterType === 'all') {
    if (btnAll) btnAll.className = 'px-2.5 py-1 rounded text-xs font-semibold font-mono bg-sky-600 text-white transition';
  } else if (filterType === 'uncritical') {
    if (btnUncrit) btnUncrit.className = 'px-2.5 py-1 rounded text-xs font-semibold font-mono bg-emerald-600 text-white transition';
  } else if (filterType === 'critical') {
    if (btnCrit) btnCrit.className = 'px-2.5 py-1 rounded text-xs font-semibold font-mono bg-rose-600 text-white transition';
  }

  const buttons = document.querySelectorAll('.scenario-btn');
  buttons.forEach(btn => {
    if (filterType === 'all') {
      btn.style.display = 'flex';
    } else if (filterType === 'uncritical') {
      btn.style.display = btn.classList.contains('scenario-uncritical') ? 'flex' : 'none';
    } else if (filterType === 'critical') {
      btn.style.display = (btn.classList.contains('scenario-critical') || btn.classList.contains('scenario-standard')) ? 'flex' : 'none';
    }
  });
}

"""
    updated = text[:p1] + new_code + text[p2:]
    with open(JS_PATH, "w", encoding="utf-8") as f:
        f.write(updated)
    print("app.js updated successfully with uncritical handlers and filterScenarioCards!")
else:
    print(f"Markers not found: p1={p1}, p2={p2}")

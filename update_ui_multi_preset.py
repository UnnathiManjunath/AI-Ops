import re
import os

PROJECT_DIR = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai"
INDEX_PATH = os.path.join(PROJECT_DIR, "templates", "index.html")
APP_JS_PATH = os.path.join(PROJECT_DIR, "static", "js", "app.js")

# =========================================================================
# 1. UPDATE templates/index.html
# =========================================================================
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Add Active Preset Badge in Top Header (near Safe Mode Active)
if 'id="topActivePresetBadge"' not in html:
    html = html.replace(
        '<span class="hidden md:inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">\n              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse mr-1.5"></span> Safe Mode Active\n            </span>',
        '<span class="hidden md:inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">\n              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse mr-1.5"></span> Safe Mode Active\n            </span>\n            <span id="topActivePresetBadge" class="hidden md:inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-sky-500/20 text-sky-300 border border-sky-500/30 font-mono">\n              🏦 GlobalPay Core Fintech\n            </span>'
    )

# Add IDs to the 12 buttons in Section 2 so updateSection2Buttons can target them
html = html.replace('onclick="injectFault(\'disk_overflow\', \'routine_hygiene\')"', 'id="sec2-disk-unc" onclick="injectFault(\'disk_overflow\', \'routine_hygiene\')"')
html = html.replace('onclick="injectFault(\'disk_overflow\', \'logs\')"', 'id="sec2-disk-warn" onclick="injectFault(\'disk_overflow\', \'logs\')"')
html = html.replace('onclick="injectFault(\'disk_overflow\', \'core_dump\')"', 'id="sec2-disk-crit" onclick="injectFault(\'disk_overflow\', \'core_dump\')"')

html = html.replace('onclick="injectFault(\'worker_stuck\', \'routine_gc_trim\')"', 'id="sec2-worker-unc" onclick="injectFault(\'worker_stuck\', \'routine_gc_trim\')"')
html = html.replace('onclick="injectFault(\'worker_stuck\', \'deadlock_clean\')"', 'id="sec2-worker-warn" onclick="injectFault(\'worker_stuck\', \'deadlock_clean\')"')
html = html.replace('onclick="injectFault(\'worker_stuck\', \'db_exhaustion\')"', 'id="sec2-worker-crit" onclick="injectFault(\'worker_stuck\', \'db_exhaustion\')"')

html = html.replace('onclick="injectFault(\'queue_growth\', \'routine_queue_balance\')"', 'id="sec2-queue-unc" onclick="injectFault(\'queue_growth\', \'routine_queue_balance\')"')
html = html.replace('onclick="injectFault(\'queue_growth\', \'traffic_surge\')"', 'id="sec2-queue-warn" onclick="injectFault(\'queue_growth\', \'traffic_surge\')"')
html = html.replace('onclick="injectFault(\'queue_growth\', \'poison_pill\')"', 'id="sec2-queue-crit" onclick="injectFault(\'queue_growth\', \'poison_pill\')"')

html = html.replace('onclick="injectFault(\'ssl_expiry\', \'routine_audit_check\')"', 'id="sec2-ssl-unc" onclick="injectFault(\'ssl_expiry\', \'routine_audit_check\')"')
html = html.replace('onclick="injectFault(\'ssl_expiry\', \'routine_renew\')"', 'id="sec2-ssl-warn" onclick="injectFault(\'ssl_expiry\', \'routine_renew\')"')
html = html.replace('onclick="injectFault(\'ssl_expiry\', \'root_ca_broken\')"', 'id="sec2-ssl-crit" onclick="injectFault(\'ssl_expiry\', \'root_ca_broken\')"')

# Add Scenario Switcher Bar right above Section 2 Quick Action Buttons
scenario_switcher_bar = '''
      <!-- Industry Dataset Profile Switcher (Judge Demonstration Highlight) -->
      <div class="mb-4 p-3 rounded-xl bg-[#070b14] border border-cyber-border flex flex-wrap items-center justify-between gap-3 shadow-inner">
        <div class="flex items-center space-x-2">
          <i data-lucide="layers" class="w-4 h-4 text-sky-400"></i>
          <span class="text-xs font-mono font-bold text-slate-200">Active Scenario Dataset:</span>
          <span id="activePresetBadge" class="text-xs font-mono font-semibold px-2 py-0.5 rounded bg-sky-500/20 text-sky-300 border border-sky-500/30">🏦 GlobalPay Fintech</span>
        </div>
        <div class="flex items-center flex-wrap gap-2 font-mono text-xs">
          <span class="text-[11px] text-slate-400 mr-1 hidden sm:inline">1-Click Switch:</span>
          <button id="btnPreset-ecommerce" onclick="loadDatasetPreset('ecommerce')" class="px-2.5 py-1.5 rounded-lg border border-cyber-border hover:border-amber-500 text-slate-300 hover:text-white transition flex items-center gap-1.5" title="Switch to QuickCart Food Delivery & Logistics Cloud">
            🛒 QuickCart (E-Commerce: 98.7% / 3.4k Riders)
          </button>
          <button id="btnPreset-healthcare" onclick="loadDatasetPreset('healthcare')" class="px-2.5 py-1.5 rounded-lg border border-cyber-border hover:border-rose-500 text-slate-300 hover:text-white transition flex items-center gap-1.5" title="Switch to LifeCare Hospital ICU Patient Cloud">
            🏥 LifeCare (Hospital ICU: 99.1% / 18 EMS)
          </button>
          <button id="btnPreset-fintech" onclick="loadDatasetPreset('fintech')" class="px-2.5 py-1.5 rounded-lg border font-mono text-xs transition flex items-center gap-1.5 bg-sky-600 text-white border-sky-400 shadow-md font-bold" title="Switch to GlobalPay Core Banking Infrastructure">
            🏦 GlobalPay (Fintech: 96.8% / $1.4M Recon)
          </button>
        </div>
      </div>
'''

if 'id="btnPreset-ecommerce"' not in html:
    # Insert right above Quick Action Injector Buttons
    needle = '<!-- Quick Action Injector Buttons -->'
    html = html.replace(needle, scenario_switcher_bar + "\n      " + needle)

# Now update uploadDatabaseModal with the 3 Preset Scenario Cards!
new_modal_options = '''
        <!-- Tab Option 1: Pre-Packaged Industry Scenarios (Judge Showcase) -->
        <div class="bg-[#0b101d] border border-cyber-border rounded-xl p-4 space-y-3">
          <div class="flex items-center justify-between">
            <label class="block text-slate-200 font-bold text-xs flex items-center gap-1.5">
              <i data-lucide="sparkles" class="w-4 h-4 text-sky-400"></i>
              Option A: Select & Switch Industry Scenario Dataset (3 Distinct Profiles)
            </label>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">1-Click Switch & Direct Downloads</span>
          </div>
          <p class="text-[11px] text-slate-400">
            Each dataset has completely distinct real-world metrics, units, and stakes across all 4 problem areas (Critical Disasters vs Uncritical Maintenance):
          </p>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-1">
            
            <!-- Card 1: QuickCart E-Commerce -->
            <div class="p-3 rounded-xl bg-[#070b14] border border-amber-500/30 hover:border-amber-400 transition flex flex-col justify-between space-y-2.5 shadow-lg">
              <div>
                <div class="flex items-center justify-between mb-1.5">
                  <span class="font-bold text-amber-300 text-xs flex items-center gap-1.5">
                    🛒 QuickCart E-Commerce
                  </span>
                  <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300">12 Runbooks</span>
                </div>
                <div class="text-[10px] text-slate-400 mb-2">Food Delivery & Real-Time Logistics</div>
                <div class="space-y-1 text-[10px] font-mono">
                  <div class="text-rose-400">🔴 Invoices: 98.7% (450MB left)</div>
                  <div class="text-rose-400">🔴 Dispatch: 3,420 Riders Locked</div>
                  <div class="text-rose-400">🔴 Kafka GPS: 184,000 msgs (88% Err)</div>
                  <div class="text-rose-400">🔴 Kitchen SSL: 4 Hours Left</div>
                  <div class="text-emerald-400 pt-1 border-t border-slate-800">🟢 Menu Previews: 51.4% (Uncritical)</div>
                  <div class="text-emerald-400">🟢 Rider GPS Queue: 620 msgs</div>
                </div>
              </div>
              <div class="space-y-1.5 pt-2 border-t border-slate-800">
                <button type="button" onclick="loadDatasetPreset('ecommerce')" class="w-full py-1.5 rounded-lg bg-amber-600 hover:bg-amber-500 text-white font-bold text-xs flex items-center justify-center gap-1.5 shadow transition">
                  <i data-lucide="zap" class="w-3.5 h-3.5"></i> Load QuickCart
                </button>
                <div class="flex items-center gap-1 text-[10px] font-mono">
                  <a href="/api/database/download-preset/ecommerce" download="QuickCart_ECommerce_Dataset.json" class="flex-1 py-1 rounded bg-slate-800 hover:bg-slate-700 text-amber-300 text-center transition">⬇ .JSON</a>
                  <a href="/api/database/download-preset-sql/ecommerce" download="QuickCart_ECommerce_Schema.sql" class="flex-1 py-1 rounded bg-slate-800 hover:bg-slate-700 text-amber-300 text-center transition">⬇ .SQL</a>
                  <a href="/api/database/download-preset-db/ecommerce" download="QuickCart_ECommerce.db" class="flex-1 py-1 rounded bg-slate-800 hover:bg-slate-700 text-amber-300 text-center transition">⬇ .DB</a>
                </div>
              </div>
            </div>

            <!-- Card 2: LifeCare Healthcare -->
            <div class="p-3 rounded-xl bg-[#070b14] border border-rose-500/30 hover:border-rose-400 transition flex flex-col justify-between space-y-2.5 shadow-lg">
              <div>
                <div class="flex items-center justify-between mb-1.5">
                  <span class="font-bold text-rose-300 text-xs flex items-center gap-1.5">
                    🏥 LifeCare Hospital ICU
                  </span>
                  <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300">12 Runbooks</span>
                </div>
                <div class="text-[10px] text-slate-400 mb-2">Hospital ICU & Emergency EMS Vitals</div>
                <div class="space-y-1 text-[10px] font-mono">
                  <div class="text-rose-400">🔴 Cardiac ECG: 99.1% (180MB left)</div>
                  <div class="text-rose-400">🔴 Ambulance: 18 Calls Locked</div>
                  <div class="text-rose-400">🔴 Bedside Vitals: 96,000 msgs (94% Err)</div>
                  <div class="text-rose-400">🔴 Telemed SSL: 5 Hours Left</div>
                  <div class="text-emerald-400 pt-1 border-t border-slate-800">🟢 Nurse Shift Logs: 48.2% (Uncritical)</div>
                  <div class="text-emerald-400">🟢 Meal Orders Queue: 410 msgs</div>
                </div>
              </div>
              <div class="space-y-1.5 pt-2 border-t border-slate-800">
                <button type="button" onclick="loadDatasetPreset('healthcare')" class="w-full py-1.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs flex items-center justify-center gap-1.5 shadow transition">
                  <i data-lucide="zap" class="w-3.5 h-3.5"></i> Load LifeCare
                </button>
                <div class="flex items-center gap-1 text-[10px] font-mono">
                  <a href="/api/database/download-preset/healthcare" download="LifeCare_Healthcare_Dataset.json" class="flex-1 py-1 rounded bg-slate-800 hover:bg-slate-700 text-rose-300 text-center transition">⬇ .JSON</a>
                  <a href="/api/database/download-preset-sql/healthcare" download="LifeCare_Healthcare_Schema.sql" class="flex-1 py-1 rounded bg-slate-800 hover:bg-slate-700 text-rose-300 text-center transition">⬇ .SQL</a>
                  <a href="/api/database/download-preset-db/healthcare" download="LifeCare_Healthcare.db" class="flex-1 py-1 rounded bg-slate-800 hover:bg-slate-700 text-rose-300 text-center transition">⬇ .DB</a>
                </div>
              </div>
            </div>

            <!-- Card 3: GlobalPay Fintech -->
            <div class="p-3 rounded-xl bg-[#070b14] border border-sky-500/30 hover:border-sky-400 transition flex flex-col justify-between space-y-2.5 shadow-lg">
              <div>
                <div class="flex items-center justify-between mb-1.5">
                  <span class="font-bold text-sky-300 text-xs flex items-center gap-1.5">
                    🏦 GlobalPay Fintech
                  </span>
                  <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-sky-500/20 text-sky-300">26 Runbooks</span>
                </div>
                <div class="text-[10px] text-slate-400 mb-2">High-Frequency Ledger & Wire Payments</div>
                <div class="space-y-1 text-[10px] font-mono">
                  <div class="text-rose-400">🔴 Ledger: 96.8% ($4.2M/min risk)</div>
                  <div class="text-rose-400">🔴 Recon: 8,400 Trans Locked</div>
                  <div class="text-rose-400">🔴 Fraud Stream: 148,000 msgs (92% Err)</div>
                  <div class="text-rose-400">🔴 Payment SSL: 2 Hours Left</div>
                  <div class="text-emerald-400 pt-1 border-t border-slate-800">🟢 Docker Build Scratch: 54.2% (Uncrit)</div>
                  <div class="text-emerald-400">🟢 Clickstream Queue: 850 msgs</div>
                </div>
              </div>
              <div class="space-y-1.5 pt-2 border-t border-slate-800">
                <button type="button" onclick="loadDatasetPreset('fintech')" class="w-full py-1.5 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs flex items-center justify-center gap-1.5 shadow transition">
                  <i data-lucide="zap" class="w-3.5 h-3.5"></i> Load GlobalPay
                </button>
                <div class="flex items-center gap-1 text-[10px] font-mono">
                  <a href="/api/database/download-preset/fintech" download="GlobalPay_Fintech_Dataset.json" class="flex-1 py-1 rounded bg-slate-800 hover:bg-slate-700 text-sky-300 text-center transition">⬇ .JSON</a>
                  <a href="/api/database/download-preset-sql/fintech" download="GlobalPay_Fintech_Schema.sql" class="flex-1 py-1 rounded bg-slate-800 hover:bg-slate-700 text-sky-300 text-center transition">⬇ .SQL</a>
                  <a href="/api/database/download-preset-db/fintech" download="GlobalPay_Fintech.db" class="flex-1 py-1 rounded bg-slate-800 hover:bg-slate-700 text-sky-300 text-center transition">⬇ .DB</a>
                </div>
              </div>
            </div>

          </div>
        </div>

        <!-- Tab Option 2: File Upload (.db, .sqlite, .json, .csv) -->
        <div class="bg-[#0b101d] border border-cyber-border rounded-xl p-4 space-y-3">
          <label class="block text-slate-200 font-bold text-xs flex items-center gap-1.5">
            <i data-lucide="file-up" class="w-4 h-4 text-emerald-400"></i>
            Option B: Upload Custom Database File from Your Computer
          </label>
          <p class="text-[11px] text-slate-400">
            Upload your own raw SQLite database binary (<code class="text-sky-300">.db</code> / <code class="text-sky-300">.sqlite</code>) or formatted JSON dataset (<code class="text-amber-300">.json</code>):
          </p>

          <div class="flex items-center gap-3">
            <input type="file" id="databaseFileInput" accept=".db,.sqlite,.json,.csv" onchange="handleDatabaseFileSelection(event)" class="block w-full text-xs text-slate-400 file:mr-3 file:py-2 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-emerald-600 file:text-white hover:file:bg-emerald-500 cursor-pointer bg-[#070b14] border border-cyber-border rounded-lg p-1.5" />
          </div>

          <div id="fileSelectionInfo" class="hidden p-2 rounded bg-emerald-950/40 border border-emerald-500/30 text-emerald-300 text-[11px] font-mono flex items-center justify-between">
            <span id="selectedFileName">file.db</span>
            <span id="selectedFileSize">0 KB</span>
          </div>

          <button type="button" onclick="submitUploadedDatabase()" class="w-full py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 transition text-xs font-bold text-white flex items-center justify-center gap-2 shadow-lg shadow-emerald-600/30">
            <i data-lucide="upload" class="w-4 h-4"></i>
            Ingest & Replace Database
          </button>
        </div>
'''

# Replace Tab Option 1 and 2 inside uploadDatabaseModal
idx_modal_opts = html.find('<!-- Tab Option 1: File Upload (.db, .sqlite, .json, .csv) -->')
idx_modal_end = html.find('</div>\n\n      <!-- Modal Footer -->', idx_modal_opts)

if idx_modal_opts != -1 and idx_modal_end != -1:
    html = html[:idx_modal_opts] + new_modal_options + html[idx_modal_end:]

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Updated index.html successfully!")

# =========================================================================
# 2. UPDATE static/js/app.js
# =========================================================================
with open(APP_JS_PATH, "r", encoding="utf-8") as f:
    app_js = f.read()

js_preset_functions = '''
// -------------------------------------------------------------------------
// 13.5. Multi-Dataset Preset Switcher (QuickCart, LifeCare, GlobalPay)
// -------------------------------------------------------------------------
async function loadDatasetPreset(presetName) {
  try {
    const titles = {
      'ecommerce': 'QuickCart E-Commerce & Delivery Cloud',
      'healthcare': 'LifeCare Hospital ICU Patient Cloud',
      'fintech': 'GlobalPay Core Fintech & Banking'
    };
    showToast('Switching Domain Dataset...', `Loading ${titles[presetName] || presetName}...`, 'info');
    const res = await fetch(`/api/database/load-preset/${presetName}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    const data = await res.json();

    if (data.success) {
      showToast('Dataset Activated!', data.message, 'success');
      updateActivePresetUI(presetName);
      closeDatabaseModal();
      await fetchMetrics();
      await fetchIncidents();
      await fetchAuditLogs();
      if (window.confetti) confetti({ particleCount: 100, spread: 85, origin: { y: 0.6 } });
    } else {
      showToast('Preset Error', data.error || 'Failed to load dataset preset.', 'error');
    }
  } catch (err) {
    showToast('Network Error', err.message, 'error');
  }
}

function updateActivePresetUI(presetName) {
  const badge = document.getElementById('activePresetBadge');
  const topBadge = document.getElementById('topActivePresetBadge');
  const titles = {
    'ecommerce': '🛒 QuickCart E-Commerce (98.7% / 3,420 Riders)',
    'healthcare': '🏥 LifeCare Hospital ICU (99.1% / 18 EMS)',
    'fintech': '🏦 GlobalPay Core Fintech (96.8% / $1.4M Recon)'
  };
  const colors = {
    'ecommerce': 'bg-amber-500/20 text-amber-300 border-amber-500/30',
    'healthcare': 'bg-rose-500/20 text-rose-300 border-rose-500/30',
    'fintech': 'bg-sky-500/20 text-sky-300 border-sky-500/30'
  };
  if (badge) {
    badge.textContent = titles[presetName] || presetName;
    badge.className = `text-xs font-mono font-semibold px-2 py-0.5 rounded border ${colors[presetName] || 'bg-sky-500/20 text-sky-300 border-sky-500/30'}`;
  }
  if (topBadge) {
    topBadge.textContent = titles[presetName] || presetName;
    topBadge.className = `hidden md:inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold border ${colors[presetName] || 'bg-sky-500/20 text-sky-300 border-sky-500/30'} font-mono`;
  }
  
  // Highlight active button in switcher
  ['ecommerce', 'healthcare', 'fintech'].forEach(p => {
    const btn = document.getElementById(`btnPreset-${p}`);
    if (btn) {
      if (p === presetName) {
        btn.className = 'px-2.5 py-1.5 rounded-lg border font-mono text-xs transition flex items-center gap-1.5 bg-sky-600 text-white border-sky-400 shadow-md font-bold';
      } else {
        btn.className = 'px-2.5 py-1.5 rounded-lg border border-cyber-border hover:border-slate-500 text-slate-300 hover:text-white transition flex items-center gap-1.5 font-mono text-xs';
      }
    }
  });

  // Dynamically update Section 2 button text based on domain
  updateSection2Buttons(presetName);
}

function updateSection2Buttons(presetName) {
  const diskUnc = document.getElementById('sec2-disk-unc');
  const diskWarn = document.getElementById('sec2-disk-warn');
  const diskCrit = document.getElementById('sec2-disk-crit');

  const workerUnc = document.getElementById('sec2-worker-unc');
  const workerWarn = document.getElementById('sec2-worker-warn');
  const workerCrit = document.getElementById('sec2-worker-crit');

  const queueUnc = document.getElementById('sec2-queue-unc');
  const queueWarn = document.getElementById('sec2-queue-warn');
  const queueCrit = document.getElementById('sec2-queue-crit');

  const sslUnc = document.getElementById('sec2-ssl-unc');
  const sslWarn = document.getElementById('sec2-ssl-warn');
  const sslCrit = document.getElementById('sec2-ssl-crit');

  if (presetName === 'ecommerce') {
    if (diskUnc) diskUnc.innerHTML = '<span class="flex items-center gap-1.5">🟢 Menu Previews (51.4%)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>';
    if (diskWarn) diskWarn.innerHTML = '<span class="flex items-center gap-1.5">🟡 Rider GPS Logs (89.2%)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-sky-500/10 text-sky-400 font-mono">Safe Tier 1</span>';
    if (diskCrit) diskCrit.innerHTML = '<span class="flex items-center gap-1.5">🔴 Invoicing Partition (98.7%)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">450MB Left!</span>';
    
    if (workerUnc) workerUnc.innerHTML = '<span class="flex items-center gap-1.5">🟢 Loyalty Points Worker GC</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>';
    if (workerWarn) workerWarn.innerHTML = '<span class="flex items-center gap-1.5">🟡 SMS/WhatsApp Worker (280s)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-sky-500/10 text-sky-400 font-mono">Safe Tier 1</span>';
    if (workerCrit) workerCrit.innerHTML = '<span class="flex items-center gap-1.5">🔴 Rider Dispatch Lock (3.4k Orders)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">3,420 Waiting!</span>';
    
    if (queueUnc) queueUnc.innerHTML = '<span class="flex items-center gap-1.5">🟢 Clickstream Ripple (620 msgs)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>';
    if (queueWarn) queueWarn.innerHTML = '<span class="flex items-center gap-1.5">🟡 Flash Sale Orders (32.4k msgs)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-400 font-mono">Scale 4➔8</span>';
    if (queueCrit) queueCrit.innerHTML = '<span class="flex items-center gap-1.5">🔴 Rider GPS Crash Loop (184k msgs)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">88.2% Err</span>';

    if (sslUnc) sslUnc.innerHTML = '<span class="flex items-center gap-1.5">🟢 Warehouse mTLS Audit (62d)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>';
    if (sslWarn) sslWarn.innerHTML = '<span class="flex items-center gap-1.5">🟡 App Push Gateway (3.8d)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-sky-500/10 text-sky-400 font-mono">Safe Tier 1</span>';
    if (sslCrit) sslCrit.innerHTML = '<span class="flex items-center gap-1.5">🔴 Kitchen Tablet API (4 Hours!)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">CA Revoked</span>';
  } else if (presetName === 'healthcare') {
    if (diskUnc) diskUnc.innerHTML = '<span class="flex items-center gap-1.5">🟢 Nurse Shift Logs (48.2%)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>';
    if (diskWarn) diskWarn.innerHTML = '<span class="flex items-center gap-1.5">🟡 PACS X-Ray Cache (87.6%)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-sky-500/10 text-sky-400 font-mono">Safe Tier 1</span>';
    if (diskCrit) diskCrit.innerHTML = '<span class="flex items-center gap-1.5">🔴 ICU Cardiac ECG (99.1%)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">180MB Left!</span>';
    
    if (workerUnc) workerUnc.innerHTML = '<span class="flex items-center gap-1.5">🟢 Discharge PDF Worker GC</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>';
    if (workerWarn) workerWarn.innerHTML = '<span class="flex items-center gap-1.5">🟡 Pharmacy Sync Stalled (320s)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-sky-500/10 text-sky-400 font-mono">Safe Tier 1</span>';
    if (workerCrit) workerCrit.innerHTML = '<span class="flex items-center gap-1.5">🔴 Ambulance Dispatch Lock (18 Calls)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">18 911 Calls!</span>';
    
    if (queueUnc) queueUnc.innerHTML = '<span class="flex items-center gap-1.5">🟢 Meal Orders Ripple (410 msgs)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>';
    if (queueWarn) queueWarn.innerHTML = '<span class="flex items-center gap-1.5">🟡 Blood Lab Results (19.8k msgs)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-400 font-mono">Scale 2➔6</span>';
    if (queueCrit) queueCrit.innerHTML = '<span class="flex items-center gap-1.5">🔴 Bedside Vitals Crash (96k msgs)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">94.1% Err</span>';

    if (sslUnc) sslUnc.innerHTML = '<span class="flex items-center gap-1.5">🟢 Medical IoT Gateway Audit (75d)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>';
    if (sslWarn) sslWarn.innerHTML = '<span class="flex items-center gap-1.5">🟡 Patient Records Portal (4.2d)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-sky-500/10 text-sky-400 font-mono">Safe Tier 1</span>';
    if (sslCrit) sslCrit.innerHTML = '<span class="flex items-center gap-1.5">🔴 Telemed Video Gateway (5 Hours!)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">CA Revoked</span>';
  } else {
    if (diskUnc) diskUnc.innerHTML = '<span class="flex items-center gap-1.5">🟢 Dev Build Scratch (54.2%)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>';
    if (diskWarn) diskWarn.innerHTML = '<span class="flex items-center gap-1.5">🟡 Nginx Static Cache (88.5%)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-sky-500/10 text-sky-400 font-mono">Safe Tier 1</span>';
    if (diskCrit) diskCrit.innerHTML = '<span class="flex items-center gap-1.5">🔴 Postgres WAL Full (99.4%)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">124MB Left!</span>';
    
    if (workerUnc) workerUnc.innerHTML = '<span class="flex items-center gap-1.5">🟢 Image Worker GC (15k Tasks)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>';
    if (workerWarn) workerWarn.innerHTML = '<span class="flex items-center gap-1.5">🟡 Email Worker Hung (310s)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-sky-500/10 text-sky-400 font-mono">Safe Tier 1</span>';
    if (workerCrit) workerCrit.innerHTML = '<span class="flex items-center gap-1.5">🔴 Payment Recon Lock (8.4k Trans)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">$1.42M Risk</span>';
    
    if (queueUnc) queueUnc.innerHTML = '<span class="flex items-center gap-1.5">🟢 Clickstream Ripple (850 msgs)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>';
    if (queueWarn) queueWarn.innerHTML = '<span class="flex items-center gap-1.5">🟡 Flash Sale Surge (28.5k msgs)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-400 font-mono">Scale 4➔8</span>';
    if (queueCrit) queueCrit.innerHTML = '<span class="flex items-center gap-1.5">🔴 Fraud Detection Crash (148k msgs)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">92.4% Err</span>';

    if (sslUnc) sslUnc.innerHTML = '<span class="flex items-center gap-1.5">🟢 Microservice mTLS Audit (58d)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>';
    if (sslWarn) sslWarn.innerHTML = '<span class="flex items-center gap-1.5">🟡 Customer Web Portal (4.5d)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-sky-500/10 text-sky-400 font-mono">Safe Tier 1</span>';
    if (sslCrit) sslCrit.innerHTML = '<span class="flex items-center gap-1.5">🔴 Edge API Gateway TLS (6.2h)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">CA Revoked</span>';
  }
  if (window.lucide) lucide.createIcons();
}
'''

if 'async function loadDatasetPreset' not in app_js:
    # Append before last section
    idx_insert = app_js.find('// 14. Interactive Problem Solver')
    if idx_insert != -1:
        app_js = app_js[:idx_insert] + js_preset_functions + "\n\n" + app_js[idx_insert:]
    else:
        app_js += "\n\n" + js_preset_functions

with open(APP_JS_PATH, "w", encoding="utf-8") as f:
    f.write(app_js)

print("Updated app.js successfully!")

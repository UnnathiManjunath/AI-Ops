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

# 1.1 Add "View Table" button in top nav bar
table_nav_btn = '''        <!-- View Dataset as Table Modal Button -->
        <button onclick="openTableModal('it_sector')" class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-teal-950/50 border border-teal-500/50 hover:bg-teal-900/60 transition text-xs font-semibold text-teal-300 shadow-lg" title="Open Interactive Table Viewer (Rows & Columns)">
          <i data-lucide="table" class="w-4 h-4 text-teal-400"></i>
          <span>View Table</span>
        </button>
'''

if 'onclick="openTableModal' not in html:
    html = html.replace('<!-- Upload / Import Database Button -->', table_nav_btn + '\n        <!-- Upload / Import Database Button -->')

# 1.2 Add CSV download links to all 4 cards in uploadDatabaseModal
# In card 0 (IT sector)
if '/api/database/download-preset-csv/it_sector' not in html:
    html = html.replace(
        '<a href="/api/database/download-preset-db/it_sector" download="DevOpsCorp_ITSector.db" class="flex-1 py-1 rounded bg-slate-800 hover:bg-slate-700 text-emerald-300 text-center transition">⬇ .DB</a>',
        '<a href="/api/database/download-preset-db/it_sector" download="DevOpsCorp_ITSector.db" class="flex-1 py-1 rounded bg-slate-800 hover:bg-slate-700 text-emerald-300 text-center transition">⬇ .DB</a>\n                  <a href="/api/database/download-preset-csv/it_sector" download="DevOpsCorp_ITSector_Table.csv" class="flex-1 py-1 rounded bg-teal-900/60 hover:bg-teal-800 text-teal-300 text-center font-bold transition" title="Download as CSV Table for Excel">⬇ .CSV</a>'
    )
    html = html.replace(
        '<a href="/api/database/download-preset-db/ecommerce" download="QuickCart_ECommerce.db" class="flex-1 py-1 rounded bg-slate-800 hover:bg-slate-700 text-amber-300 text-center transition">⬇ .DB</a>',
        '<a href="/api/database/download-preset-db/ecommerce" download="QuickCart_ECommerce.db" class="flex-1 py-1 rounded bg-slate-800 hover:bg-slate-700 text-amber-300 text-center transition">⬇ .DB</a>\n                  <a href="/api/database/download-preset-csv/ecommerce" download="QuickCart_ECommerce_Table.csv" class="flex-1 py-1 rounded bg-teal-900/60 hover:bg-teal-800 text-teal-300 text-center font-bold transition" title="Download as CSV Table for Excel">⬇ .CSV</a>'
    )
    html = html.replace(
        '<a href="/api/database/download-preset-db/healthcare" download="LifeCare_Healthcare.db" class="flex-1 py-1 rounded bg-slate-800 hover:bg-slate-700 text-rose-300 text-center transition">⬇ .DB</a>',
        '<a href="/api/database/download-preset-db/healthcare" download="LifeCare_Healthcare.db" class="flex-1 py-1 rounded bg-slate-800 hover:bg-slate-700 text-rose-300 text-center transition">⬇ .DB</a>\n                  <a href="/api/database/download-preset-csv/healthcare" download="LifeCare_Healthcare_Table.csv" class="flex-1 py-1 rounded bg-teal-900/60 hover:bg-teal-800 text-teal-300 text-center font-bold transition" title="Download as CSV Table for Excel">⬇ .CSV</a>'
    )
    html = html.replace(
        '<a href="/api/database/download-preset-db/fintech" download="GlobalPay_Fintech.db" class="flex-1 py-1 rounded bg-slate-800 hover:bg-slate-700 text-sky-300 text-center transition">⬇ .DB</a>',
        '<a href="/api/database/download-preset-db/fintech" download="GlobalPay_Fintech.db" class="flex-1 py-1 rounded bg-slate-800 hover:bg-slate-700 text-sky-300 text-center transition">⬇ .DB</a>\n                  <a href="/api/database/download-preset-csv/fintech" download="GlobalPay_Fintech_Table.csv" class="flex-1 py-1 rounded bg-teal-900/60 hover:bg-teal-800 text-teal-300 text-center font-bold transition" title="Download as CSV Table for Excel">⬇ .CSV</a>'
    )

# 1.3 Add Interactive Dataset Table Viewer Modal (id="datasetTableModal")
table_modal_html = '''
  <!-- MODAL 4: Interactive Dataset Table Viewer (Rows & Columns for Judges) -->
  <div id="datasetTableModal" class="hidden fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-3 lg:p-6">
    <div class="bg-cyber-card border border-cyber-border rounded-2xl max-w-7xl w-full p-6 shadow-2xl relative max-h-[94vh] flex flex-col">
      
      <button onclick="closeTableModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white transition p-1 rounded-lg bg-slate-800/60">
        <i data-lucide="x" class="w-5 h-5"></i>
      </button>

      <!-- Modal Header -->
      <div class="flex flex-wrap items-center justify-between gap-4 mb-4 pb-3 border-b border-cyber-border">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-xl bg-teal-500/20 border border-teal-500/30 flex items-center justify-center shadow-lg shadow-teal-500/20">
            <i data-lucide="table" class="w-5 h-5 text-teal-400"></i>
          </div>
          <div>
            <h3 class="text-lg font-bold text-white flex items-center gap-2">
              Operational Dataset Table Viewer
              <span id="tableRowsBadge" class="text-[10px] font-mono px-2 py-0.5 rounded bg-teal-500/20 text-teal-300 border border-teal-500/30">12 Rows • 13 Columns</span>
            </h3>
            <p class="text-xs text-slate-400">Structured tabular view of SRE Runbooks, Trigger Rules, Blast Radius & Governance</p>
          </div>
        </div>

        <!-- 1-Click Export CSV / Excel Button -->
        <div class="flex items-center gap-2">
          <a id="btnTableDownloadCsv" href="/api/database/download-preset-csv/it_sector" download class="px-3.5 py-1.5 rounded-lg bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs flex items-center gap-1.5 shadow-lg shadow-teal-600/30 transition">
            <i data-lucide="download" class="w-4 h-4"></i>
            <span>Export Table to CSV (Excel)</span>
          </a>
        </div>
      </div>

      <!-- Sector Selector Bar & Search Input -->
      <div class="flex flex-wrap items-center justify-between gap-3 mb-3 p-2.5 rounded-xl bg-[#070b14] border border-cyber-border">
        <!-- Sector Tabs -->
        <div class="flex items-center flex-wrap gap-1.5 font-mono text-xs">
          <button id="tableTab-it_sector" onclick="loadTableData('it_sector')" class="px-2.5 py-1 rounded-lg bg-teal-600 text-white font-bold border border-teal-400 shadow transition flex items-center gap-1">
            💻 IT Sector (12)
          </button>
          <button id="tableTab-ecommerce" onclick="loadTableData('ecommerce')" class="px-2.5 py-1 rounded-lg border border-cyber-border text-slate-300 hover:text-white transition flex items-center gap-1">
            🛒 E-Commerce (12)
          </button>
          <button id="tableTab-healthcare" onclick="loadTableData('healthcare')" class="px-2.5 py-1 rounded-lg border border-cyber-border text-slate-300 hover:text-white transition flex items-center gap-1">
            🏥 Healthcare (12)
          </button>
          <button id="tableTab-fintech" onclick="loadTableData('fintech')" class="px-2.5 py-1 rounded-lg border border-cyber-border text-slate-300 hover:text-white transition flex items-center gap-1">
            🏦 Fintech (26)
          </button>
          <button id="tableTab-master" onclick="loadTableData('master')" class="px-2.5 py-1 rounded-lg border border-cyber-border text-slate-300 hover:text-white transition flex items-center gap-1 font-bold text-sky-400">
            🌐 All Sectors (62 Rows)
          </button>
          <button id="tableTab-metrics" onclick="loadTableData('metrics')" class="px-2.5 py-1 rounded-lg border border-cyber-border text-slate-300 hover:text-white transition flex items-center gap-1 text-amber-300">
            📈 Metrics (24)
          </button>
        </div>

        <!-- Filter / Search Input -->
        <div class="relative w-full sm:w-64">
          <i data-lucide="search" class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5"></i>
          <input type="text" id="tableSearchInput" oninput="filterTableRows()" placeholder="Search rows or keywords..." class="w-full bg-[#0b101c] border border-cyber-border rounded-lg pl-8 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-teal-500 font-mono" />
        </div>
      </div>

      <!-- Scrollable Table Container -->
      <div class="flex-1 overflow-x-auto overflow-y-auto border border-cyber-border rounded-xl bg-[#070b14] shadow-inner text-xs">
        <table id="interactiveDataTable" class="w-full text-left border-collapse">
          <thead id="interactiveTableHead" class="sticky top-0 bg-[#0d1424] text-slate-300 border-b border-cyber-border z-10 font-mono text-[11px] uppercase tracking-wider">
            <!-- Headers inserted dynamically -->
          </thead>
          <tbody id="interactiveTableBody" class="divide-y divide-slate-800/60 font-sans text-xs">
            <!-- Rows inserted dynamically -->
          </tbody>
        </table>
      </div>

      <!-- Modal Footer -->
      <div class="flex items-center justify-between pt-3 mt-3 border-t border-cyber-border text-xs text-slate-400">
        <span id="tableShowingCount">Showing 12 of 12 rows</span>
        <button onclick="closeTableModal()" class="px-4 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 transition">
          Close
        </button>
      </div>

    </div>
  </div>
'''

if 'id="datasetTableModal"' not in html:
    # Insert right before </body>
    html = html.replace('</body>', table_modal_html + '\n</body>')

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Updated index.html with Interactive Table Viewer Modal!")

# =========================================================================
# 2. UPDATE static/js/app.js
# =========================================================================
with open(APP_JS_PATH, "r", encoding="utf-8") as f:
    app_js = f.read()

js_table_logic = '''
// -------------------------------------------------------------------------
// 15. Interactive Dataset Table Viewer (Rows & Columns for Judges)
// -------------------------------------------------------------------------
let currentTableData = { columns: [], rows: [] };
let currentTablePreset = 'it_sector';

function openTableModal(presetName = 'it_sector') {
  const modal = document.getElementById('datasetTableModal');
  if (modal) {
    modal.classList.remove('hidden');
    loadTableData(presetName);
  }
}

function closeTableModal() {
  const modal = document.getElementById('datasetTableModal');
  if (modal) modal.classList.add('hidden');
}

async function loadTableData(presetName) {
  currentTablePreset = presetName;
  const thead = document.getElementById('interactiveTableHead');
  const tbody = document.getElementById('interactiveTableBody');
  const badge = document.getElementById('tableRowsBadge');
  const dlBtn = document.getElementById('btnTableDownloadCsv');

  // Highlight tab
  ['it_sector', 'ecommerce', 'healthcare', 'fintech', 'master', 'metrics'].forEach(p => {
    const tab = document.getElementById(`tableTab-${p}`);
    if (tab) {
      if (p === presetName) {
        tab.className = 'px-2.5 py-1 rounded-lg bg-teal-600 text-white font-bold border border-teal-400 shadow transition flex items-center gap-1';
      } else {
        tab.className = 'px-2.5 py-1 rounded-lg border border-cyber-border text-slate-300 hover:text-white transition flex items-center gap-1';
      }
    }
  });

  // Update download link
  if (dlBtn) {
    dlBtn.href = `/api/database/download-preset-csv/${presetName}`;
    dlBtn.download = `SafeOps_${presetName.toUpperCase()}_Table.csv`;
  }

  if (tbody) {
    tbody.innerHTML = '<tr><td colspan="10" class="p-8 text-center text-slate-400 font-mono animate-pulse"><i data-lucide="loader" class="w-5 h-5 mx-auto mb-2 animate-spin text-teal-400"></i>Loading table rows and columns...</td></tr>';
    if (window.lucide) lucide.createIcons();
  }

  try {
    const res = await fetch(`/api/database/table-data/${presetName}`);
    const data = await res.json();

    if (!data.success) {
      if (tbody) tbody.innerHTML = `<tr><td colspan="10" class="p-6 text-center text-rose-400 font-mono">${data.error}</td></tr>`;
      return;
    }

    currentTableData = data;
    renderTable(data.columns, data.rows);

    if (badge) {
      badge.textContent = `${data.total_rows} Rows • ${data.columns.length} Columns`;
    }

  } catch (err) {
    if (tbody) tbody.innerHTML = `<tr><td colspan="10" class="p-6 text-center text-rose-400 font-mono">${err.message}</td></tr>`;
  }
}

function renderTable(columns, rows) {
  const thead = document.getElementById('interactiveTableHead');
  const tbody = document.getElementById('interactiveTableBody');
  const showingCount = document.getElementById('tableShowingCount');

  if (!thead || !tbody) return;

  // Render headers
  let thHtml = '<tr>';
  columns.forEach(col => {
    const label = col.replace(/_/g, ' ');
    thHtml += `<th class="p-3 whitespace-nowrap border-r border-slate-800/60 font-semibold">${label}</th>`;
  });
  thHtml += '</tr>';
  thead.innerHTML = thHtml;

  // Render rows
  if (rows.length === 0) {
    tbody.innerHTML = '<tr><td colspan="15" class="p-6 text-center text-slate-500 font-mono">No matching records found.</td></tr>';
    if (showingCount) showingCount.textContent = 'Showing 0 rows';
    return;
  }

  let trHtml = '';
  rows.forEach((row, idx) => {
    const isAlt = idx % 2 === 1 ? 'bg-[#090e1b]' : 'bg-[#070b14]';
    trHtml += `<tr class="${isAlt} hover:bg-slate-800/50 transition">`;
    
    columns.forEach(col => {
      let val = row[col] || '';
      let cellContent = val;

      // Badges for severity
      if (col === 'Severity') {
        if (val.includes('CRITICAL')) {
          cellContent = `<span class="px-2 py-0.5 rounded font-mono text-[10px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">🔴 ${val}</span>`;
        } else if (val.includes('WARNING')) {
          cellContent = `<span class="px-2 py-0.5 rounded font-mono text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">🟡 ${val}</span>`;
        } else if (val.includes('UNCRITICAL')) {
          cellContent = `<span class="px-2 py-0.5 rounded font-mono text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">🟢 ${val}</span>`;
        }
      } else if (col === 'Requires_Human_Approval') {
        if (val.includes('YES')) {
          cellContent = `<span class="px-2 py-0.5 rounded font-mono text-[10px] font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30">🔒 ${val}</span>`;
        } else {
          cellContent = `<span class="px-2 py-0.5 rounded font-mono text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">⚡ Auto</span>`;
        }
      } else if (col.includes('Command')) {
        cellContent = `<code class="text-[10px] font-mono text-cyan-300 bg-slate-900 px-1.5 py-0.5 rounded max-w-xs truncate block" title="${val}">${val}</code>`;
      } else if (col === 'Runbook_ID' || col === 'Metric_Key') {
        cellContent = `<span class="font-mono text-xs font-bold text-sky-400">${val}</span>`;
      }

      trHtml += `<td class="p-3 border-r border-slate-800/40 whitespace-nowrap text-slate-300">${cellContent}</td>`;
    });
    trHtml += '</tr>';
  });

  tbody.innerHTML = trHtml;
  if (showingCount) showingCount.textContent = `Showing ${rows.length} of ${currentTableData.total_rows} rows`;
  if (window.lucide) lucide.createIcons();
}

function filterTableRows() {
  const query = (document.getElementById('tableSearchInput')?.value || '').toLowerCase().trim();
  if (!query) {
    renderTable(currentTableData.columns, currentTableData.rows);
    return;
  }
  const filtered = currentTableData.rows.filter(row => {
    return Object.values(row).some(v => String(v).toLowerCase().includes(query));
  });
  renderTable(currentTableData.columns, filtered);
}
'''

if 'function openTableModal' not in app_js:
    app_js += '\n\n' + js_table_logic
    with open(APP_JS_PATH, "w", encoding="utf-8") as f:
        f.write(app_js)
    print("Updated app.js with Interactive Table Viewer logic!")

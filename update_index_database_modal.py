import os

INDEX_PATH = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\templates\index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update Top Bar Navigation
old_top_bar_marker_start = '<!-- Upload Runbook Button -->'
old_top_bar_marker_end = '<!-- Reset Demo -->'

p_top_start = text.find(old_top_bar_marker_start)
p_top_end = text.find(old_top_bar_marker_end)

new_top_bar_buttons = """<!-- Upload / Import Database Button -->
        <button onclick="openDatabaseModal()" class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-emerald-950/50 border border-emerald-500/50 hover:bg-emerald-900/60 transition text-xs font-semibold text-emerald-300 shadow-lg shadow-emerald-950/50" title="Upload or Import SRE Database (.db, .sqlite, .json, .csv)">
          <i data-lucide="database" class="w-4 h-4 text-emerald-400"></i>
          <span>Upload Database</span>
        </button>

        <!-- Download Active Database .DB -->
        <a href="/api/database/export" download="safeops_master.db" class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-cyan-950/50 border border-cyan-500/50 hover:bg-cyan-900/60 transition text-xs font-semibold text-cyan-300" title="Download Active SQLite Database (.db)">
          <i data-lucide="hard-drive" class="w-4 h-4 text-cyan-400"></i>
          <span>Download .DB</span>
        </a>

        <!-- Download Runbook Button -->
        <a href="/api/download/runbook" download class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-sky-950/40 border border-sky-500/40 hover:bg-sky-900/50 transition text-xs font-semibold text-sky-300" title="Download Master Operational Runbook Markdown">
          <i data-lucide="download" class="w-4 h-4 text-sky-400"></i>
          <span>Download Runbook</span>
        </a>

        <!-- Download Project ZIP Button -->
        <a href="/api/download/project-zip" download class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-indigo-950/40 border border-indigo-500/40 hover:bg-indigo-900/50 transition text-xs font-semibold text-indigo-300" title="Download complete project ZIP for submission">
          <i data-lucide="folder-archive" class="w-4 h-4 text-indigo-400"></i>
          <span>Download .ZIP</span>
        </a>

        """

if p_top_start != -1 and p_top_end != -1:
    text = text[:p_top_start] + new_top_bar_buttons + text[p_top_end:]
    print("Top bar buttons updated successfully!")
else:
    print(f"Top bar markers not found: p_top_start={p_top_start}, p_top_end={p_top_end}")

# 2. Update Modals: Replace uploadRunbookModal with uploadDatabaseModal and remove duplicate
modal_marker_start = '<!-- MODAL 3: Upload & Ingest Runbook Modal -->'
p_m_start = text.find(modal_marker_start)
p_runbooks_modal = text.find('<!-- MODAL 2: 10 Representative Runbooks Library Browser -->')

new_database_modal = """<!-- MODAL 3: Upload & Import Operational Database (Critical & Uncritical Dataset) -->
  <div id="uploadDatabaseModal" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-cyber-card border border-cyber-border rounded-2xl max-w-3xl w-full p-6 shadow-2xl relative max-h-[92vh] flex flex-col">
      
      <button onclick="closeDatabaseModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white transition">
        <i data-lucide="x" class="w-5 h-5"></i>
      </button>

      <!-- Modal Header -->
      <div class="flex items-center space-x-3 mb-4 pb-3 border-b border-cyber-border">
        <div class="w-10 h-10 rounded-xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center shadow-lg shadow-emerald-500/20">
          <i data-lucide="database" class="w-5 h-5 text-emerald-400"></i>
        </div>
        <div>
          <h3 class="text-lg font-bold text-white flex items-center gap-2">
            Upload & Ingest Operational Database
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">SQLite / JSON / CSV</span>
          </h3>
          <p class="text-xs text-slate-400">Upload or import datasets covering Critical & Uncritical situations across all 4 problem areas</p>
        </div>
      </div>

      <!-- Scrollable Modal Body -->
      <div class="space-y-4 flex-1 overflow-y-auto pr-1 text-xs">

        <!-- 4 Problems Scope Preview Box -->
        <div class="bg-[#070b14] border border-cyber-border rounded-xl p-3.5 space-y-2.5">
          <div class="flex items-center justify-between">
            <span class="font-bold text-slate-200 text-xs flex items-center gap-1.5">
              <i data-lucide="layers" class="w-4 h-4 text-sky-400"></i>
              Dataset Coverage (Both Critical & Uncritical Situations Included):
            </span>
            <span class="text-[10px] font-mono text-emerald-400 font-bold">18 SRE Runbooks Ready</span>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-[11px]">
            <div class="p-2 rounded bg-[#0b101d] border border-cyber-border">
              <span class="font-bold text-sky-400 block mb-0.5">💾 1. Disk Storage Dataset:</span>
              <div class="text-slate-300">🔴 Critical: MySQL Crash Core Dumps (96.8%)</div>
              <div class="text-emerald-400 font-semibold">🟢 Uncritical: Routine /tmp & Logs Hygiene (62.4%)</div>
            </div>
            <div class="p-2 rounded bg-[#0b101d] border border-cyber-border">
              <span class="font-bold text-purple-400 block mb-0.5">⚡ 2. Worker Threads Dataset:</span>
              <div class="text-slate-300">🔴 Critical: PostgreSQL Connection Saturation (99%)</div>
              <div class="text-emerald-400 font-semibold">🟢 Uncritical: Routine Heap Memory Trim & Idle Recycle</div>
            </div>
            <div class="p-2 rounded bg-[#0b101d] border border-cyber-border">
              <span class="font-bold text-amber-400 block mb-0.5">📦 3. Message Queue Dataset:</span>
              <div class="text-slate-300">🔴 Critical: Poison Pill Kafka Crash Loop (68.4% Err)</div>
              <div class="text-emerald-400 font-semibold">🟢 Uncritical: Off-Peak Backlog Ripple Balancing (420 msgs)</div>
            </div>
            <div class="p-2 rounded bg-[#0b101d] border border-cyber-border">
              <span class="font-bold text-emerald-400 block mb-0.5">🔒 4. SSL Security Dataset:</span>
              <div class="text-slate-300">🔴 Critical: Root CA Trust Chain Revocation (1.2d)</div>
              <div class="text-emerald-400 font-semibold">🟢 Uncritical: 45-Day Routine Cryptographic Health Audit</div>
            </div>
          </div>
        </div>

        <!-- Tab Option 1: File Upload (.db, .sqlite, .json, .csv) -->
        <div class="bg-[#0b101d] border border-cyber-border rounded-xl p-4 space-y-3">
          <label class="block text-slate-200 font-bold text-xs flex items-center gap-1.5">
            <i data-lucide="file-up" class="w-4 h-4 text-emerald-400"></i>
            Option A: Upload Database File from Your Computer
          </label>
          <p class="text-[11px] text-slate-400">
            Select a raw SQLite database binary (<code class="text-sky-300">.db</code> / <code class="text-sky-300">.sqlite</code>) or a structured JSON dataset (<code class="text-amber-300">.json</code>):
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

        <!-- Tab Option 2: 1-Click Load Master SRE Dataset -->
        <div class="bg-[#0b101d] border border-cyber-border rounded-xl p-4 space-y-2.5">
          <div class="flex items-center justify-between">
            <label class="block text-slate-200 font-bold text-xs flex items-center gap-1.5">
              <i data-lucide="sparkles" class="w-4 h-4 text-sky-400"></i>
              Option B: 1-Click Load Pre-Packaged Master Database
            </label>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-sky-950 text-sky-300 border border-sky-800">safeops_master.db</span>
          </div>
          <p class="text-[11px] text-slate-400">
            Instantly restores all 18 representative SRE runbooks, safety guardrails, and both Critical & Uncritical situations with zero file upload needed.
          </p>
          <button type="button" onclick="loadPrepackagedMasterDatabase()" class="w-full py-2 rounded-lg bg-sky-600 hover:bg-sky-500 transition text-xs font-bold text-white flex items-center justify-center gap-2 shadow-lg shadow-sky-600/30">
            <i data-lucide="rotate-ccw" class="w-4 h-4"></i>
            1-Click Restore Master Database (Critical + Uncritical)
          </button>
        </div>

        <!-- Tab Option 3: Download & Export Active Database -->
        <div class="bg-[#0b101d] border border-cyber-border rounded-xl p-4 space-y-2.5">
          <label class="block text-slate-200 font-bold text-xs flex items-center gap-1.5">
            <i data-lucide="download" class="w-4 h-4 text-cyan-400"></i>
            Option C: Download Active Database & Datasets
          </label>
          <p class="text-[11px] text-slate-400">
            Export the live database in binary or text formats to share with your teammates or judges:
          </p>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-2">
            <a href="/api/database/export" download="safeops_master.db" class="p-2 rounded bg-[#070b14] border border-cyan-500/40 hover:bg-cyan-950/40 transition text-center block">
              <span class="font-bold text-cyan-400 block text-xs">💾 Download .DB</span>
              <span class="text-[10px] text-slate-400 font-mono">SQLite Binary</span>
            </a>
            <a href="/api/database/export-json" download="MASTER_DATABASE_DATASET.json" class="p-2 rounded bg-[#070b14] border border-amber-500/40 hover:bg-amber-950/40 transition text-center block">
              <span class="font-bold text-amber-400 block text-xs">📄 Download .JSON</span>
              <span class="text-[10px] text-slate-400 font-mono">Structured Dataset</span>
            </a>
            <a href="/api/export-audit?format=csv" download="ITIL_Audit_Trail.csv" class="p-2 rounded bg-[#070b14] border border-emerald-500/40 hover:bg-emerald-950/40 transition text-center block">
              <span class="font-bold text-emerald-400 block text-xs">📊 Export Audit .CSV</span>
              <span class="text-[10px] text-slate-400 font-mono">ITIL Change Trail</span>
            </a>
          </div>
        </div>

      </div>

      <!-- Modal Footer -->
      <div class="mt-4 pt-3 border-t border-cyber-border flex items-center justify-between">
        <span class="text-[11px] text-slate-400 flex items-center gap-1.5">
          <i data-lucide="shield-check" class="w-3.5 h-3.5 text-emerald-400"></i>
          ACID-compliant SQLite relational storage engine
        </span>
        <button onclick="closeDatabaseModal()" class="px-4 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 transition text-xs font-semibold text-slate-300">
          Close Window
        </button>
      </div>

    </div>
  </div>

  """

if p_m_start != -1 and p_runbooks_modal != -1:
    text = text[:p_m_start] + new_database_modal + text[p_runbooks_modal:]
    print("Database modal inserted cleanly!")
else:
    print(f"Modal marker not found: p_m_start={p_m_start}, p_runbooks_modal={p_runbooks_modal}")

# 3. Clean up any duplicate modal at the end before </body>
p_dup = text.find('<!-- MODAL 3: Upload & Ingest Runbook Modal -->')
if p_dup != -1:
    p_body = text.find('<!-- Notification Toast Container -->')
    if p_body != -1 and p_dup < p_body:
        text = text[:p_dup] + text[p_body:]
        print("Duplicate modal removed cleanly!")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("index.html completely updated!")

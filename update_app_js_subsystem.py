import re

js_path = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\static\js\app.js"

with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

new_js_logic = '''// -------------------------------------------------------------------------
// 12. Visual Subsystem Inspector & Multi-Layer OS Architecture
// -------------------------------------------------------------------------
let currentSubsystemTab = 'disk';

function switchSubsystemTab(tabKey) {
  currentSubsystemTab = tabKey;
  
  const tabs = ['disk', 'worker', 'queue', 'ssl', 'arch'];
  tabs.forEach(t => {
    const btn = document.getElementById(`tab-subsystem-${t}`);
    if (btn) {
      if (t === tabKey) {
        btn.className = 'px-2.5 py-1 rounded text-xs font-semibold bg-sky-600 text-white transition flex items-center gap-1.5 shadow';
      } else {
        btn.className = 'px-2.5 py-1 rounded text-xs font-semibold text-slate-400 hover:text-white transition flex items-center gap-1.5';
      }
    }
  });

  if (tabKey === 'disk') {
    loadRealFilesystem();
  } else if (tabKey === 'worker') {
    fetchSubsystemState('worker_stuck');
  } else if (tabKey === 'queue') {
    fetchSubsystemState('queue_growth');
  } else if (tabKey === 'ssl') {
    fetchSubsystemState('ssl_expiry');
  } else if (tabKey === 'arch') {
    renderArchitectureMatrix();
  }
}

async function loadRealFilesystem() {
  const list = document.getElementById('subsystemContentList');
  const msg = document.getElementById('subsystemMessage');
  const badge = document.getElementById('subsystemBadge');
  if (!list) return;

  if (badge) {
    badge.textContent = 'HARD DISK VFS: /dev/sda1';
    badge.className = 'text-[10px] font-mono px-2 py-0.5 rounded bg-sky-950/60 text-sky-300 border border-sky-500/40';
  }

  list.innerHTML = `<div class="text-center py-4 text-slate-500 text-xs font-mono">// Probing local physical files in var_log_app...</div>`;

  try {
    const res = await fetch('/api/filesystem/inventory');
    const data = await res.json();

    if (msg) {
      msg.innerHTML = `
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 w-full">
          <div>
            <span class="font-bold text-white">Physical Storage Path:</span>
            <span class="text-sky-300 font-mono">${data.base_path}</span>
          </div>
          <span class="text-[11px] text-emerald-400 font-mono">Real-Time Host Filesystem Active</span>
        </div>
      `;
    }

    let html = `
      <!-- Live Windows Explorer & Compression Control Toolbar -->
      <div class="p-2.5 rounded-lg bg-[#070b14] border border-cyber-border mb-2.5 flex flex-wrap items-center justify-between gap-2">
        <div class="flex flex-wrap items-center gap-2">
          <button onclick="openArchiveFolder()" class="px-3 py-1.5 rounded bg-emerald-600 hover:bg-emerald-500 text-white font-mono text-xs font-bold transition flex items-center gap-1.5 shadow">
            <i data-lucide="folder-open" class="w-3.5 h-3.5"></i>
            📂 Open .GZ Archive in Windows Explorer
          </button>
          <button onclick="openRawFolder()" class="px-2.5 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 font-mono text-xs transition flex items-center gap-1.5">
            <i data-lucide="folder" class="w-3.5 h-3.5"></i>
            Open Raw Logs Folder
          </button>
        </div>
        <div class="flex flex-wrap items-center gap-2">
          <button onclick="executeRealZip()" class="px-2.5 py-1.5 rounded bg-sky-600/30 hover:bg-sky-600/50 text-sky-300 border border-sky-500/40 font-mono text-xs transition flex items-center gap-1.5">
            <i data-lucide="archive" class="w-3.5 h-3.5"></i>
            ⚡ Run Real Gzip on Disk Now
          </button>
          <button onclick="executeRealRollback()" class="px-2.5 py-1.5 rounded bg-rose-600/30 hover:bg-rose-600/50 text-rose-300 border border-rose-500/40 font-mono text-xs transition flex items-center gap-1.5">
            <i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i>
            ↩️ Rollback (Gunzip)
          </button>
        </div>
      </div>

      <!-- The 5 Strict SRE Compression Criteria (Judge Compliance Panel) -->
      <div class="mb-2.5 p-2.5 rounded-lg bg-[#0c1222] border border-sky-500/30 text-xs">
        <div class="flex items-center justify-between mb-2">
          <span class="font-bold text-sky-400 font-mono flex items-center gap-1.5">
            <i data-lucide="check-check" class="w-4 h-4 text-sky-400"></i>
            5 Strict SRE Compression Eligibility Criteria (Why Not All Files Can Be Zipped)
          </span>
          <span class="text-[10px] text-slate-400 font-mono">ITIL Safety Guardrails</span>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-5 gap-2 text-[11px] font-mono">
          <div class="p-1.5 rounded bg-[#070b14] border border-cyber-border">
            <div class="text-sky-300 font-bold">1. Entropy & Format</div>
            <div class="text-slate-400 text-[10px]">Plaintext logs only. Reject .gz/.png/.mp4 (Entropy > 0.98 saves 0 MB).</div>
          </div>
          <div class="p-1.5 rounded bg-[#070b14] border border-cyber-border">
            <div class="text-sky-300 font-bold">2. Age > 48 Hours</div>
            <div class="text-slate-400 text-[10px]">Rotated logs only (.log.1). Never touch active live streaming app.log.</div>
          </div>
          <div class="p-1.5 rounded bg-[#070b14] border border-cyber-border">
            <div class="text-sky-300 font-bold">3. lsof File Locks</div>
            <div class="text-slate-400 text-[10px]">Zero active PIDs holding write descriptors. Block .lock & active DB WAL.</div>
          </div>
          <div class="p-1.5 rounded bg-[#070b14] border border-cyber-border">
            <div class="text-sky-300 font-bold">4. Safety Floor</div>
            <div class="text-slate-400 text-[10px]">Direct stream compression to cold tier without temporary disk spikes.</div>
          </div>
          <div class="p-1.5 rounded bg-[#070b14] border border-cyber-border">
            <div class="text-sky-300 font-bold">5. SHA-256 Checksum</div>
            <div class="text-slate-400 text-[10px]">Verify archive integrity before unlinking original raw log from disk.</div>
          </div>
        </div>
      </div>

      <!-- Real Files on Disk Table -->
      <div class="space-y-1.5">
    `;

    data.files.forEach(f => {
      const isZipped = f.is_compressed || f.name.endsWith('.gz');
      html += `
        <div class="flex flex-col sm:flex-row sm:items-center justify-between p-2 rounded bg-[#070b14] border border-cyber-border hover:border-slate-700 transition gap-1.5">
          <div class="flex items-center space-x-2">
            <i data-lucide="${isZipped ? 'file-archive' : 'file-text'}" class="w-4 h-4 ${isZipped ? 'text-emerald-400' : 'text-rose-400'}"></i>
            <div>
              <span class="font-mono text-slate-200 text-xs font-bold">${f.name}</span>
              <span class="ml-2 font-mono text-slate-400 text-[11px]">(${f.size_formatted})</span>
            </div>
          </div>
          <div class="flex items-center space-x-2 text-[11px]">
            <span class="text-slate-300 font-mono text-[10px] hidden md:inline">${f.criteria_detail || ''}</span>
            <span class="px-2 py-0.5 rounded text-[10px] font-mono border ${f.badge}">${f.status}</span>
          </div>
        </div>
      `;
    });

    html += `</div>`;
    list.innerHTML = html;
    if (window.lucide) lucide.createIcons();

  } catch (err) {
    console.error('Error loading real filesystem:', err);
    list.innerHTML = `<div class="text-rose-400 py-3 text-center text-xs">Failed to load real filesystem telemetry: ${err.message}</div>`;
  }
}

async function openArchiveFolder() {
  try {
    const res = await fetch('/api/filesystem/open-folder', { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      showNotification('📂 Windows File Explorer opened at real .GZ archive directory!', 'success');
    } else {
      showNotification(`Note: ${data.message || data.error}`, 'warning');
    }
  } catch (err) {
    console.error('Error opening folder:', err);
  }
}

async function openRawFolder() {
  try {
    const res = await fetch('/api/filesystem/open-raw-folder', { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      showNotification('📂 Windows File Explorer opened at raw logs directory!', 'success');
    } else {
      showNotification(`Note: ${data.message || data.error}`, 'warning');
    }
  } catch (err) {
    console.error('Error opening folder:', err);
  }
}

async function executeRealZip() {
  try {
    const res = await fetch('/api/filesystem/execute-zip', { method: 'POST' });
    const data = await res.json();
    showNotification(`⚡ Real Gzip executed! Reclaimed ${data.reclaimed_mb} physical storage on hard disk.`, 'success');
    await loadRealFilesystem();
    if (typeof loadMetrics === 'function') loadMetrics();
  } catch (err) {
    console.error('Error executing real zip:', err);
  }
}

async function executeRealRollback() {
  try {
    const res = await fetch('/api/filesystem/execute-rollback', { method: 'POST' });
    const data = await res.json();
    showNotification(`↩️ Rollback executed! Gunzipped ${data.restored_files ? data.restored_files.length : 0} logs back to disk.`, 'info');
    await loadRealFilesystem();
    if (typeof loadMetrics === 'function') loadMetrics();
  } catch (err) {
    console.error('Error executing rollback:', err);
  }
}

async function renderArchitectureMatrix() {
  const list = document.getElementById('subsystemContentList');
  const msg = document.getElementById('subsystemMessage');
  const badge = document.getElementById('subsystemBadge');
  if (!list) return;

  if (badge) {
    badge.textContent = 'OS SUBSYSTEM ARCHITECTURE MATRIX';
    badge.className = 'text-[10px] font-mono px-2 py-0.5 rounded bg-amber-950/60 text-amber-300 border border-amber-500/40';
  }

  if (msg) {
    msg.innerHTML = `
      <div class="w-full">
        <span class="font-bold text-amber-400">Architectural Clarification for Judges:</span>
        <span class="text-slate-300">Disk Overflow operates in Storage Inodes. Worker Deadlock operates in Kernel RAM. Queue Lag operates in Network Streams. SSL operates in Cryptographic Proxy Memory.</span>
      </div>
    `;
  }

  list.innerHTML = `<div class="text-center py-4 text-slate-500 text-xs font-mono">// Fetching OS architecture layers...</div>`;

  try {
    const res = await fetch('/api/subsystem-architecture');
    const data = await res.json();

    let html = `
      <div class="overflow-x-auto">
        <table class="w-full text-left font-mono text-xs border border-cyber-border rounded-lg overflow-hidden">
          <thead class="bg-[#070b14] text-slate-300 border-b border-cyber-border text-[11px]">
            <tr>
              <th class="p-2 font-bold text-white">Problem Statement</th>
              <th class="p-2 font-bold text-sky-400">Subsystem & OS Layer</th>
              <th class="p-2 font-bold text-amber-300">Physical Medium</th>
              <th class="p-2 font-bold text-slate-300">Why NOT in Hard Disk?</th>
              <th class="p-2 font-bold text-emerald-400">Inspection Tools</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-cyber-border bg-[#0a0f1d]">
    `;

    data.matrix.forEach(row => {
      html += `
        <tr class="hover:bg-slate-900/40 transition">
          <td class="p-2 font-bold text-white">
            <span class="px-1.5 py-0.5 rounded text-[10px] border ${row.badge}">${row.problem}</span>
          </td>
          <td class="p-2 text-sky-300 text-[11px]">${row.layer}</td>
          <td class="p-2 text-amber-200 text-[11px]">${row.physical_medium}</td>
          <td class="p-2 text-slate-400 text-[10px] max-w-xs">${row.why_not_hard_disk}</td>
          <td class="p-2 font-mono text-[10px] text-emerald-300">${row.inspection_tools}</td>
        </tr>
      `;
    });

    html += `
          </tbody>
        </table>
      </div>
    `;

    list.innerHTML = html;
    if (window.lucide) lucide.createIcons();

  } catch (err) {
    console.error('Error rendering architecture matrix:', err);
    list.innerHTML = `<div class="text-rose-400 py-3 text-center text-xs">Failed to load architecture matrix: ${err.message}</div>`;
  }
}

async function fetchSubsystemState(faultType) {
  try {
    if (faultType === 'disk_overflow') {
      await loadRealFilesystem();
      return;
    }

    const res = await fetch(`/api/subsystem-state/${faultType}`);
    const data = await res.json();

    const list = document.getElementById('subsystemContentList');
    const msg = document.getElementById('subsystemMessage');
    const badge = document.getElementById('subsystemBadge');
    if (!list) return;

    if (badge) {
      badge.textContent = `${data.type.toUpperCase()} PROBE: ${data.metric_val || 'LIVE'}`;
      badge.className = data.is_fixed ? 
        'text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-500/40' : 
        'text-[10px] font-mono px-2 py-0.5 rounded bg-rose-950/60 text-rose-300 border border-rose-500/40 animate-pulse';
    }

    if (msg) {
      const layer = data.subsystem_layer ? `<span class="text-amber-400 block mt-1 text-[11px]">🧠 OS Layer: ${data.subsystem_layer.os_layer} (${data.subsystem_layer.physical_medium})</span>` : '';
      msg.innerHTML = `<div><span>${data.message}</span>${layer}</div>`;
    }

    if (!data.items || data.items.length === 0) {
      list.innerHTML = `<div class="text-slate-500 py-3 text-center text-xs">No active subsystem files to display.</div>`;
      return;
    }

    if (data.type === 'worker') {
      list.innerHTML = data.items.map(item => `
        <div class="flex items-center justify-between p-2 rounded bg-[#070b14] border border-cyber-border hover:border-slate-700 transition">
          <div class="flex items-center space-x-2">
            <i data-lucide="cpu" class="w-4 h-4 text-purple-400"></i>
            <span class="font-mono font-bold text-slate-200 text-xs">${item.name} (PID: ${item.pid})</span>
          </div>
          <div class="flex items-center space-x-3 text-xs">
            <span class="font-mono text-slate-400">Heartbeat: ${item.heartbeat}</span>
            <span class="px-2 py-0.5 rounded text-[10px] font-mono border ${item.badge}">${item.status}</span>
          </div>
        </div>
      `).join('');
    } else if (data.type === 'queue') {
      list.innerHTML = data.items.map(item => `
        <div class="flex items-center justify-between p-2 rounded bg-[#070b14] border border-cyber-border hover:border-slate-700 transition">
          <div class="flex items-center space-x-2">
            <i data-lucide="layers" class="w-4 h-4 text-amber-400"></i>
            <span class="font-mono text-slate-200 text-xs">${item.pod}</span>
          </div>
          <div class="flex items-center space-x-3 text-xs">
            <span class="font-mono text-slate-400">${item.rate}</span>
            <span class="px-2 py-0.5 rounded text-[10px] font-mono border ${item.badge}">${item.status}</span>
          </div>
        </div>
      `).join('');
    } else if (data.type === 'ssl') {
      list.innerHTML = data.items.map(item => `
        <div class="flex items-center justify-between p-2 rounded bg-[#070b14] border border-cyber-border hover:border-slate-700 transition">
          <span class="font-mono text-slate-400 text-xs">${item.key}:</span>
          <span class="font-mono px-2 py-0.5 rounded text-[11px] ${item.badge}">${item.val}</span>
        </div>
      `).join('');
    }

    if (window.lucide) lucide.createIcons();
  } catch (err) {
    console.error('Error fetching subsystem state:', err);
  }
}
'''

# Find Section 12 start and Section 13 start
sec12_regex = r'// -------------------------------------------------------------------------\s*// 12\. Visual Subsystem Inspector[\s\S]*?(?=// -------------------------------------------------------------------------\s*// 13\. Operational Database)'

if re.search(sec12_regex, js):
    js = re.sub(sec12_regex, new_js_logic + '\n', js, count=1)
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js)
    print("Successfully updated static/js/app.js!")
else:
    print("Warning: Section 12 regex not matched!")

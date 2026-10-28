import re

index_path = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\templates\index.html"

with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

new_tab_disk_html = '''      <!-- TAB 1: INTERACTIVE SRE FILE COMPRESSION WORKBENCH (JUDGE DEFENSE PANEL) -->
      <div id="showcaseTab-disk" class="space-y-4">
        
        <!-- Top Toolbar: Path, Status & Action Controls -->
        <div class="bg-[#070b14] border border-cyber-border rounded-xl p-4">
          <div class="flex flex-wrap items-center justify-between gap-3 mb-3 pb-3 border-b border-cyber-border">
            <div>
              <div class="flex items-center space-x-2">
                <i data-lucide="folder-open" class="w-5 h-5 text-sky-400"></i>
                <h3 class="text-sm font-bold text-white uppercase tracking-wider font-mono">Interactive SRE File Compression Workbench</h3>
                <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Live Hard Drive & Shannon Entropy</span>
              </div>
              <p class="text-xs text-slate-400 mt-1">
                Demonstrates to judges why some files compress efficiently and other files cannot be zipped. Evaluates Shannon Entropy, MIME Types, and Kernel Locks.
              </p>
            </div>
            <div class="flex items-center space-x-3">
              <span id="diskShowcaseStatusBadge" class="px-2.5 py-1 rounded text-xs font-mono font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">94.2% CRITICAL (5.7 MB UNCOMPRESSED)</span>
            </div>
          </div>

          <!-- Interactive Filter Pills & Bulk Controls -->
          <div class="flex flex-wrap items-center justify-between gap-2.5">
            <!-- Filter Pills -->
            <div class="flex flex-wrap items-center gap-1.5 text-xs font-mono">
              <span class="text-slate-400 text-[11px] mr-1">Filter Formats:</span>
              <button id="wbFilter-all" onclick="filterWorkbenchFiles('all')" class="px-2.5 py-1 rounded bg-sky-600 text-white font-semibold transition">All Formats (8)</button>
              <button id="wbFilter-eligible" onclick="filterWorkbenchFiles('eligible')" class="px-2.5 py-1 rounded bg-slate-800 text-emerald-300 hover:bg-slate-700 transition">Eligible Text/SQL (4)</button>
              <button id="wbFilter-ineligible" onclick="filterWorkbenchFiles('ineligible')" class="px-2.5 py-1 rounded bg-slate-800 text-slate-400 hover:bg-slate-700 transition">Ineligible Binary (2)</button>
              <button id="wbFilter-protected" onclick="filterWorkbenchFiles('protected')" class="px-2.5 py-1 rounded bg-slate-800 text-amber-300 hover:bg-slate-700 transition">Protected Locks (2)</button>
            </div>

            <!-- Action Buttons for Judges -->
            <div class="flex flex-wrap items-center gap-2">
              <button onclick="applyAISafetyFilter()" class="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-mono text-xs font-bold transition flex items-center gap-1.5 shadow-lg shadow-indigo-600/30" title="Automatically selects only safe, high-efficiency text files and rejects ineligible formats">
                <i data-lucide="sparkles" class="w-3.5 h-3.5 text-indigo-200"></i>
                <span>🧠 AI Safety Filter (Auto-Select Safe)</span>
              </button>
              <button id="compressSelectedBtn" onclick="compressSelectedFiles()" class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-mono text-xs font-bold transition flex items-center gap-1.5 shadow-lg shadow-emerald-600/30">
                <i data-lucide="archive" class="w-3.5 h-3.5"></i>
                <span>⚡ Compress Selected Files</span>
              </button>
              <button onclick="rollbackSelectedFiles()" class="px-2.5 py-1.5 rounded-lg bg-amber-600/20 hover:bg-amber-600/30 text-amber-300 border border-amber-500/30 font-mono text-xs transition flex items-center gap-1.5">
                <i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i>
                <span>↩️ Rollback (Gunzip to Raw)</span>
              </button>
              <button onclick="openArchiveFolder()" class="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 font-mono text-xs transition flex items-center gap-1.5" title="Opens the real archive folder on this computer's hard drive">
                <i data-lucide="folder-open" class="w-3.5 h-3.5 text-sky-400"></i>
                <span>📂 Open in Explorer</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Interactive File Selection Table (Addresses the Judge's Exact Question!) -->
        <div class="bg-[#070b14] border border-cyber-border rounded-xl p-3 overflow-x-auto">
          <table class="w-full text-left font-mono text-xs border-collapse">
            <thead>
              <tr class="border-b border-cyber-border text-slate-400 text-[11px] pb-2">
                <th class="p-2 w-10 text-center">
                  <input type="checkbox" id="selectAllCheckbox" onchange="toggleSelectAllFiles(this)" checked class="rounded bg-slate-900 border-slate-700 text-sky-500 focus:ring-0">
                </th>
                <th class="p-2 font-bold text-white">File Name & Format</th>
                <th class="p-2 font-bold text-sky-400">Category</th>
                <th class="p-2 font-bold text-slate-300">Disk Size</th>
                <th class="p-2 font-bold text-purple-400">Shannon Entropy</th>
                <th class="p-2 font-bold text-emerald-400">Compression Efficiency</th>
                <th class="p-2 font-bold text-amber-300">SRE Verdict & Reason</th>
              </tr>
            </thead>
            <tbody id="interactiveFileTableBody" class="divide-y divide-cyber-border">
              <!-- Dynamically populated or default fallback -->
              
              <!-- 1. Text Log 1 -->
              <tr class="file-row hover:bg-slate-900/40 transition" data-category="eligible" data-filename="app-access.log.1">
                <td class="p-2 text-center">
                  <input type="checkbox" class="file-checkbox rounded bg-slate-900 border-slate-700 text-sky-500 focus:ring-0" value="app-access.log.1" checked>
                </td>
                <td class="p-2 font-bold text-white flex items-center gap-2">
                  <i data-lucide="file-text" class="w-4 h-4 text-emerald-400"></i>
                  <span>app-access.log.1</span>
                </td>
                <td class="p-2 text-slate-300">Rotated Plaintext Log</td>
                <td class="p-2 text-rose-300 font-bold">2.29 MB</td>
                <td class="p-2">
                  <span class="px-1.5 py-0.5 rounded text-[10px] bg-purple-500/20 text-purple-300 border border-purple-500/30">0.42 (Low Entropy)</span>
                </td>
                <td class="p-2 text-emerald-400 font-bold">~94% Space Saved</td>
                <td class="p-2">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">✅ SAFE (ELIGIBLE)</span>
                  <span class="text-[10px] text-slate-400 block mt-0.5">Repetitive ASCII words. Lempel-Ziv dictionary match.</span>
                </td>
              </tr>

              <!-- 2. Text Log 2 -->
              <tr class="file-row hover:bg-slate-900/40 transition" data-category="eligible" data-filename="app-error.log.1">
                <td class="p-2 text-center">
                  <input type="checkbox" class="file-checkbox rounded bg-slate-900 border-slate-700 text-sky-500 focus:ring-0" value="app-error.log.1" checked>
                </td>
                <td class="p-2 font-bold text-white flex items-center gap-2">
                  <i data-lucide="file-text" class="w-4 h-4 text-emerald-400"></i>
                  <span>app-error.log.1</span>
                </td>
                <td class="p-2 text-slate-300">Rotated Stderr Log</td>
                <td class="p-2 text-rose-300 font-bold">1.11 MB</td>
                <td class="p-2">
                  <span class="px-1.5 py-0.5 rounded text-[10px] bg-purple-500/20 text-purple-300 border border-purple-500/30">0.45 (Low Entropy)</span>
                </td>
                <td class="p-2 text-emerald-400 font-bold">~97% Space Saved</td>
                <td class="p-2">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">✅ SAFE (ELIGIBLE)</span>
                  <span class="text-[10px] text-slate-400 block mt-0.5">mtime > 48h. Zero active open lsof locks.</span>
                </td>
              </tr>

              <!-- 3. Database SQL Dump -->
              <tr class="file-row hover:bg-slate-900/40 transition" data-category="eligible" data-filename="database_backup_dump.sql">
                <td class="p-2 text-center">
                  <input type="checkbox" class="file-checkbox rounded bg-slate-900 border-slate-700 text-sky-500 focus:ring-0" value="database_backup_dump.sql" checked>
                </td>
                <td class="p-2 font-bold text-white flex items-center gap-2">
                  <i data-lucide="database" class="w-4 h-4 text-sky-400"></i>
                  <span>database_backup_dump.sql</span>
                </td>
                <td class="p-2 text-slate-300">Database SQL Dump</td>
                <td class="p-2 text-rose-300 font-bold">1.69 MB</td>
                <td class="p-2">
                  <span class="px-1.5 py-0.5 rounded text-[10px] bg-purple-500/20 text-purple-300 border border-purple-500/30">0.38 (Very Low)</span>
                </td>
                <td class="p-2 text-emerald-400 font-bold">~92% Space Saved</td>
                <td class="p-2">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">✅ SAFE (ELIGIBLE)</span>
                  <span class="text-[10px] text-slate-400 block mt-0.5">SQL INSERT statements repeat columns. High Huffman efficiency.</span>
                </td>
              </tr>

              <!-- 4. JSON Telemetry -->
              <tr class="file-row hover:bg-slate-900/40 transition" data-category="eligible" data-filename="telemetry_stream.json">
                <td class="p-2 text-center">
                  <input type="checkbox" class="file-checkbox rounded bg-slate-900 border-slate-700 text-sky-500 focus:ring-0" value="telemetry_stream.json" checked>
                </td>
                <td class="p-2 font-bold text-white flex items-center gap-2">
                  <i data-lucide="code" class="w-4 h-4 text-sky-400"></i>
                  <span>telemetry_stream.json</span>
                </td>
                <td class="p-2 text-slate-300">Raw JSON Events</td>
                <td class="p-2 text-rose-300 font-bold">679.1 KB</td>
                <td class="p-2">
                  <span class="px-1.5 py-0.5 rounded text-[10px] bg-purple-500/20 text-purple-300 border border-purple-500/30">0.40 (Low Entropy)</span>
                </td>
                <td class="p-2 text-emerald-400 font-bold">~90% Space Saved</td>
                <td class="p-2">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">✅ SAFE (ELIGIBLE)</span>
                  <span class="text-[10px] text-slate-400 block mt-0.5">Key-value schema redundancy. Outstanding ratio.</span>
                </td>
              </tr>

              <!-- 5. Pre-Compressed Archive -->
              <tr class="file-row hover:bg-slate-900/40 transition bg-slate-950/40" data-category="ineligible" data-filename="legacy-backup.tar.gz">
                <td class="p-2 text-center">
                  <input type="checkbox" class="file-checkbox rounded bg-slate-900 border-slate-700 text-sky-500 focus:ring-0" value="legacy-backup.tar.gz">
                </td>
                <td class="p-2 font-bold text-slate-400 flex items-center gap-2">
                  <i data-lucide="file-archive" class="w-4 h-4 text-slate-500"></i>
                  <span>legacy-backup.tar.gz</span>
                </td>
                <td class="p-2 text-slate-400">Pre-Compressed Gzip</td>
                <td class="p-2 text-slate-400">24.0 KB</td>
                <td class="p-2">
                  <span class="px-1.5 py-0.5 rounded text-[10px] bg-slate-800 text-slate-400 border border-slate-700">0.99 (Max Entropy)</span>
                </td>
                <td class="p-2 text-slate-400">0% Savings (Waste CPU)</td>
                <td class="p-2">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-slate-400 border border-slate-700">❌ REJECT: INCOMPRESSIBLE</span>
                  <span class="text-[10px] text-slate-500 block mt-0.5">Already Deflate-coded. Re-gzipping adds headers and expands file!</span>
                </td>
              </tr>

              <!-- 6. Multimedia Binary -->
              <tr class="file-row hover:bg-slate-900/40 transition bg-slate-950/40" data-category="ineligible" data-filename="dashboard-preview.png">
                <td class="p-2 text-center">
                  <input type="checkbox" class="file-checkbox rounded bg-slate-900 border-slate-700 text-sky-500 focus:ring-0" value="dashboard-preview.png">
                </td>
                <td class="p-2 font-bold text-slate-400 flex items-center gap-2">
                  <i data-lucide="image" class="w-4 h-4 text-slate-500"></i>
                  <span>dashboard-preview.png</span>
                </td>
                <td class="p-2 text-slate-400">Binary Multimedia (PNG)</td>
                <td class="p-2 text-slate-400">3.9 KB</td>
                <td class="p-2">
                  <span class="px-1.5 py-0.5 rounded text-[10px] bg-slate-800 text-slate-400 border border-slate-700">0.98 (Max Entropy)</span>
                </td>
                <td class="p-2 text-slate-400">&lt; 1% (Ineffective)</td>
                <td class="p-2">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-slate-400 border border-slate-700">❌ REJECT: BINARY IMAGE</span>
                  <span class="text-[10px] text-slate-500 block mt-0.5">PNG uses internal Deflate. Lossless gzip yields &lt; 1% reduction.</span>
                </td>
              </tr>

              <!-- 7. Active Kernel Lock -->
              <tr class="file-row hover:bg-slate-900/40 transition bg-amber-950/20" data-category="protected" data-filename="postgres-daemon.lock">
                <td class="p-2 text-center">
                  <input type="checkbox" class="file-checkbox rounded bg-slate-900 border-slate-700 text-sky-500 focus:ring-0" value="postgres-daemon.lock">
                </td>
                <td class="p-2 font-bold text-amber-300 flex items-center gap-2">
                  <i data-lucide="shield-alert" class="w-4 h-4 text-amber-400"></i>
                  <span>postgres-daemon.lock</span>
                </td>
                <td class="p-2 text-amber-300/80">Kernel File Lock</td>
                <td class="p-2 text-amber-300 font-bold">64 B</td>
                <td class="p-2">
                  <span class="px-1.5 py-0.5 rounded text-[10px] bg-amber-500/20 text-amber-300 border border-amber-500/30">0.55 (Lock Handle)</span>
                </td>
                <td class="p-2 text-rose-400 font-bold">DANGEROUS: Crash</td>
                <td class="p-2">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">🚨 BLOCKED: ACTIVE KERNEL LOCK</span>
                  <span class="text-[10px] text-amber-400/80 block mt-0.5">Held by PID 4092 (lsof). Deletion causes database panic & inode leak.</span>
                </td>
              </tr>

              <!-- 8. Active Streaming Handle -->
              <tr class="file-row hover:bg-slate-900/40 transition bg-amber-950/20" data-category="protected" data-filename="app-access.log">
                <td class="p-2 text-center">
                  <input type="checkbox" class="file-checkbox rounded bg-slate-900 border-slate-700 text-sky-500 focus:ring-0" value="app-access.log">
                </td>
                <td class="p-2 font-bold text-amber-300 flex items-center gap-2">
                  <i data-lucide="activity" class="w-4 h-4 text-amber-400"></i>
                  <span>app-access.log</span>
                </td>
                <td class="p-2 text-amber-300/80">Active Streaming Handle</td>
                <td class="p-2 text-amber-300 font-bold">120 B</td>
                <td class="p-2">
                  <span class="px-1.5 py-0.5 rounded text-[10px] bg-amber-500/20 text-amber-300 border border-amber-500/30">0.64 (Active Stream)</span>
                </td>
                <td class="p-2 text-rose-400 font-bold">DANGEROUS: Race</td>
                <td class="p-2">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">🚨 BLOCKED: ACTIVE WRITER</span>
                  <span class="text-[10px] text-amber-400/80 block mt-0.5">Daemon currently writing. Only rotated *.log.1 is eligible.</span>
                </td>
              </tr>

            </tbody>
          </table>
        </div>

        <!-- SRE Technical Explanation: Why Different Formats Can or Cannot Be Zipped -->
        <div class="bg-[#0c1220] border border-cyber-border rounded-xl p-4 text-xs">
          <div class="flex items-center justify-between pb-2 mb-3 border-b border-cyber-border">
            <h4 class="font-bold text-white flex items-center gap-2 text-sm">
              <i data-lucide="info" class="w-4 h-4 text-sky-400"></i>
              SRE Technical Defense: Why Different File Formats Can or Cannot Be Zipped
            </h4>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-sky-500/20 text-sky-300 border border-sky-500/30">Mathematical & Operating System Proof</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-4 gap-3 font-mono text-[11px]">
            <div class="p-2.5 rounded-lg bg-[#070b14] border border-emerald-500/30 space-y-1">
              <div class="text-emerald-400 font-bold">1. Plaintext (.log, .sql, .json)</div>
              <div class="text-slate-300 text-[10px]">
                Low Shannon entropy (0.35 - 0.45). Repeated ASCII words allow Lempel-Ziv dictionary matching to replace strings with bit codes. <strong>Achieves 85% - 97% reduction.</strong>
              </div>
            </div>

            <div class="p-2.5 rounded-lg bg-[#070b14] border border-slate-700 space-y-1">
              <div class="text-slate-300 font-bold">2. Pre-Compressed (.tar.gz, .zip)</div>
              <div class="text-slate-400 text-[10px]">
                Maximum Shannon entropy (~0.99). Bytes have a uniform random distribution. Zero pattern redundancy means gzip cannot compress and <strong>adds 18-byte headers, expanding file size!</strong>
              </div>
            </div>

            <div class="p-2.5 rounded-lg bg-[#070b14] border border-slate-700 space-y-1">
              <div class="text-slate-300 font-bold">3. Multimedia (.png, .jpg, .mp4)</div>
              <div class="text-slate-400 text-[10px]">
                PNG uses internal Deflate and JPEG uses discrete cosine transforms. Re-compressing already compressed image channels wastes CPU time and <strong>yields &lt; 0.5% space reduction.</strong>
              </div>
            </div>

            <div class="p-2.5 rounded-lg bg-[#070b14] border border-amber-500/30 space-y-1">
              <div class="text-amber-300 font-bold">4. Kernel Locks (.lock, active .log)</div>
              <div class="text-amber-200/90 text-[10px]">
                Held by running operating system processes (`lsof`). Compressing an open file descriptor creates <strong>orphan unlinked open inodes</strong> (space not freed until reboot) or daemon crash.
              </div>
            </div>
          </div>
        </div>

      </div>'''

# Match from <!-- TAB 1: DISK OVERFLOW (REAL PHYSICAL STORAGE & 5 SRE CRITERIA) --> up to <!-- TAB 2: STUCK WORKER
tab1_start = '<!-- TAB 1: DISK OVERFLOW'
tab2_start = '<!-- TAB 2: STUCK WORKER'

start_idx = html.find(tab1_start)
end_idx = html.find(tab2_start)

print("Tab 1 start:", start_idx, "Tab 2 start:", end_idx)

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + new_tab_disk_html + "\n\n      " + html[end_idx:]
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Successfully replaced showcaseTab-disk with the Interactive SRE Compression Workbench!")
else:
    print("Error: Tab 1 or Tab 2 markers not found!")

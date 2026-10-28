import os

index_path = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\templates\index.html"

new_html = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SafeOps AI - Enterprise SRE Autonomous Remediation System</title>
  
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: { 50: '#f0f9ff', 100: '#e0f2fe', 500: '#0284c7', 600: '#0369a1', 900: '#0c4a6e' },
            cyber: { dark: '#090d16', card: '#0f172a', border: '#1e293b', accent: '#38bdf8', emerald: '#10b981', amber: '#f59e0b', rose: '#f43f5e', purple: '#a855f7' }
          },
          fontFamily: {
            mono: ['JetBrains Mono', 'Fira Code', 'Courier New', 'monospace'],
            sans: ['Inter', 'system-ui', 'sans-serif']
          }
        }
      }
    }
  </script>
  
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <!-- Canvas Confetti -->
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
  <link rel="stylesheet" href="/static/css/styles.css">
  <style>
    /* Clean custom scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0b0f19; }
    ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #334155; }
  </style>
</head>
<body class="bg-[#070b14] text-slate-100 min-h-screen font-sans antialiased selection:bg-sky-500 selection:text-white">

  <!-- TOP HEADER / BRAND NAVIGATION BAR -->
  <header class="bg-[#0b1120] border-b border-cyber-border sticky top-0 z-50 shadow-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
      <div class="flex flex-wrap items-center justify-between gap-4">
        
        <!-- Logo & Hackathon Team -->
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-500 via-indigo-500 to-emerald-400 p-0.5 flex items-center justify-center shadow-lg shadow-sky-500/20">
            <div class="w-full h-full bg-[#0b1120] rounded-[10px] flex items-center justify-center">
              <i data-lucide="shield-check" class="w-5 h-5 text-sky-400"></i>
            </div>
          </div>
          <div>
            <div class="flex items-center space-x-2">
              <h1 class="text-base font-extrabold text-white tracking-wide font-mono">SafeOps AI</h1>
              <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 flex items-center gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span> LIVE CLUSTER
              </span>
            </div>
            <p class="text-xs text-slate-400">Cynefian AI-Ops Track (Problem AO-04) | <strong class="text-slate-200">Team Idea Ignitors (XH-23)</strong></p>
          </div>
        </div>

        <!-- Live Telemetry Status Bar -->
        <div class="flex flex-wrap items-center gap-2 font-mono text-xs">
          <!-- Disk Status -->
          <div class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-[#070b14] border border-cyber-border">
            <i data-lucide="hard-drive" class="w-3.5 h-3.5 text-rose-400"></i>
            <span class="text-slate-400">Disk:</span>
            <span id="navDiskMetric" class="font-bold text-rose-400">94.2% (CRIT)</span>
          </div>

          <!-- Worker Status -->
          <div class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-[#070b14] border border-cyber-border">
            <i data-lucide="cpu" class="w-3.5 h-3.5 text-purple-400"></i>
            <span class="text-slate-400">Workers:</span>
            <span id="navWorkerMetric" class="font-bold text-purple-300">1 DEADLOCK</span>
          </div>

          <!-- Queue Status -->
          <div class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-[#070b14] border border-cyber-border">
            <i data-lucide="layers" class="w-3.5 h-3.5 text-amber-400"></i>
            <span class="text-slate-400">Queue:</span>
            <span id="navQueueMetric" class="font-bold text-amber-300">48,250 msgs</span>
          </div>

          <!-- SSL Status -->
          <div class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-[#070b14] border border-cyber-border">
            <i data-lucide="lock" class="w-3.5 h-3.5 text-cyan-400"></i>
            <span class="text-slate-400">SSL:</span>
            <span id="navSslMetric" class="font-bold text-cyan-300">2.0 Days</span>
          </div>

          <!-- Master Kill-Switch Toggle -->
          <button id="navKillSwitchBtn" onclick="toggleKillSwitch()" class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-emerald-950/40 text-emerald-300 border border-emerald-500/40 hover:bg-emerald-900/50 transition">
            <i data-lucide="power" class="w-3.5 h-3.5 text-emerald-400"></i>
            <span id="navKillSwitchText" class="font-bold">Kill-Switch: SAFE</span>
          </button>
        </div>

      </div>
    </div>
  </header>

  <!-- MAIN NAVIGATION TABS -->
  <div class="bg-[#0c1222] border-b border-cyber-border sticky top-[65px] z-40 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center space-x-2 overflow-x-auto py-2.5 scrollbar-none text-xs font-mono font-semibold">
        
        <button id="navTabBtn-disk" onclick="switchMainTab('disk')" class="px-3.5 py-2 rounded-lg bg-sky-600 text-white flex items-center space-x-2 shadow transition whitespace-nowrap">
          <i data-lucide="hard-drive" class="w-4 h-4"></i>
          <span>1. Smart Disk Optimizer (How & Where Files Zip)</span>
        </button>

        <button id="navTabBtn-worker" onclick="switchMainTab('worker')" class="px-3.5 py-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 flex items-center space-x-2 transition whitespace-nowrap">
          <i data-lucide="cpu" class="w-4 h-4"></i>
          <span>2. Worker Deadlock (Kernel RAM)</span>
        </button>

        <button id="navTabBtn-queue" onclick="switchMainTab('queue')" class="px-3.5 py-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 flex items-center space-x-2 transition whitespace-nowrap">
          <i data-lucide="layers" class="w-4 h-4"></i>
          <span>3. Queue Lag (Kubernetes Pods)</span>
        </button>

        <button id="navTabBtn-ssl" onclick="switchMainTab('ssl')" class="px-3.5 py-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 flex items-center space-x-2 transition whitespace-nowrap">
          <i data-lucide="shield" class="w-4 h-4"></i>
          <span>4. Edge SSL Rotation (Proxy Memory)</span>
        </button>

        <button id="navTabBtn-arch" onclick="switchMainTab('arch')" class="px-3.5 py-2 rounded-lg text-amber-300 bg-amber-500/10 border border-amber-500/30 hover:bg-amber-500/20 flex items-center space-x-2 transition whitespace-nowrap">
          <i data-lucide="brain-circuit" class="w-4 h-4"></i>
          <span>5. Architecture Map: Where Each Problem Lives</span>
        </button>

        <button id="navTabBtn-audit" onclick="switchMainTab('audit')" class="px-3.5 py-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 flex items-center space-x-2 transition whitespace-nowrap">
          <i data-lucide="file-check-2" class="w-4 h-4"></i>
          <span>6. ITIL Audit Trail & Change Logs</span>
        </button>

      </div>
    </div>
  </div>

  <!-- MAIN CONTAINER -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">

    <!-- ========================================================================= -->
    <!-- TAB 1: SMART DISK OPTIMIZER & SRE ZIPPING (CORE JUDGE DEMO) -->
    <!-- ========================================================================= -->
    <div id="mainView-disk" class="space-y-6">
      
      <!-- CARD 1: VISUAL STORAGE PIPELINE (WHERE ARE THE FILES STORED?) -->
      <div class="bg-[#0f172a] border border-cyber-border rounded-xl p-5 shadow-lg">
        <div class="flex flex-wrap items-center justify-between gap-3 pb-3 mb-4 border-b border-cyber-border">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-lg bg-sky-500/20 border border-sky-500/30 flex items-center justify-center">
              <i data-lucide="map-pin" class="w-4 h-4 text-sky-400"></i>
            </div>
            <div>
              <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono">1. Physical Storage Architecture & File Locations</h2>
              <p class="text-xs text-slate-400">Directly answers the judge: Where are files stored before and after zipping?</p>
            </div>
          </div>
          <span class="text-xs font-mono px-2.5 py-1 rounded bg-sky-950/60 text-sky-300 border border-sky-500/40">HOST HARD DRIVE (C:\\...\\scratch\\safeops-ai)</span>
        </div>

        <!-- 3-Step Storage Visual Flow -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
          
          <!-- Source Hot Storage -->
          <div class="p-3.5 rounded-xl bg-[#070b14] border border-cyber-border space-y-2">
            <div class="flex items-center justify-between text-slate-400">
              <span class="font-bold text-white flex items-center gap-1.5">
                <i data-lucide="folder" class="w-4 h-4 text-rose-400"></i> Source Hot Tier (Raw Logs)
              </span>
              <span class="px-1.5 py-0.5 rounded text-[10px] bg-rose-500/20 text-rose-300">Uncompressed</span>
            </div>
            <div class="text-[11px] text-slate-300 bg-[#0b101c] p-2 rounded border border-slate-800 break-all select-all font-mono">
              /simulated_system/var_log_app/
            </div>
            <p class="text-[10px] text-slate-400">Contains uncompressed UTF-8 logs, SQL dumps, active writer logs, and kernel lock files.</p>
            <button onclick="openRawFolder()" class="w-full py-1.5 px-3 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold transition flex items-center justify-center gap-1.5">
              <i data-lucide="folder-open" class="w-3.5 h-3.5 text-sky-400"></i>
              Open Source Logs in Explorer
            </button>
          </div>

          <!-- SRE Compression Pipeline -->
          <div class="p-3.5 rounded-xl bg-[#070b14] border border-sky-500/40 flex flex-col justify-between space-y-2">
            <div class="flex items-center justify-between text-slate-400">
              <span class="font-bold text-sky-300 flex items-center gap-1.5">
                <i data-lucide="cpu" class="w-4 h-4 text-sky-400"></i> SafeOps Gzip Pipeline
              </span>
              <span class="px-1.5 py-0.5 rounded text-[10px] bg-sky-500/20 text-sky-300">Level 9 In-Stream</span>
            </div>
            <div class="text-[11px] text-slate-300 space-y-1">
              <div class="flex justify-between"><span>Current Partition:</span> <span id="pipelineDiskPct" class="text-rose-400 font-bold">94.2%</span></div>
              <div class="flex justify-between"><span>Space to Reclaim:</span> <span class="text-emerald-400 font-bold">~5.08 MB (94%)</span></div>
              <div class="w-full bg-slate-800 rounded-full h-2 overflow-hidden mt-1">
                <div id="pipelineDiskBar" class="bg-rose-500 h-2 rounded-full transition-all duration-700" style="width: 94.2%"></div>
              </div>
            </div>
            <p class="text-[10px] text-slate-400">Streams directly from raw disk blocks to archive tier without creating temporary disk spikes.</p>
          </div>

          <!-- Target Cold Archive -->
          <div class="p-3.5 rounded-xl bg-[#070b14] border border-emerald-500/40 space-y-2">
            <div class="flex items-center justify-between text-slate-400">
              <span class="font-bold text-emerald-300 flex items-center gap-1.5">
                <i data-lucide="file-archive" class="w-4 h-4 text-emerald-400"></i> Target Cold Tier (/archive)
              </span>
              <span class="px-1.5 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-300">Compressed</span>
            </div>
            <div class="text-[11px] text-slate-300 bg-[#0b101c] p-2 rounded border border-slate-800 break-all select-all font-mono">
              /simulated_system/var_log_app/archive/
            </div>
            <p class="text-[10px] text-slate-400">Stores production `.gz` archives with SHA-256 verification before original logs are unlinked.</p>
            <button onclick="openArchiveFolder()" class="w-full py-1.5 px-3 rounded bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition flex items-center justify-center gap-1.5 shadow-md shadow-emerald-600/30">
              <i data-lucide="folder-check" class="w-3.5 h-3.5"></i>
              Open .GZ Archive in Explorer
            </button>
          </div>

        </div>
      </div>

      <!-- CARD 2: THE 4 SRE CRITERIA (BASED ON WHAT CRITERIA DOES IT ZIP?) -->
      <div class="bg-[#0f172a] border border-cyber-border rounded-xl p-5 shadow-lg">
        <div class="flex flex-wrap items-center justify-between gap-3 pb-3 mb-4 border-b border-cyber-border">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-lg bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center">
              <i data-lucide="check-check" class="w-4 h-4 text-indigo-400"></i>
            </div>
            <div>
              <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono">2. The 4 Strict SRE Compression Criteria (Why Not All Files Can Be Zipped)</h2>
              <p class="text-xs text-slate-400">Directly answers the judge: How does the AI decide which files are safe to zip?</p>
            </div>
          </div>
          <span class="text-xs font-mono px-2.5 py-1 rounded bg-indigo-950/60 text-indigo-300 border border-indigo-500/40">PRODUCTION SAFETY POLICY</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs font-mono">
          
          <!-- Criteria 1 -->
          <div class="p-3 rounded-lg bg-[#070b14] border border-emerald-500/30 space-y-1.5">
            <div class="flex items-center justify-between">
              <span class="font-bold text-emerald-400">1. Entropy Check</span>
              <span class="text-[10px] text-emerald-300">Shannon < 0.50</span>
            </div>
            <p class="text-[11px] text-slate-300 leading-snug">
              Plain text logs, SQL dumps, and JSON have low entropy and high character repetition. <strong>Gzip LZ77 dictionary matches achieve ~94% space reduction.</strong>
            </p>
            <div class="text-[10px] text-rose-300 bg-rose-950/30 p-1.5 rounded border border-rose-500/30">
              ❌ Pre-compressed (.tar.gz, .png) has entropy > 0.98. Gzipping saves 0 MB & wastes CPU!
            </div>
          </div>

          <!-- Criteria 2 -->
          <div class="p-3 rounded-lg bg-[#070b14] border border-emerald-500/30 space-y-1.5">
            <div class="flex items-center justify-between">
              <span class="font-bold text-emerald-400">2. Inactivity Age</span>
              <span class="text-[10px] text-emerald-300">mtime > 48 Hours</span>
            </div>
            <p class="text-[11px] text-slate-300 leading-snug">
              Only rotated generation logs (<code class="text-sky-300">*.log.1</code>) are touched. They are static and no longer being written to.
            </p>
            <div class="text-[10px] text-rose-300 bg-rose-950/30 p-1.5 rounded border border-rose-500/30">
              ❌ Active stream (app.log) is protected. Compressing live logs causes line truncation race conditions!
            </div>
          </div>

          <!-- Criteria 3 -->
          <div class="p-3 rounded-lg bg-[#070b14] border border-amber-500/30 space-y-1.5">
            <div class="flex items-center justify-between">
              <span class="font-bold text-amber-400">3. Kernel Locks</span>
              <span class="text-[10px] text-amber-300">lsof check == 0</span>
            </div>
            <p class="text-[11px] text-slate-300 leading-snug">
              Verifies zero active operating system PIDs hold an open write file descriptor on the target file.
            </p>
            <div class="text-[10px] text-amber-300 bg-amber-950/30 p-1.5 rounded border border-amber-500/30">
              🚨 Active lock (postgres.lock) held by PID 4092 is BLOCKED. Deletion crashes the database!
            </div>
          </div>

          <!-- Criteria 4 -->
          <div class="p-3 rounded-lg bg-[#070b14] border border-sky-500/30 space-y-1.5">
            <div class="flex items-center justify-between">
              <span class="font-bold text-sky-400">4. Checksum Floor</span>
              <span class="text-[10px] text-sky-300">SHA-256 Validated</span>
            </div>
            <p class="text-[11px] text-slate-300 leading-snug">
              Direct-to-archive stream ensures partition never fills with temporary staging duplicates.
            </p>
            <div class="text-[10px] text-sky-300 bg-sky-950/30 p-1.5 rounded border border-sky-500/30">
              ✅ SHA-256 integrity hash is computed and verified before unlinking the raw log.
            </div>
          </div>

        </div>
      </div>

      <!-- CARD 3: INTERACTIVE FILE-BY-FILE COMPRESSION WORKBENCH -->
      <div class="bg-[#0f172a] border border-cyber-border rounded-xl p-5 shadow-lg space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-cyber-border">
          <div>
            <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono">3. Interactive File-by-File SRE Workbench</h2>
            <p class="text-xs text-slate-400">Select files to analyze, test the AI Safety Filter, or execute real physical Gzip compression on disk.</p>
          </div>

          <!-- Action Buttons -->
          <div class="flex flex-wrap items-center gap-2 font-mono text-xs">
            <button onclick="applyAISafetyFilter()" class="px-3.5 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-bold transition flex items-center gap-1.5 shadow-md shadow-indigo-600/30">
              <i data-lucide="sparkles" class="w-4 h-4 text-indigo-200"></i>
              <span>🧠 AI Safety Filter (Auto-Select Safe)</span>
            </button>
            <button id="compressSelectedBtn" onclick="compressSelectedFiles()" class="px-3.5 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold transition flex items-center gap-1.5 shadow-md shadow-emerald-600/30">
              <i data-lucide="archive" class="w-4 h-4"></i>
              <span>⚡ Compress Selected Files</span>
            </button>
            <button onclick="rollbackSelectedFiles()" class="px-3 py-2 rounded-lg bg-amber-600/20 hover:bg-amber-600/30 text-amber-300 border border-amber-500/30 font-bold transition flex items-center gap-1.5">
              <i data-lucide="rotate-ccw" class="w-4 h-4"></i>
              <span>↩️ Rollback to Raw</span>
            </button>
          </div>
        </div>

        <!-- Filter Pills -->
        <div class="flex flex-wrap items-center justify-between gap-2 text-xs font-mono">
          <div class="flex items-center gap-1.5">
            <span class="text-slate-400 mr-1">Filter View:</span>
            <button id="wbFilter-all" onclick="filterWorkbenchFiles('all')" class="px-2.5 py-1 rounded bg-sky-600 text-white font-semibold transition">All Files (8)</button>
            <button id="wbFilter-eligible" onclick="filterWorkbenchFiles('eligible')" class="px-2.5 py-1 rounded bg-slate-800 text-emerald-300 hover:bg-slate-700 transition">Eligible Logs/SQL (4)</button>
            <button id="wbFilter-ineligible" onclick="filterWorkbenchFiles('ineligible')" class="px-2.5 py-1 rounded bg-slate-800 text-slate-400 hover:bg-slate-700 transition">Ineligible Binary (2)</button>
            <button id="wbFilter-protected" onclick="filterWorkbenchFiles('protected')" class="px-2.5 py-1 rounded bg-slate-800 text-amber-300 hover:bg-slate-700 transition">Protected Locks (2)</button>
          </div>
          <span class="text-[11px] text-slate-400">Tip: Check an ineligible file to see how SafeOps AI blocks unsafe actions!</span>
        </div>

        <!-- The Table of 8 Real Files -->
        <div class="overflow-x-auto rounded-lg border border-cyber-border">
          <table class="w-full text-left font-mono text-xs border-collapse">
            <thead>
              <tr class="bg-[#070b14] border-b border-cyber-border text-slate-400 text-[11px]">
                <th class="p-2.5 w-10 text-center">
                  <input type="checkbox" id="selectAllCheckbox" onchange="toggleSelectAllFiles(this)" class="rounded bg-slate-900 border-slate-700 text-sky-500 focus:ring-0">
                </th>
                <th class="p-2.5 font-bold text-white">File Name</th>
                <th class="p-2.5 font-bold text-sky-400">Category</th>
                <th class="p-2.5 font-bold text-slate-300">Disk Size</th>
                <th class="p-2.5 font-bold text-purple-400">Shannon Entropy</th>
                <th class="p-2.5 font-bold text-emerald-400">Potential Savings</th>
                <th class="p-2.5 font-bold text-amber-300">SRE Verdict & Reason</th>
              </tr>
            </thead>
            <tbody id="interactiveFileTableBody" class="divide-y divide-cyber-border bg-[#0b101c]">
              <!-- Dynamically populated by JS from /api/filesystem/inventory -->
              <tr class="text-slate-500 text-center py-4">
                <td colspan="7" class="p-4">// Loading real files from hard drive...</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Real-Time Execution Log Box (Shows HOW it is Zipped!) -->
        <div id="executionPipelineTerminal" class="hidden font-mono text-xs p-3.5 rounded-lg bg-[#070b14] border border-emerald-500/40 space-y-1">
          <div class="flex justify-between text-emerald-400 font-bold border-b border-slate-800 pb-1">
            <span>// Live SRE Compression Execution Stream (Physical Hard Drive)</span>
            <span class="text-sky-300">VERIFIED SHA-256</span>
          </div>
          <div id="pipelineStreamLog" class="text-slate-300 space-y-0.5 pt-1"></div>
        </div>

      </div>

    </div>

    <!-- ========================================================================= -->
    <!-- TAB 2: STUCK WORKER (KERNEL RAM RECOVERY) -->
    <!-- ========================================================================= -->
    <div id="mainView-worker" class="hidden space-y-6">
      <div class="bg-[#0f172a] border border-cyber-border rounded-xl p-5 shadow-lg space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-cyber-border">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-lg bg-purple-500/20 border border-purple-500/30 flex items-center justify-center">
              <i data-lucide="cpu" class="w-4 h-4 text-purple-400"></i>
            </div>
            <div>
              <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono">Linux Kernel Process Table & Celery Worker Pool</h2>
              <p class="text-xs text-slate-400">Where this operates: <strong>Volatile RAM Memory & Kernel Process Scheduler (/proc)</strong>. NOT on the hard disk!</p>
            </div>
          </div>
          <span id="workerStatusBadge" class="px-2.5 py-1 rounded text-xs font-mono font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">WORKER-03 DEADLOCKED</span>
        </div>

        <!-- Worker Processes Table -->
        <div class="space-y-2 font-mono text-xs">
          <div class="flex items-center justify-between p-3 rounded-lg bg-[#070b14] border border-cyber-border">
            <span class="text-white font-bold">celery@worker-01 (PID: 19400)</span>
            <span class="text-emerald-400 font-semibold">Heartbeat: 2s ago | CPU 1.9% [RUNNING]</span>
          </div>
          <div class="flex items-center justify-between p-3 rounded-lg bg-[#070b14] border border-cyber-border">
            <span class="text-white font-bold">celery@worker-02 (PID: 19401)</span>
            <span class="text-emerald-400 font-semibold">Heartbeat: 2s ago | CPU 1.8% [RUNNING]</span>
          </div>
          <div id="worker3Container" class="flex items-center justify-between p-3.5 rounded-lg bg-rose-950/30 border border-rose-500/40">
            <div>
              <span id="worker3Name" class="text-white font-bold block">celery@worker-03 (PID: 18294)</span>
              <span id="worker3Detail" class="text-[11px] text-rose-400">Thread locked on socket wait. CPU 0.0% (RAM Deadlock for 240s)</span>
            </div>
            <span id="worker3Pill" class="px-2.5 py-1 rounded text-xs font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">DEADLOCKED</span>
          </div>
        </div>

        <!-- Restart Action -->
        <div class="pt-2">
          <button onclick="interactiveSolveWorker()" class="w-full py-3 px-4 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-mono text-xs font-bold shadow-lg shadow-purple-600/30 transition flex items-center justify-center gap-2">
            <i data-lucide="refresh-cw" class="w-4 h-4"></i>
            <span>⚡ Gracefully Restart Stuck Worker (SIGTERM + 10s Task Drain)</span>
          </button>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- TAB 3: QUEUE CONSUMER AUTOSCALING -->
    <!-- ========================================================================= -->
    <div id="mainView-queue" class="hidden space-y-6">
      <div class="bg-[#0f172a] border border-cyber-border rounded-xl p-5 shadow-lg space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-cyber-border">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-lg bg-amber-500/20 border border-amber-500/30 flex items-center justify-center">
              <i data-lucide="layers" class="w-4 h-4 text-amber-400"></i>
            </div>
            <div>
              <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono">Distributed Network Streaming & Kubernetes Pod Compute</h2>
              <p class="text-xs text-slate-400">Where this operates: <strong>TCP Network Socket Buffers & Container Memory (cgroups)</strong>. NOT on the hard disk!</p>
            </div>
          </div>
          <span id="queueBadge" class="px-2.5 py-1 rounded text-xs font-mono font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">48,250 MSGS BACKLOG</span>
        </div>

        <!-- Pod Grid -->
        <div class="space-y-3 font-mono text-xs">
          <div class="flex justify-between bg-[#070b14] p-3 rounded-lg border border-cyber-border">
            <span>Ingress Traffic: <strong>850 msg/s</strong></span>
            <span id="queueDrainRate" class="text-amber-400 font-bold">Drain Capacity: 250 msg/s (LAGGING)</span>
          </div>

          <div id="queuePodsGrid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2.5">
            <div class="p-3 rounded-lg bg-[#070b14] border border-cyber-border text-center"><i data-lucide="box" class="w-5 h-5 mx-auto text-sky-400 mb-1"></i>pod-1<span class="block text-[10px] text-emerald-400">Running</span></div>
            <div class="p-3 rounded-lg bg-[#070b14] border border-cyber-border text-center"><i data-lucide="box" class="w-5 h-5 mx-auto text-sky-400 mb-1"></i>pod-2<span class="block text-[10px] text-emerald-400">Running</span></div>
            <div class="p-3 rounded-lg bg-[#070b14] border border-cyber-border text-center"><i data-lucide="box" class="w-5 h-5 mx-auto text-sky-400 mb-1"></i>pod-3<span class="block text-[10px] text-emerald-400">Running</span></div>
          </div>
        </div>

        <!-- Auto-scale Action -->
        <div class="pt-2 flex gap-3">
          <button onclick="interactiveSolveQueue()" class="flex-1 py-3 px-4 rounded-xl bg-amber-600 hover:bg-amber-500 text-white font-mono text-xs font-bold shadow-lg shadow-amber-600/30 transition flex items-center justify-center gap-2">
            <i data-lucide="trending-up" class="w-4 h-4"></i>
            <span>⚡ Autoscale Deployment (+3 Pod Replicas to 6)</span>
          </button>
          <button onclick="interactiveScaleDownQueue()" class="py-3 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-mono text-xs font-bold transition flex items-center justify-center gap-2">
            <i data-lucide="trending-down" class="w-4 h-4 text-sky-400"></i>
            <span>Scale Down (3 Pods)</span>
          </button>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- TAB 4: EDGE SSL ROTATION -->
    <!-- ========================================================================= -->
    <div id="mainView-ssl" class="hidden space-y-6">
      <div class="bg-[#0f172a] border border-cyber-border rounded-xl p-5 shadow-lg space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-cyber-border">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-lg bg-cyan-500/20 border border-cyan-500/30 flex items-center justify-center">
              <i data-lucide="shield-alert" class="w-4 h-4 text-cyan-400"></i>
            </div>
            <div>
              <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono">Edge Ingress TLS Keystore & Proxy Memory</h2>
              <p class="text-xs text-slate-400">Where this operates: <strong>OpenSSL Cryptographic Keystore & In-Memory Termination Sockets (Nginx)</strong>. NOT on the hard disk!</p>
            </div>
          </div>
          <span id="sslStatusBadge" class="px-2.5 py-1 rounded text-xs font-mono font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">2.0 DAYS REMAINING</span>
        </div>

        <div class="bg-[#070b14] p-4 rounded-lg border border-cyber-border font-mono text-xs space-y-2">
          <div class="flex justify-between"><span class="text-slate-400">Target Domain:</span><span class="text-white font-bold">api.production.internal</span></div>
          <div class="flex justify-between"><span class="text-slate-400">Issuer Authority:</span><span class="text-white">Let's Encrypt Authority X3</span></div>
          <div class="flex justify-between"><span class="text-slate-400">Validity Period:</span><span id="sslExpiryDate" class="text-rose-400 font-bold">Expires in 2.0 Days (Oct 31, 2026)</span></div>
          <div class="flex justify-between"><span class="text-slate-400">TLS Handshake:</span><span id="sslHandshakeState" class="text-rose-400 font-bold">SLA Warning: Expiring &lt; 72 Hours</span></div>
        </div>

        <!-- Rotate Action -->
        <div class="pt-2">
          <button onclick="interactiveSolveSSL()" class="w-full py-3 px-4 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-mono text-xs font-bold shadow-lg shadow-cyan-600/30 transition flex items-center justify-center gap-2">
            <i data-lucide="shield-check" class="w-4 h-4"></i>
            <span>⚡ Rotate Certificate (ACME DNS Challenge + Zero-Downtime Nginx Reload)</span>
          </button>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- TAB 5: ARCHITECTURE MATRIX (WHERE EACH PROBLEM OPERATES) -->
    <!-- ========================================================================= -->
    <div id="mainView-arch" class="hidden space-y-6">
      <div class="bg-[#0f172a] border border-cyber-border rounded-xl p-5 shadow-lg space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-cyber-border">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-lg bg-amber-500/20 border border-amber-500/30 flex items-center justify-center">
              <i data-lucide="brain-circuit" class="w-4 h-4 text-amber-400"></i>
            </div>
            <div>
              <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono">OS Subsystem Architecture Matrix</h2>
              <p class="text-xs text-slate-400">Answers the judge's question: <em>"Are these done in hard disk or somewhere else? How do we see them?"</em></p>
            </div>
          </div>
          <span class="px-2.5 py-1 rounded text-xs font-mono font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">SYSTEMS ARCHITECTURE PROOF</span>
        </div>

        <div class="overflow-x-auto rounded-lg border border-cyber-border">
          <table class="w-full text-left font-mono text-xs border-collapse">
            <thead class="bg-[#070b14] text-slate-300 text-[11px] border-b border-cyber-border">
              <tr>
                <th class="p-3 font-bold text-white">Problem Statement</th>
                <th class="p-3 font-bold text-sky-400">OS Subsystem Layer</th>
                <th class="p-3 font-bold text-amber-300">Physical Medium</th>
                <th class="p-3 font-bold text-rose-300">Why NOT on Hard Disk?</th>
                <th class="p-3 font-bold text-emerald-400">Inspection Command / Tool</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-cyber-border bg-[#0b101c]">
              <tr class="hover:bg-slate-900/50">
                <td class="p-3 font-bold text-white"><span class="px-2 py-0.5 rounded text-[10px] bg-rose-500/20 text-rose-300 border border-rose-500/30">1. Full Disk</span></td>
                <td class="p-3 text-sky-300 font-semibold">Storage Filesystem (ext4/xfs Inodes)</td>
                <td class="p-3 text-amber-200">Hard Disk / NVMe SSD Sectors</td>
                <td class="p-3 text-slate-400 text-[11px]"><strong>N/A:</strong> This problem DOES live on physical hard disk blocks.</td>
                <td class="p-3 text-emerald-300">Windows File Explorer, df -h, ls -lh</td>
              </tr>
              <tr class="hover:bg-slate-900/50">
                <td class="p-3 font-bold text-white"><span class="px-2 py-0.5 rounded text-[10px] bg-purple-500/20 text-purple-300 border border-purple-500/30">2. Stuck Worker</span></td>
                <td class="p-3 text-sky-300 font-semibold">Operating System RAM & Kernel Scheduler (/proc)</td>
                <td class="p-3 text-purple-200">Volatile RAM Memory (Heap & Registers)</td>
                <td class="p-3 text-slate-400 text-[11px]"><strong>Deadlock is NOT on disk!</strong> It is a stalled thread mutex in RAM. Deleting files does nothing.</td>
                <td class="p-3 text-emerald-300">ps aux | grep celery, top, /proc/&lt;pid&gt;/status</td>
              </tr>
              <tr class="hover:bg-slate-900/50">
                <td class="p-3 font-bold text-white"><span class="px-2 py-0.5 rounded text-[10px] bg-amber-500/20 text-amber-300 border border-amber-500/30">3. Queue Lag</span></td>
                <td class="p-3 text-sky-300 font-semibold">Distributed Streaming Broker & K8s Pods</td>
                <td class="p-3 text-amber-200">TCP Network Sockets & Container cgroups</td>
                <td class="p-3 text-slate-400 text-[11px]"><strong>Backlogs are in-flight network packets</strong>, not stored local files. Disk cleanup cannot scale worker pools.</td>
                <td class="p-3 text-emerald-300">kubectl get pods, kafka-consumer-groups.sh</td>
              </tr>
              <tr class="hover:bg-slate-900/50">
                <td class="p-3 font-bold text-white"><span class="px-2 py-0.5 rounded text-[10px] bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">4. SSL Expiry</span></td>
                <td class="p-3 text-sky-300 font-semibold">Cryptographic Keystore & Proxy Memory</td>
                <td class="p-3 text-cyan-200">OpenSSL In-Memory TLS Sockets (Nginx)</td>
                <td class="p-3 text-slate-400 text-[11px]"><strong>Certs are cryptographic public keys in RAM</strong> verified during TLS handshakes. Disk storage is unaffected.</td>
                <td class="p-3 text-emerald-300">openssl x509 -text, openssl s_client, nginx -s reload</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- TAB 6: ITIL CHANGE RECORDS & COMPLETE AUDIT TRAIL -->
    <!-- ========================================================================= -->
    <div id="mainView-audit" class="hidden space-y-6">
      <div class="bg-[#0f172a] border border-cyber-border rounded-xl p-5 shadow-lg space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-cyber-border">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center">
              <i data-lucide="file-check-2" class="w-4 h-4 text-emerald-400"></i>
            </div>
            <div>
              <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono">ITIL Change Records & Complete Audit Trail</h2>
              <p class="text-xs text-slate-400">Problem Statement Requirement: <em>"Make every action, decision, and outcome visible after the fact."</em></p>
            </div>
          </div>
          
          <div class="flex items-center gap-2">
            <a href="/api/export-audit?format=csv" download class="px-3 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 font-mono text-xs font-bold transition flex items-center gap-1.5">
              <i data-lucide="download" class="w-3.5 h-3.5 text-sky-400"></i> Export CSV
            </a>
            <a href="/api/export-audit?format=json" download class="px-3 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 font-mono text-xs font-bold transition flex items-center gap-1.5">
              <i data-lucide="code" class="w-3.5 h-3.5 text-emerald-400"></i> Export JSON
            </a>
          </div>
        </div>

        <div class="overflow-x-auto rounded-lg border border-cyber-border">
          <table class="w-full text-left font-mono text-xs border-collapse">
            <thead class="bg-[#070b14] text-slate-400 text-[11px] border-b border-cyber-border">
              <tr>
                <th class="p-2.5">Change ID</th>
                <th class="p-2.5">Timestamp</th>
                <th class="p-2.5">Incident Title</th>
                <th class="p-2.5">Actor</th>
                <th class="p-2.5">Command Executed</th>
                <th class="p-2.5">Outcome</th>
              </tr>
            </thead>
            <tbody id="auditTableBody" class="divide-y divide-cyber-border bg-[#0b101c]">
              <tr class="text-slate-500 text-center py-4">
                <td colspan="6" class="p-4">// Loading ITIL change records...</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

  </main>

  <!-- TOAST NOTIFICATION CONTAINER -->
  <div id="toastContainer" class="fixed bottom-5 right-5 z-50 flex flex-col gap-2 pointer-events-none"></div>

  <!-- JAVASCRIPT APPLICATION SCRIPT -->
  <script src="/static/js/app.js?v=20261029_0200"></script>
</body>
</html>
"""

with open(index_path, "w", encoding="utf-8") as f:
    f.write(new_html)

print("Successfully written clean, modern, real-world templates/index.html!")

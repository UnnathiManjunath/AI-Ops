import os

INDEX_PATH = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\templates\index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    text = f.read()

start_marker = '<!-- Section 2: Interactive Fault Injector Sandbox'
end_marker = '<!-- Section 3: Active Incident Remediation Console'

p1 = text.find(start_marker)
p2 = text.find(end_marker)

new_section_2 = """<!-- Section 2: Interactive Fault Injector Sandbox (Figure 3: "How do we demonstrate?") -->
    <div class="bg-cyber-card border border-cyber-border rounded-xl p-5 shadow-lg">
      <div class="flex flex-wrap items-center justify-between gap-3 mb-3 pb-3 border-b border-cyber-border">
        <div>
          <h2 class="text-base font-semibold text-white flex items-center gap-2">
            <i data-lucide="flask-conical" class="w-5 h-5 text-sky-400"></i>
            Interactive Fault Injector Sandbox (Distinct Enterprise Telemetry)
          </h2>
          <p class="text-xs text-slate-400">Contrast realistic Critical Disasters vs Routine Uncritical Maintenance with distinctive metrics across all 4 Subsystems</p>
        </div>
        
        <!-- Filter Pills to impress Judges -->
        <div class="flex items-center gap-1.5 bg-[#070b14] p-1 rounded-lg border border-cyber-border">
          <button id="filterBtn-all" onclick="filterScenarioCards('all')" class="px-2.5 py-1 rounded text-xs font-semibold font-mono bg-sky-600 text-white transition">
            ⚡ All (12 Scenarios)
          </button>
          <button id="filterBtn-uncritical" onclick="filterScenarioCards('uncritical')" class="px-2.5 py-1 rounded text-xs font-semibold font-mono text-emerald-400 hover:bg-emerald-500/20 transition">
            🟢 Uncritical Routine (4)
          </button>
          <button id="filterBtn-critical" onclick="filterScenarioCards('critical')" class="px-2.5 py-1 rounded text-xs font-semibold font-mono text-rose-400 hover:bg-rose-500/20 transition">
            🔴 Critical Emergency (8)
          </button>
        </div>
      </div>

      <!-- Judge Pitch Tip Banner -->
      <div class="mb-4 p-2.5 rounded-lg bg-indigo-950/40 border border-indigo-500/30 flex items-center justify-between text-xs text-indigo-200">
        <div class="flex items-center space-x-2">
          <i data-lucide="sparkles" class="w-4 h-4 text-indigo-400 flex-shrink-0"></i>
          <span><strong>Judge Demonstration Tip:</strong> Notice each problem has <em>completely distinct numbers and impact metrics</em>! Compare an Uncritical scenario (resolved silently in 0.8s) vs a Critical high-risk scenario (freezes at Human Gate)!</span>
        </div>
      </div>

      <!-- Quick Action Injector Buttons -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
        
        <!-- Fault 1: Disk Storage -->
        <div class="bg-[#0b101c] border border-cyber-border rounded-lg p-3 hover:border-sky-500/40 transition">
          <div class="flex items-center justify-between mb-2">
            <span class="font-bold text-sm text-slate-200 flex items-center gap-1.5">
              <i data-lucide="hard-drive" class="w-4 h-4 text-sky-400"></i> 1. Storage Exhaustion
            </span>
            <span class="text-[10px] font-mono text-slate-400">Postgres / Cache</span>
          </div>
          <p class="text-xs text-slate-400 mb-2.5">Docker builds vs Nginx cache vs Postgres WAL</p>
          <div class="space-y-1.5">
            <button onclick="injectFault('disk_overflow', 'routine_hygiene')" class="scenario-btn scenario-uncritical w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-emerald-600/20 hover:text-emerald-300 border border-emerald-500/30 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🟢 Dev Build Scratch (54.2%)</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>
            </button>
            <button onclick="injectFault('disk_overflow', 'logs')" class="scenario-btn scenario-standard w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-sky-600/20 hover:text-sky-300 border border-slate-700 hover:border-sky-500/50 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🟡 Nginx Static Cache (88.5%)</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-sky-500/10 text-sky-400 font-mono">Safe Tier 1</span>
            </button>
            <button onclick="injectFault('disk_overflow', 'core_dump')" class="scenario-btn scenario-critical w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-rose-600/20 hover:text-rose-300 border border-rose-500/40 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🔴 Postgres WAL Full (99.4%)</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">124MB Left!</span>
            </button>
          </div>
        </div>

        <!-- Fault 2: Background Worker Stuck -->
        <div class="bg-[#0b101c] border border-cyber-border rounded-lg p-3 hover:border-purple-500/40 transition">
          <div class="flex items-center justify-between mb-2">
            <span class="font-bold text-sm text-slate-200 flex items-center gap-1.5">
              <i data-lucide="cpu" class="w-4 h-4 text-purple-400"></i> 2. Process Threadlock
            </span>
            <span class="text-[10px] font-mono text-slate-400">Fintech / Celery</span>
          </div>
          <p class="text-xs text-slate-400 mb-2.5">Image GC vs Email timeout vs $1.4M Recon lock</p>
          <div class="space-y-1.5">
            <button onclick="injectFault('worker_stuck', 'routine_gc_trim')" class="scenario-btn scenario-uncritical w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-emerald-600/20 hover:text-emerald-300 border border-emerald-500/30 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🟢 Image Worker GC (15k Tasks)</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>
            </button>
            <button onclick="injectFault('worker_stuck', 'deadlock_clean')" class="scenario-btn scenario-standard w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-sky-600/20 hover:text-sky-300 border border-slate-700 hover:border-sky-500/50 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🟡 Email Worker Hung (310s)</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-sky-500/10 text-sky-400 font-mono">Safe Tier 1</span>
            </button>
            <button onclick="injectFault('worker_stuck', 'db_exhaustion')" class="scenario-btn scenario-critical w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-rose-600/20 hover:text-rose-300 border border-rose-500/40 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🔴 Payment Recon Lock (8.4k Trans)</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">$1.42M Risk</span>
            </button>
          </div>
        </div>

        <!-- Fault 3: Growing Queue -->
        <div class="bg-[#0b101c] border border-cyber-border rounded-lg p-3 hover:border-amber-500/40 transition">
          <div class="flex items-center justify-between mb-2">
            <span class="font-bold text-sm text-slate-200 flex items-center gap-1.5">
              <i data-lucide="layers" class="w-4 h-4 text-amber-400"></i> 3. Stream Queue Lag
            </span>
            <span class="text-[10px] font-mono text-slate-400">Kafka Backlog</span>
          </div>
          <p class="text-xs text-slate-400 mb-2.5">Clickstream vs Flash Sale vs Fraud Poison Pill</p>
          <div class="space-y-1.5">
            <button onclick="injectFault('queue_growth', 'routine_queue_balance')" class="scenario-btn scenario-uncritical w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-emerald-600/20 hover:text-emerald-300 border border-emerald-500/30 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🟢 Clickstream Ripple (850 msgs)</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>
            </button>
            <button onclick="injectFault('queue_growth', 'traffic_surge')" class="scenario-btn scenario-standard w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-sky-600/20 hover:text-sky-300 border border-slate-700 hover:border-sky-500/50 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🟡 Flash Sale Surge (28.5k msgs)</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-400 font-mono">Scale 4➔8</span>
            </button>
            <button onclick="injectFault('queue_growth', 'poison_pill')" class="scenario-btn scenario-critical w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-rose-600/20 hover:text-rose-300 border border-rose-500/40 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🔴 Fraud Poison Pill (142.8k msgs)</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">92.4% Err!</span>
            </button>
          </div>
        </div>

        <!-- Fault 4: Outdated Certificate -->
        <div class="bg-[#0b101c] border border-cyber-border rounded-lg p-3 hover:border-emerald-500/40 transition">
          <div class="flex items-center justify-between mb-2">
            <span class="font-bold text-sm text-slate-200 flex items-center gap-1.5">
              <i data-lucide="lock" class="w-4 h-4 text-emerald-400"></i> 4. SSL Key Rotation
            </span>
            <span class="text-[10px] font-mono text-slate-400">Edge Gateway</span>
          </div>
          <p class="text-xs text-slate-400 mb-2.5">Internal mTLS vs Portal renew vs CA Revocation</p>
          <div class="space-y-1.5">
            <button onclick="injectFault('ssl_expiry', 'routine_audit_check')" class="scenario-btn scenario-uncritical w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-emerald-600/20 hover:text-emerald-300 border border-emerald-500/30 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🟢 Internal mTLS Audit (58.0 Days)</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>
            </button>
            <button onclick="injectFault('ssl_expiry', 'routine_renew')" class="scenario-btn scenario-standard w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-sky-600/20 hover:text-sky-300 border border-slate-700 hover:border-sky-500/50 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🟡 Portal TLS Expiry (4.5 Days)</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Safe Tier 1</span>
            </button>
            <button onclick="injectFault('ssl_expiry', 'root_ca_broken')" class="scenario-btn scenario-critical w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-rose-600/20 hover:text-rose-300 border border-rose-500/40 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🔴 Root CA Revocation (6 Hours!)</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">CRL Drift!</span>
            </button>
          </div>
        </div>

      </div>
    </div>

    """

if p1 != -1 and p2 != -1:
    updated = text[:p1] + new_section_2 + text[p2:]
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(updated)
    print("templates/index.html updated successfully with distinct enterprise scenario cards!")
else:
    print(f"Markers not found in index.html: p1={p1}, p2={p2}")

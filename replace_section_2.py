import os

INDEX_PATH = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\templates\index.html"

new_section_2 = """<!-- Section 2: Interactive Fault Injector Sandbox (Figure 3: "How do we demonstrate?") -->
    <div class="bg-cyber-card border border-cyber-border rounded-xl p-5 shadow-lg">
      <div class="flex flex-wrap items-center justify-between gap-3 mb-3 pb-3 border-b border-cyber-border">
        <div>
          <h2 class="text-base font-semibold text-white flex items-center gap-2">
            <i data-lucide="flask-conical" class="w-5 h-5 text-sky-400"></i>
            Interactive Fault Injector Sandbox
          </h2>
          <p class="text-xs text-slate-400">Demonstrate Uncritical Routine Maintenance vs Critical High-Risk Emergencies across all 4 Core Subsystems</p>
        </div>
        
        <!-- Filter Pills to impress Judges -->
        <div class="flex items-center gap-1.5 bg-[#070b14] p-1 rounded-lg border border-cyber-border">
          <button id="filterBtn-all" onclick="filterScenarioCards('all')" class="px-2.5 py-1 rounded text-xs font-semibold font-mono bg-sky-600 text-white transition">
            ⚡ All (12)
          </button>
          <button id="filterBtn-uncritical" onclick="filterScenarioCards('uncritical')" class="px-2.5 py-1 rounded text-xs font-semibold font-mono text-emerald-400 hover:bg-emerald-500/20 transition">
            🟢 Uncritical / Routine (4)
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
          <span><strong>Judge Demonstration Tip:</strong> Trigger a <span class="text-emerald-400 font-bold">🟢 Uncritical Routine</span> scenario to show 100% silent safe auto-heal (zero engineer disturbance), then trigger a <span class="text-rose-400 font-bold">🔴 Critical</span> scenario to show the safety gate halt!</span>
        </div>
      </div>

      <!-- Quick Action Injector Buttons -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
        
        <!-- Fault 1: Disk Overflow -->
        <div class="bg-[#0b101c] border border-cyber-border rounded-lg p-3 hover:border-sky-500/40 transition">
          <div class="flex items-center justify-between mb-2">
            <span class="font-bold text-sm text-slate-200 flex items-center gap-1.5">
              <i data-lucide="hard-drive" class="w-4 h-4 text-sky-400"></i> 1. Disk Storage
            </span>
            <span class="text-[10px] font-mono text-slate-400">/dev/sda1</span>
          </div>
          <p class="text-xs text-slate-400 mb-2.5">Storage hygiene vs catastrophic core dump</p>
          <div class="space-y-1.5">
            <button onclick="injectFault('disk_overflow', 'routine_hygiene')" class="scenario-btn scenario-uncritical w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-emerald-600/20 hover:text-emerald-300 border border-emerald-500/30 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🟢 Routine /tmp & Logs (62%)</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>
            </button>
            <button onclick="injectFault('disk_overflow', 'logs')" class="scenario-btn scenario-standard w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-sky-600/20 hover:text-sky-300 border border-slate-700 hover:border-sky-500/50 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🟡 App Logs Overflow (94%)</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-sky-500/10 text-sky-400 font-mono">Safe Tier 1</span>
            </button>
            <button onclick="injectFault('disk_overflow', 'core_dump')" class="scenario-btn scenario-critical w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-rose-600/20 hover:text-rose-300 border border-rose-500/40 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🔴 MySQL Core Dumps (96%)</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">Tier 3 Gate</span>
            </button>
          </div>
        </div>

        <!-- Fault 2: Background Worker Stuck -->
        <div class="bg-[#0b101c] border border-cyber-border rounded-lg p-3 hover:border-purple-500/40 transition">
          <div class="flex items-center justify-between mb-2">
            <span class="font-bold text-sm text-slate-200 flex items-center gap-1.5">
              <i data-lucide="cpu" class="w-4 h-4 text-purple-400"></i> 2. Worker Threads
            </span>
            <span class="text-[10px] font-mono text-slate-400">Worker-03</span>
          </div>
          <p class="text-xs text-slate-400 mb-2.5">Memory trim vs DB saturation deadlock</p>
          <div class="space-y-1.5">
            <button onclick="injectFault('worker_stuck', 'routine_gc_trim')" class="scenario-btn scenario-uncritical w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-emerald-600/20 hover:text-emerald-300 border border-emerald-500/30 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🟢 Soft Heap Memory Trim</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>
            </button>
            <button onclick="injectFault('worker_stuck', 'deadlock_clean')" class="scenario-btn scenario-standard w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-sky-600/20 hover:text-sky-300 border border-slate-700 hover:border-sky-500/50 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🟡 Soft Thread Deadlock</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-sky-500/10 text-sky-400 font-mono">Safe Tier 1</span>
            </button>
            <button onclick="injectFault('worker_stuck', 'db_exhaustion')" class="scenario-btn scenario-critical w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-rose-600/20 hover:text-rose-300 border border-rose-500/40 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🔴 DB Pool Saturated (99%)</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">Tier 3 Gate</span>
            </button>
          </div>
        </div>

        <!-- Fault 3: Growing Queue -->
        <div class="bg-[#0b101c] border border-cyber-border rounded-lg p-3 hover:border-amber-500/40 transition">
          <div class="flex items-center justify-between mb-2">
            <span class="font-bold text-sm text-slate-200 flex items-center gap-1.5">
              <i data-lucide="layers" class="w-4 h-4 text-amber-400"></i> 3. Growing Queue
            </span>
            <span class="text-[10px] font-mono text-slate-400">Kafka Orders</span>
          </div>
          <p class="text-xs text-slate-400 mb-2.5">Minor balancing vs poison pill crash</p>
          <div class="space-y-1.5">
            <button onclick="injectFault('queue_growth', 'routine_queue_balance')" class="scenario-btn scenario-uncritical w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-emerald-600/20 hover:text-emerald-300 border border-emerald-500/30 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🟢 Off-Peak Ripple (420)</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>
            </button>
            <button onclick="injectFault('queue_growth', 'traffic_surge')" class="scenario-btn scenario-standard w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-sky-600/20 hover:text-sky-300 border border-slate-700 hover:border-sky-500/50 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🟡 Traffic Spike (48k msgs)</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-400 font-mono">Tier 2 Scale</span>
            </button>
            <button onclick="injectFault('queue_growth', 'poison_pill')" class="scenario-btn scenario-critical w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-rose-600/20 hover:text-rose-300 border border-rose-500/40 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🔴 Poison Pill Crash (68%)</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">Tier 3 Gate</span>
            </button>
          </div>
        </div>

        <!-- Fault 4: Outdated Certificate -->
        <div class="bg-[#0b101c] border border-cyber-border rounded-lg p-3 hover:border-emerald-500/40 transition">
          <div class="flex items-center justify-between mb-2">
            <span class="font-bold text-sm text-slate-200 flex items-center gap-1.5">
              <i data-lucide="lock" class="w-4 h-4 text-emerald-400"></i> 4. SSL Certificate
            </span>
            <span class="text-[10px] font-mono text-slate-400">api-edge</span>
          </div>
          <p class="text-xs text-slate-400 mb-2.5">Proactive audit vs Root CA revocation</p>
          <div class="space-y-1.5">
            <button onclick="injectFault('ssl_expiry', 'routine_audit_check')" class="scenario-btn scenario-uncritical w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-emerald-600/20 hover:text-emerald-300 border border-emerald-500/30 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🟢 45-Day Health Audit</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>
            </button>
            <button onclick="injectFault('ssl_expiry', 'routine_renew')" class="scenario-btn scenario-standard w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-sky-600/20 hover:text-sky-300 border border-slate-700 hover:border-sky-500/50 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🟡 Auto-Renew (&lt; 3 Days)</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Safe Tier 1</span>
            </button>
            <button onclick="injectFault('ssl_expiry', 'root_ca_broken')" class="scenario-btn scenario-critical w-full text-left px-2.5 py-1.5 rounded bg-slate-800/80 hover:bg-rose-600/20 hover:text-rose-300 border border-rose-500/40 text-xs font-medium text-slate-300 flex items-center justify-between transition">
              <span class="flex items-center gap-1.5">🔴 Root CA Revocation</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">Tier 3 Gate</span>
            </button>
          </div>
        </div>

      </div>
    </div>

    """

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = '<!-- Section 2: Interactive Fault Injector Sandbox'
end_marker = '<!-- Section 3: Active Incident Remediation Console'

p1 = content.find(start_marker)
p2 = content.find(end_marker)

if p1 != -1 and p2 != -1:
    updated = content[:p1] + new_section_2 + content[p2:]
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(updated)
    print("Section 2 successfully updated in index.html!")
else:
    print(f"Error locating markers: p1={p1}, p2={p2}")

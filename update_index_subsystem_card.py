import re

index_path = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\templates\index.html"

with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Replace the existing subsystemProofCard with the enhanced multi-layer subsystem inspector
new_card_html = '''        <!-- Subsystem State Inspector & File Proof Box (Multi-Layer OS & Hard Disk Inspector) -->
        <div class="bg-cyber-card border border-cyber-border rounded-xl p-4 shadow-lg" id="subsystemProofCard">
          <div class="flex flex-wrap items-center justify-between gap-2 mb-3 pb-2 border-b border-cyber-border">
            <div class="flex items-center space-x-2">
              <i data-lucide="cpu" class="w-4 h-4 text-sky-400"></i>
              <h4 class="text-xs font-bold text-white uppercase tracking-wider font-mono">Live Subsystem State & OS Architecture Inspector</h4>
            </div>
            <span id="subsystemBadge" class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-sky-300 border border-slate-700">MULTI-LAYER PROBE</span>
          </div>

          <!-- Subsystem Navigation Tabs -->
          <div class="flex flex-wrap items-center gap-1.5 mb-3 p-1 bg-[#070b14] rounded-lg border border-cyber-border text-xs font-mono">
            <button id="tab-subsystem-disk" onclick="switchSubsystemTab('disk')" class="px-2.5 py-1 rounded text-xs font-semibold bg-sky-600 text-white transition flex items-center gap-1.5">
              <i data-lucide="hard-drive" class="w-3.5 h-3.5"></i>
              <span>1. Disk Filesystem & Real .GZ</span>
            </button>
            <button id="tab-subsystem-worker" onclick="switchSubsystemTab('worker')" class="px-2.5 py-1 rounded text-xs font-semibold text-slate-400 hover:text-white transition flex items-center gap-1.5">
              <i data-lucide="activity" class="w-3.5 h-3.5"></i>
              <span>2. Worker Deadlock (Kernel RAM)</span>
            </button>
            <button id="tab-subsystem-queue" onclick="switchSubsystemTab('queue')" class="px-2.5 py-1 rounded text-xs font-semibold text-slate-400 hover:text-white transition flex items-center gap-1.5">
              <i data-lucide="layers" class="w-3.5 h-3.5"></i>
              <span>3. Queue Lag (K8s Network)</span>
            </button>
            <button id="tab-subsystem-ssl" onclick="switchSubsystemTab('ssl')" class="px-2.5 py-1 rounded text-xs font-semibold text-slate-400 hover:text-white transition flex items-center gap-1.5">
              <i data-lucide="shield-check" class="w-3.5 h-3.5"></i>
              <span>4. SSL Keystore (Proxy Memory)</span>
            </button>
            <button id="tab-subsystem-arch" onclick="switchSubsystemTab('arch')" class="px-2.5 py-1 rounded text-xs font-semibold text-amber-400 bg-amber-500/10 border border-amber-500/30 hover:bg-amber-500/20 transition flex items-center gap-1.5">
              <i data-lucide="brain-circuit" class="w-3.5 h-3.5"></i>
              <span>🧠 OS Architecture Matrix</span>
            </button>
          </div>
          
          <div id="subsystemMessage" class="text-xs text-slate-300 mb-3 bg-[#0a0f1d] p-2.5 rounded border border-cyber-border flex items-center justify-between">
            <span>Inspecting real physical storage sectors, kernel memory scheduler, and distributed network queues.</span>
          </div>

          <!-- Dynamic Container for Selected Subsystem View -->
          <div id="subsystemContentList" class="space-y-2 font-mono text-xs">
            <div class="text-center py-4 text-slate-500 text-xs">// Loading physical filesystem & subsystem telemetry...</div>
          </div>
        </div>'''

target_regex = r'<!-- Subsystem State Inspector & File Proof Box[\s\S]*?</div>\s*</div>\s*(?=\s*</div>\s*<!-- Section 4:)'

if re.search(target_regex, html):
    html = re.sub(target_regex, new_card_html + '\n\n        </div>\n', html, count=1)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Successfully updated templates/index.html!")
else:
    print("Regex did not match; inspecting structure...")
    idx = html.find('id="subsystemProofCard"')
    print("subsystemProofCard index:", idx)
    if idx != -1:
        start_idx = html.rfind('<!-- Subsystem State Inspector', 0, idx)
        end_idx = html.find('<!-- Section 4:', idx)
        last_div_idx = html.rfind('</div>', start_idx, end_idx)
        prev_div_idx = html.rfind('</div>', start_idx, last_div_idx)
        print("Slice found:", start_idx, end_idx)
        html = html[:start_idx] + new_card_html + "\n\n      </div>\n\n    </div>\n\n    " + html[end_idx:]
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html)
        print("Successfully updated templates/index.html via slicing!")

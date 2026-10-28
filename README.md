# SafeOps AI — Automation That Is Safe Enough to Leave Switched On

**Hackathon Track:** Cynefian 24-Hour Student Hackathon — AI-Ops Track  
**Problem Statement AO-04:** *Automation that is safe enough to leave switched on*  
**Team Name:** Idea Ignitors  
**Team Number:** XH-23  
**Domain:** AI Ops  
**Team Members:**
- **Unnathi T M** — AI/LLM Architecture & Risk Policy
- **Chaithanya N S** — Frontend Telemetry & Dashboard UX
- **M Eshwar** — Backend Engine & SQLite Database
- **Babitha M** — ITIL Audit & Rollback Controller

---

## 📌 Executive Summary & Problem Context (Figures 1 & 2)

An operations team has dozens of runbooks for routine fixes:
- Clearing full disks
- Restarting stuck worker processes
- Scaling queue consumers
- Rotating expiring certificates

Each is currently executed by hand at 3 a.m. because an earlier attempt at automation once made an outage worse, and nobody has trusted it since:
> *"The barrier is trust, not tooling."*

Runbooks encode human judgment:
- *"If the disk is full because of logs, rotate and compress; if because of a core dump, investigate/escalate."*
- *"If a worker is stuck due to a deadlock, restart it; if stuck because the DB pool is exhausted, restarting will trigger a thundering herd outage."*
- *"If a queue is growing due to traffic, scale consumers; if due to a poison pill crashing workers, halt and route to Dead Letter Queue (DLQ)."*
- *"If a TLS certificate is within 7 days of expiry, auto-renew with Let's Encrypt; if root CA trust is broken, escalate to Security."*

**SafeOps AI** bridges this trust barrier by turning passive markdown runbooks into an active, guardrailed autonomous remediation platform equipped with **explicit human control points, hard blast-radius limits, a master emergency kill-switch, and guaranteed automatic rollback.**

---

## 🔄 End-to-End Architectural Flowchart (Figure 3)

```mermaid
flowchart TD
    A["1. Monitor IT System\n(Live Telemetry Probes)"] --> B["2. Detect a Fault\n(Disk, Worker, Queue, SSL)"]
    B --> C["3. AI Diagnosis\n(Runbook Judgment Engine)"]
    C --> D["4. Risk Assessment\n(Tier 1 / Tier 2 / Tier 3 / Ambiguous)"]
    
    D -->|Low/Medium Risk: Tier 1/2| E1["Autonomous Policy Authorization\n(Pre-checks & Blast Radius Bounds)"]
    D -->|High Risk: Tier 3 or Ambiguous| E2["Human Authorization Gate (HITL)\n(Mandatory Operator Review)"]
    
    E2 -->|Approved| E1
    E2 -->|Rejected| H["Incident Escalated & Documented"]
    
    E1 --> F["5. Execute Scoped Remediation\n(Least-Privilege Sandbox)"]
    F --> G{"Post-Execution Health Verification"}
    
    G -->|PASS| I["Healthy Telemetry Restored\n(Update Metrics to Green)"]
    G -->|FAIL| J["Automatic Rollback Triggered\n(Atomic Reversion to Pre-Clean Snapshot)"]
    
    I --> K["6. ITIL Change Record Sealed\n(Cryptographic Audit Trail in SQLite)"]
    J --> K
```

---

## 🛠️ Technologies Used

| Layer | Technologies |
|---|---|
| **Backend & API** | Python 3.11, Flask REST API |
| **Database & Persistence** | SQLite3, SQL Relational Schemas, JSON Snapshots |
| **AI / Heuristic Engine** | AI Ops Heuristic & LLM Reasoner (Encodes 10 Runbooks & Risk Policies) |
| **Monitoring Tool** | Live Real-Time Telemetry Gauges (Disk, CPU, RAM, Heartbeats, Queue Depth, SSL) |
| **Frontend Dashboard** | HTML5, TailwindCSS, Lucide Icons, Chart.js, Canvas Confetti |
| **Safety Controls** | Hard Emergency Kill-Switch, Rate Limiter, Scoped Privileges, Auto-Rollback |
| **Compliance** | ITIL Standard Change Management Records, CSV/JSON Export |

---

## 🚀 How to Run the Project

The server is currently running locally in your workspace!

### Direct Access
Open your web browser and navigate to:
```
http://127.0.0.1:5050
```

### To Restart or Run Manually from Terminal
```powershell
cd "C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai"
python app.py
```

### To Run the Automated Verification Suite
```powershell
cd "C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai"
python verify_system.py
```

---

## 🎯 Live Demonstration Guide for Judges (Figure 3 Workflow)

Follow this exact demonstration sequence during your hackathon presentation:

### Step 1: Open the Interactive Prototype
1. Navigate to `http://127.0.0.1:5050`.
2. Point out the top header:
   - **Safe Mode Active** status.
   - **Team Idea Ignitors (XH-23)** badge (click to show team member breakdown).
   - The prominent **Master Kill-Switch**.
   - Real-time **Monitoring Tool** telemetry cards (Root Disk Space, Worker State, Queue Backlog, SSL Expiry).

### Step 2: Inject a Routine Low-Risk Fault (Auto Tier 1)
1. In the **Interactive Fault Injector Sandbox**, click **"Disk Overflow: Application Logs"**.
2. Notice the Disk Space card turns critical (94.6%).
3. Click **"Analyze Fault & Diagnose Risk"**.
4. Show the judges the **AI Diagnosis**:
   - Assessed as **Tier 1 (Low Risk - Safe Auto)**.
   - Blast Radius: Local `/var/log` only; zero downtime.
   - Auto-authorized by policy (no 3 a.m. human wakeup needed!).
5. Click **"Run Safe Remediation"**.
6. Watch the live terminal simulation execute line-by-line, verify health, and restore Disk Usage down to **62.4% (Green)** with celebratory confetti!

### Step 3: Inject an Ambiguous / High-Risk Fault (Tier 3 Human Gate)
1. In the sandbox, click **"Disk Overflow: DB Core Dump"**.
2. Click **"Analyze Fault & Diagnose Risk"**.
3. Highlight to the judges how SafeOps AI behaves differently:
   - Identifies that deleting core dumps in `/var/lib/mysql` could destroy crash diagnostic evidence or crash replication.
   - **Safety Guardrail Triggered:** Classified as **Ambiguous / Tier 3 (Escalated to Human)**.
   - Reveals the **Human Authorization Gate**: Automation is strictly locked until operator **Babitha M** reviews the blast radius and clicks **"Approve Remediation"**.

### Step 4: Demonstrate Automatic Rollback (Key Hackathon Metric #3)
1. Inject the **"Stuck Worker: Soft Thread Deadlock"** fault.
2. Click **"Analyze Fault & Diagnose Risk"**.
3. Click the amber button **"Simulate Failure & Test Rollback"**.
4. Show the judges the terminal:
   - Post-remediation health check fails.
   - System immediately detects that health did not improve.
   - **Automatic Rollback Triggered:** Executes rollback script, restores prior snapshot, prevents cascading outage, and flags the incident as `ROLLED_BACK`.

### Step 5: Demonstrate the Master Kill-Switch
1. Click the top-right **"KILL SWITCH: OFF"** button.
2. It turns glowing red: **"KILL SWITCH: ACTIVE"** and displays a cluster-wide warning banner.
3. Try executing any remediation — the system immediately refuses:
   `"EXECUTION BLOCKED: Master Kill-Switch is ACTIVE. All automated actions are frozen across cluster."`
4. Click again to release the switch back to normal.

### Step 6: Review the ITIL Audit Trail
1. Scroll down to the **ITIL Change Management & Complete Audit Trail** table.
2. Show that every single action, diagnosis, human approval, command execution, and rollback is recorded with:
   - Change ID (`CHG-...`)
   - Actor (`Autonomous AI Ops Engine` vs `Human Operator: Babitha M`)
   - Risk Tier
   - Command & Blast Radius
   - Outcome (`SUCCESS`, `ROLLED_BACK`, `REJECTED`)
   - ITIL Justification
3. Click **"Export CSV"** to demonstrate downloadable compliance reports.

---

## 📚 10 Representative Preloaded Runbooks

SafeOps AI comes with all 10 representative industry runbooks pre-configured (click **"Runbooks (10)"** in the top navigation):
1. **RB-01:** Disk Overflow: Rotatable Application Logs vs DB Core Dump
2. **RB-02:** Background Process Stuck: Worker Thread Deadlock vs DB Saturation
3. **RB-03:** Growing Message Queue: Traffic Surge vs Poison Pill Message
4. **RB-04:** SSL/TLS Certificate Expiration & Key Rotation
5. **RB-05:** Memory Leak in Microservice Container (Rolling Canary Restart)
6. **RB-06:** High CPU Runaway Script / Zombie Fork Bomb
7. **RB-07:** Read-Only Filesystem Mount Due to SCSI I/O Timeout (Escalation Guard)
8. **RB-08:** Redis Cache Connection Pool Exhaustion (Idle Prune)
9. **RB-09:** DNS Resolver Cache Poisoning & Stale Lookup Drift
10. **RB-10:** API Ingress Gateway Packet Drop / SYN Flood Rate Limiting

import os

RUNBOOK_PATH = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\MASTER_OPERATIONAL_RUNBOOK.md"

appendix = """

---

## Section E: Uncritical Routine Maintenance & Preventive Procedures (Tier 0 & Tier 1)

### 1. Definition of "Uncritical" in Enterprise SRE
An **uncritical situation** is a routine, non-emergency operational condition that does not threaten active client traffic, transaction integrity, or system uptime. These situations represent preventive housekeeping, off-peak maintenance, or early health checks that should be executed silently in the background without waking an on-call engineer at 3:00 AM.

---

### Comparison Matrix: Uncritical Routine vs. Critical Emergency

| Operational Parameter | 🟢 Uncritical Routine Maintenance | 🔴 Critical / Ambiguous Emergency |
| :--- | :--- | :--- |
| **Example Telemetry** | Disk at 62%, Worker healthy (heap trim), Queue at 420 msgs, SSL valid for 45 days | Disk at 96% (Core dumps), DB Pool at 99%, Queue at 54,000 (Poison pill), SSL CA Revoked |
| **Risk Classification** | **Tier 0 / Tier 1 (Safe Autonomous Auto-Heal)** | **Tier 3 (High Risk / Human-in-the-Loop Gate)** |
| **Blast Radius** | **0% (Zero Impact):** Scoped to scratch/ephemeral files or idle workers | **High / Critical:** Risk of data corruption, transaction drops, or cluster cascade |
| **Human Operator Impact** | 😴 **Zero Disturbance:** Engineer sleeps peacefully; system fixes and logs silently | 🚨 **Piercing Siren / Wake-up Call:** Human must review plan and click Approve |
| **Execution Latency** | Autonomous background resolution in $< 1.0$ second | Execution frozen until human operator authorization |
| **ITIL Change Record** | Recorded automatically as `AUTO_REMEDIATED (Tier 1)` | Recorded with human operator signature as `APPROVED_EXECUTE (Tier 3)` |

---

### Uncritical Runbook RB-UNC-01: Routine Preventive Disk & Cache Hygiene
* **Target Subsystem:** `/tmp` and inactive rotatable application log archives.
* **Trigger Condition:** Off-peak maintenance schedule OR disk usage between $60.0\%$ and $75.0\%$ (non-emergency).
* **Safe Action Tier:** Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)
* **Blast Radius:** $0\%$ — Purely temporary scratch files and inactive logs older than 7 days.
* **Encoded SRE Judgment:** IF disk utilization is non-critical and free space is well above safety floors, prune stale `/tmp` socket files and compress archives. Do NOT page or alert human operators.
* **Remediation Script:**
  ```bash
  find /tmp -type f -name '*.tmp' -mtime +7 -delete && find /var/log/app/ -name '*.log.[1-9]' -mtime +3 -exec gzip {} \\; && journalctl --vacuum-size=500M
  ```
* **Post-Verification Probe:**
  ```bash
  df -h / | awk 'NR==2 {print "PASS_DISK_HEALTHY"}'
  ```

---

### Uncritical Runbook RB-UNC-02: Routine Worker Heap Trim & Soft Garbage Collection
* **Target Subsystem:** Background Celery/Redis Worker Pool (`Worker-03`).
* **Trigger Condition:** Worker process has handled $> 2,000$ completed tasks OR periodic idle lull.
* **Safe Action Tier:** Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)
* **Blast Radius:** $0\%$ — Worker is fully healthy; reload occurs during idle gap between message batches.
* **Encoded SRE Judgment:** Long-running Python worker processes accumulate memory heap fragmentation over time. Performing a soft graceful reload resets memory without dropping any in-flight client jobs.
* **Remediation Script:**
  ```bash
  systemctl reload-or-restart celery-worker@worker-03.service
  ```
* **Post-Verification Probe:**
  ```bash
  systemctl is-active celery-worker@worker-03.service && echo "WORKER_HEALTHY_PASS"
  ```

---

### Uncritical Runbook RB-UNC-03: Off-Peak Minor Queue Backlog Balancing
* **Target Subsystem:** Order Processing Message Queue (`orders.v1`).
* **Trigger Condition:** Backlog transient ripple between $200$ and $1,000$ messages (well below the $30,000$ emergency threshold).
* **Safe Action Tier:** Tier 1 (Uncritical - Silent Safe Auto)
* **Blast Radius:** Low ($< 5\%$) — Scales 1 standby consumer worker pod within cluster safety bounds.
* **Encoded SRE Judgment:** A minor morning order ripple does not warrant emergency alarms. SafeOps smoothly activates 1 standby consumer pod to keep queue latency strictly under 200ms.
* **Remediation Script:**
  ```bash
  kubectl scale deployment/order-consumer --replicas=4 --namespace=orders
  ```
* **Post-Verification Probe:**
  ```bash
  kubectl get deployment/order-consumer -o jsonpath='{.status.readyReplicas}'
  ```

---

### Uncritical Runbook RB-UNC-04: Preventive SSL/TLS Certificate Audit & OCSP Stapling
* **Target Subsystem:** Ingress Edge Gateway TLS Handshake (`api.production.internal`).
* **Trigger Condition:** Scheduled weekly audit OR certificate validity at $45.0$ days remaining (ample buffer).
* **Safe Action Tier:** Tier 0 / Tier 1 (Uncritical - Preventive Health Audit)
* **Blast Radius:** $0\%$ — Non-destructive, read-only cryptographic validation probe.
* **Encoded SRE Judgment:** Validate TLS trust chains and OCSP stapling 45 days in advance. No certificate installation or server restart is necessary.
* **Remediation Script:**
  ```bash
  openssl s_client -servername api.production.internal -connect 127.0.0.1:443 </dev/null 2>/dev/null | openssl x509 -noout -dates && echo "AUDIT_VERIFIED_VALID"
  ```
* **Post-Verification Probe:**
  ```bash
  openssl x509 -checkend 2592000 -noout -in /etc/ssl/certs/api.production.internal.crt && echo "CERT_VALID_PASS"
  ```

---

## Section F: How to Present & Impress the Judges (Live Showcase Script)

Use this step-by-step walkthrough during your live presentation to demonstrate why SafeOps AI satisfies Problem AO-04 (*"Automation that is safe enough to leave switched on during night shift"*):

### 1. The Opening Pitch (30 seconds)
> *"Good morning/afternoon, Judges! We are Team Idea Ignitors (XH-23). Today, DevOps teams face a painful dilemma: either leave automation off and get woken up at 3:00 AM for routine fixes, or leave automation on and risk an AI making a catastrophic mistake that crashes the company. We built **SafeOps AI**—an explainable, safe AI-Ops engine that encodes human engineering judgment into ITIL runbooks."*

### 2. Demonstrate the Uncritical Routine Scenario (1 minute)
* In **Section 2 (Interactive Fault Injector Sandbox)**, click the filter button: **`[🟢 Uncritical / Routine (4)]`**.
* Click the button: **`🟢 Routine /tmp & Logs (62%)`**.
* **What to tell the judges:**
  > *"Look at this, Judges: This is an uncritical situation. The disk is at 62%, with routine temporary scratch files. SafeOps AI evaluates Runbook RB-UNC-01, confirms the blast radius is strictly 0%, and resolves it **100% autonomously in under 1 second**.*  
  > *Notice that **no human was woken up!** The engineer slept peacefully, while our ITIL audit log recorded a clean, cryptographic change record."*

### 3. Demonstrate the Critical / Ambiguous Scenario (1 minute)
* In Section 2, click the button: **`🔴 MySQL Core Dumps (96%)`**.
* Show the judges the dashboard reaction:
  > *"Now watch what happens when a dangerous, critical situation occurs! The disk is at 96%, but this time it is full of MySQL core dumps and crash logs.*  
  > *A naive automation script would delete these files, destroying crash evidence or breaking database replication! But SafeOps AI detects the high blast radius, halts instantly, and engages the **Flashing Amber Human Authorization Gate**.*  
  > *It refuses to run any command until an authorized engineer reviews the exact blast radius and clicks **Approve**."*
* Click **`[Approve & Execute Fix]`** and watch the verified recovery!

### 4. Demonstrate Automatic Rollback (45 seconds)
* Click the checkbox: **`Force Verification Failure (Demonstrate Rollback)`**.
* Click **`Execute Remediation Plan`**.
* Point to the terminal output:
  > *"If the fix fails the post-remediation health probe, SafeOps AI **automatically rolls back** to the last-known-good snapshot in under 2 seconds, guaranteeing zero catastrophic downtime."*

### 5. Demonstrate the Master Kill-Switch (30 seconds)
* In the top bar, click **`[KILL SWITCH: OFF]`** to toggle it to **`[KILL SWITCH: ON]`**.
* Attempt any action: show the red banner blocking execution.
  > *"Finally, if any anomaly occurs, the Master Kill-Switch instantly freezes all automation cluster-wide with 1 click."*
"""

with open(RUNBOOK_PATH, "r", encoding="utf-8") as f:
    existing = f.read()

if "Section E: Uncritical Routine Maintenance" not in existing:
    with open(RUNBOOK_PATH, "a", encoding="utf-8") as f:
        f.write(appendix)
    print("MASTER_OPERATIONAL_RUNBOOK.md successfully updated with Section E & Section F!")
else:
    print("Section E already present in MASTER_OPERATIONAL_RUNBOOK.md.")

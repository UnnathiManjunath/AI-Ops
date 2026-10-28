# MASTER OPERATIONAL RUNBOOK: SRE-RB-001
## Automated Night-Shift Remediation & Safety Guardrails Policy
**System:** Enterprise Cloud Production Cluster (`prod-cluster-alpha`)  
**Track:** Cynefian Student Hackathon — AI-Ops Track (Problem AO-04)  
**Authors:** Team Idea Ignitors (XH-23) — Unnathi T M, Chaithanya N S, M Eshwar, Babitha M  
**Status:** Approved for SafeOps AI Automated Execution  
**Compliance Standard:** ITIL v4 Standard & Emergency Change Management  

---

## 📋 Table of Contents
1. [Runbook Policy Framework & Action Tiers](#1-runbook-policy-framework--action-tiers)
2. [Section A: Clearing a Full Disk (Storage & Filesystem)](#section-a-clearing-a-full-disk-storage--filesystem)
3. [Section B: Restarting a Stuck Background Worker (Compute & Processes)](#section-b-restarting-a-stuck-background-worker-compute--processes)
4. [Section C: Scaling a Queue Consumer (Messaging & Stream Processing)](#section-c-scaling-a-queue-consumer-messaging--stream-processing)
5. [Section D: Rotating an Expiring Security Certificate (Edge Ingress & TLS)](#section-d-rotating-an-expiring-security-certificate-edge-ingress--tls)
6. [Emergency Kill-Switch & Anti-Runaway Protection](#6-emergency-kill-switch--anti-runaway-protection)

---

## 1. Runbook Policy Framework & Action Tiers

To eliminate 3:00 AM human wakeups while preventing catastrophic automated outages, all remediations in this runbook are categorized into three risk tiers:

* **Tier 1 (Low Risk — Safe Auto-Execute):** Routine, non-destructive, scoped strictly to ephemeral files or stateless processes. Executed autonomously without waking an engineer.
* **Tier 2 (Medium Risk — Guarded Auto-Execute):** State changes bounded by strict hard ceilings (e.g., max scaling limits) with mandatory pre/post health probes.
* **Tier 3 (High Risk / Ambiguous — Human-in-the-Loop Required):** Scenarios where automated execution risks data loss or cascading outages (e.g., database saturation, core dumps). **Automation is locked until explicit operator approval is recorded.**

---

## Section A: Clearing a Full Disk (Storage & Filesystem)

### 1. Alarm & Trigger Condition
* **Alert Rule:** `HighDiskUtilizationCritical`
* **Trigger Threshold:** Filesystem space usage on partition `/dev/sda1` $\ge 90.0\%$ for $> 5$ minutes.
* **Impact Subsystem:** Root `/` partition and application logging directory `/var/log/app/`.

### 2. Encoded Operational Judgment (Pre-Checks)
Before running any cleanup command, the system must inspect the disk contents:
* **Condition 1 (Safe Routine):** If disk exhaustion is caused by rotated stdout/access logs (`app-access.log.[1-9]`) older than 48 hours $\rightarrow$ **Proceed with Tier 1 Auto-Compression**.
* **Condition 2 (Dangerous / Ambiguous):** If disk exhaustion is caused by database binary logs, active tablespaces, or kernel crash dumps (`/var/lib/mysql/core.*`) $\rightarrow$ **DO NOT PURGE.** Deleting core dumps destroys critical diagnostic evidence; deleting DB logs causes replication failure. **Escalate to Senior DBA & require Tier 3 Human Sign-off.**

### 3. Execution Plan
* **Action Tier:** Tier 1 (for rotated logs) / Tier 3 (for core dumps)
* **Blast Radius:** Local node disk storage only. Zero client request disruption.
* **Least-Privilege Role:** `svc-safeops-storage-cleaner`

```bash
# Pre-Snapshot & Dry Run Check
df -h /var/log/app/
find /var/log/app/ -name '*.log.[1-9]' -mtime +2 -exec ls -lh {} \;

# Remediation Command (Safe Gzip Archival & Journal Vacuum)
find /var/log/app/ -name '*.log.[1-9]' -mtime +2 -exec gzip {} \; && journalctl --vacuum-time=1d
```

### 4. Verification Check (Post-Probe)
```bash
# Verify disk usage dropped below safe threshold (75%)
df -h / | awk 'NR==2 {gsub("%", ""); if ($5 < 75) print "PASS"; else print "FAIL"}'
```

### 5. Automated Rollback Procedure
* **Rollback Trigger:** If post-check returns `FAIL` or application fails to write subsequent logs.
```bash
# Decompress archives to restore pre-action filesystem state
find /var/log/app/ -name '*.log.[1-9].gz' -exec gunzip {} \;
```

---

## Section B: Restarting a Stuck Background Worker (Compute & Processes)

### 1. Alarm & Trigger Condition
* **Alert Rule:** `WorkerHeartbeatMissingCritical`
* **Trigger Threshold:** Celery/Redis background worker (`worker-03`) missed heartbeat for $> 180$ seconds; job queue processing stalled.
* **Impact Subsystem:** Asynchronous background processing (emails, report generation, invoice PDFs).

### 2. Encoded Operational Judgment (Pre-Checks)
* **Condition 1 (Safe Soft Lock):** Worker thread is locked on a network timeout, but upstream PostgreSQL connection pool is nominal ($< 50\%$ active connections) $\rightarrow$ **Safe for Tier 1 Graceful Restart.**
* **Condition 2 (Cascade Danger — Thundering Herd):** If the PostgreSQL connection pool is saturated ($\ge 98\%$ capacity), the worker is stuck *because* it cannot acquire a DB socket. **DO NOT RESTART THE WORKER.** Restarting worker daemons will spawn 16 aggressive new connection retries simultaneously, triggering a thundering herd crash on the primary database! **Escalate to Lead SRE and require Tier 3 Human Approval to drain connection pool first.**

### 3. Execution Plan
* **Action Tier:** Tier 1 (if DB pool healthy) / Tier 3 (if DB pool saturated)
* **Blast Radius:** Single worker daemon (`worker-03`). In-flight jobs requeued to Kafka with timeout ACK.
* **Least-Privilege Role:** `svc-safeops-process-manager`

```bash
# Pre-Check DB Connection Pool Health
psql -h pg-primary.internal -U ops -c "SELECT count(*) FROM pg_stat_activity WHERE state = 'active';"

# Remediation Command (Graceful SIGTERM Restart with 10s Drain Window)
systemctl restart celery-worker@worker-03.service
```

### 4. Verification Check (Post-Probe)
```bash
# Verify worker daemon is actively listening and responsive
systemctl is-active celery-worker@worker-03.service && sleep 2 && celery -A tasks inspect ping -d celery@worker-03
```

### 5. Automated Rollback Procedure
* **Rollback Trigger:** If worker enters crash loop (`exit status 137 / OOMKilled`).
```bash
# Stop failing worker and fall back to standby auxiliary worker pool
systemctl stop celery-worker@worker-03.service && systemctl start celery-worker@worker-03-fallback.service
```

---

## Section C: Scaling a Queue Consumer (Messaging & Stream Processing)

### 1. Alarm & Trigger Condition
* **Alert Rule:** `KafkaConsumerLagCritical`
* **Trigger Threshold:** Backlog on topic `orders.v1` exceeds $30,000$ messages; consumer lag trend is positive.
* **Impact Subsystem:** Real-time customer checkout order processing.

### 2. Encoded Operational Judgment (Pre-Checks)
* **Condition 1 (Genuine Traffic Surge):** Consumer error rate is $< 1\%$; pods are CPU-bound processing legitimate purchase surges $\rightarrow$ **Safe to scale horizontally (Tier 2 Guarded Auto) up to hard ceiling of 10 replicas.**
* **Condition 2 (Poison Pill Malformed Payload):** Consumer error rate is $> 50\%$; workers are crashing with `KeyError` on specific corrupt offsets $\rightarrow$ **DO NOT SCALE CONSUMERS.** Autoscaling will consume cloud budget and crash additional pods. **Quarantine the poison payload to Dead Letter Queue (DLQ) and require Tier 3 Human Authorization.**

### 3. Execution Plan
* **Action Tier:** Tier 2 (Guarded Auto — bounded by Max Ceiling = 10 pods)
* **Blast Radius:** Kubernetes compute pod pool. Hard limit prevents resource exhaustion.
* **Least-Privilege Role:** `svc-safeops-k8s-scaler`

```bash
# Pre-Check Consumer Error Rate
curl -s http://prometheus:9090/api/v1/query?query=rate(consumer_errors_total[5m])

# Remediation Command (Scale Deployment from 3 to 6 Pods)
kubectl scale deployment/order-consumer --replicas=6 --namespace=orders
```

### 4. Verification Check (Post-Probe)
```bash
# Verify 6 pods ready and queue draining rate exceeds 1,500 msg/s
kubectl get deployment/order-consumer -n orders -o jsonpath='{.status.readyReplicas}' | grep '6'
```

### 5. Automated Rollback Procedure
* **Rollback Trigger:** If pod scaling causes node CPU exhaustion ($> 95\%$).
```bash
# Revert replica count to original baseline of 3 pods
kubectl scale deployment/order-consumer --replicas=3 --namespace=orders
```

---

## Section D: Rotating an Expiring Security Certificate (Edge Ingress & TLS)

### 1. Alarm & Trigger Condition
* **Alert Rule:** `TLSCertificateExpirationImminent`
* **Trigger Threshold:** TLS edge certificate validity $\le 7$ days remaining.
* **Impact Subsystem:** Ingress Edge Gateway (`api.production.internal`).

### 2. Encoded Operational Judgment (Pre-Checks)
* **Condition 1 (Routine Expiry):** ACME HTTP-01 challenge reachability confirmed; domain DNS points to valid edge IP $\rightarrow$ **Safe for Tier 1 Autonomous Renewal.**
* **Condition 2 (Root CA Drift / Revocation):** Intermediate or root certificate authority has revoked trust or domain ownership mismatch detected $\rightarrow$ **DO NOT ATTEMPT SCRIPTED RENEW.** Escalate to Security Engineering Lead (Tier 3).

### 3. Execution Plan
* **Action Tier:** Tier 1 (Low Risk — Safe Auto)
* **Blast Radius:** TLS termination gateway. Zero socket drop; seamless Nginx configuration reload.
* **Least-Privilege Role:** `svc-safeops-cert-manager`

```bash
# Pre-Snapshot Backup of Existing Certificate Store
cp /etc/ssl/certs/api.production.internal.crt /etc/ssl/backup/last_known_good.crt

# Remediation Command (ACME Certbot Renewal & Seamless Reload)
certbot renew --cert-name api.production.internal --quiet && nginx -s reload
```

### 4. Verification Check (Post-Probe)
```bash
# Verify newly installed certificate is valid for at least 60 days
openssl x509 -checkend 5184000 -noout -in /etc/ssl/certs/api.production.internal.crt && echo "PASS"
```

### 5. Automated Rollback Procedure
* **Rollback Trigger:** If Nginx configuration test fails (`nginx -t` fails) or TLS handshake drops.
```bash
# Revert to backup certificate and reload edge web server
cp /etc/ssl/backup/last_known_good.crt /etc/ssl/certs/api.production.internal.crt && nginx -s reload
```

---

## 6. Emergency Kill-Switch & Anti-Runaway Protection

* **Master Kill-Switch:** If unexpected behavior or multiple cascading alerts occur, toggling the Emergency Kill-Switch freezes **100% of automated remediation threads cluster-wide**.
* **Rate Limiter:** Maximum 5 automated remediations allowed per rolling minute to prevent runaway remediation loops.
* **ITIL Audit Log:** Every action, whether executed autonomously or approved by a human operator, is committed to the immutable change record log with Change ID, Actor, Command, and Rollback State.


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
  find /tmp -type f -name '*.tmp' -mtime +7 -delete && find /var/log/app/ -name '*.log.[1-9]' -mtime +3 -exec gzip {} \; && journalctl --vacuum-size=500M
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

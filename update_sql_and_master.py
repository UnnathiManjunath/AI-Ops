import sqlite3
import json
import shutil
import os

PROJECT_DIR = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai"
DB_PATH = os.path.join(PROJECT_DIR, "safeops.db")
MASTER_DB_PATH = os.path.join(PROJECT_DIR, "safeops_master.db")
JSON_PATH = os.path.join(PROJECT_DIR, "MASTER_DATABASE_DATASET.json")
SQL_PATH = os.path.join(PROJECT_DIR, "MASTER_SRE_DATABASE.sql")

new_sql = """-- ============================================================================
-- SafeOps AI - Enterprise Master SRE Operational Database Schema & Seed Data
-- Track: Cynefian 24-Hour Student Hackathon - AI-Ops Track (Problem AO-04)
-- Team: Idea Ignitors (XH-23) - Unnathi T M, Chaithanya N S, M Eshwar, Babitha M
-- Standards: ITIL v4 Standard Change Management & Google SRE Guardrails
-- ============================================================================

CREATE TABLE IF NOT EXISTS system_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_key TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    threshold_warn REAL NOT NULL,
    threshold_crit REAL NOT NULL,
    status TEXT NOT NULL,
    server_node TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS safety_policies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    policy_key TEXT UNIQUE NOT NULL,
    policy_name TEXT NOT NULL,
    value TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS runbooks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    runbook_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    target_subsystem TEXT NOT NULL,
    trigger_condition TEXT NOT NULL,
    safe_action_tier TEXT NOT NULL,
    blast_radius TEXT NOT NULL,
    judgment_rules TEXT NOT NULL,
    remediation_command TEXT NOT NULL,
    rollback_command TEXT NOT NULL,
    verification_check TEXT NOT NULL,
    documentation TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_code TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    fault_type TEXT NOT NULL,
    server_node TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    current_step TEXT NOT NULL,
    telemetry_snapshot TEXT,
    root_cause TEXT,
    ai_reasoning TEXT,
    risk_tier TEXT,
    blast_radius_desc TEXT,
    proposed_action TEXT,
    remediation_command TEXT,
    rollback_command TEXT,
    verification_check TEXT,
    requires_human_approval INTEGER DEFAULT 0,
    approved_by TEXT,
    approval_timestamp TIMESTAMP,
    remediation_logs TEXT,
    verification_status TEXT,
    rollback_triggered INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    change_id TEXT UNIQUE NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    incident_code TEXT NOT NULL,
    incident_title TEXT NOT NULL,
    actor TEXT NOT NULL,
    action_type TEXT NOT NULL,
    risk_tier TEXT NOT NULL,
    command_executed TEXT,
    blast_radius TEXT,
    outcome TEXT NOT NULL,
    itil_justification TEXT NOT NULL,
    verification_details TEXT
);

-- Safety Policies
INSERT OR REPLACE INTO safety_policies (policy_key, policy_name, value, description) VALUES
('kill_switch_active', 'Emergency Master Kill Switch', 'false', 'Instant hardware-style freeze for 100% of automation threads cluster-wide.'),
('rate_limit_per_minute', 'Action Rate Limiter', '5', 'Strict limit of maximum 5 automated remediation actions per minute to prevent loops.'),
('max_scaling_instances', 'Max Queue Worker Ceiling', '10', 'Hard cloud compute ceiling to prevent cloud bill runaway ($4,200/hr risk).'),
('disk_safety_floor_gb', 'Disk Safety Floor', '5.0', 'Minimum free disk space buffer below which high-risk escalation is mandated.'),
('tier1_auto_enabled', 'Tier 1 Safe Auto-Remediation', 'true', 'Autonomous execution of verified non-destructive fixes without engineer wakeups.'),
('tier3_requires_approval', 'Tier 3 Human Authorization Gate', 'true', 'Mandatory human approval gate before executing actions that affect persistent data or state.');

-- System Metrics Baseline
INSERT OR REPLACE INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES
('disk_usage_pct', 'Postgres WAL Storage (/var/lib/postgresql/pg_wal)', 54.2, '%', 80.0, 95.0, 'OK', 'prod-db-primary-01'),
('worker_status', 'Fintech Payment Worker Pool (py-recon-daemon)', 1.0, 'State (0=Locked, 1=Alive)', 0.5, 0.0, 'OK', 'fintech-recon-01'),
('queue_backlog_depth', 'Fraud Evaluation Kafka Backlog', 850.0, 'msgs', 10000.0, 50000.0, 'OK', 'kafka-cluster-frauddetection'),
('ssl_cert_days', 'Production Ingress Edge TLS Validity', 58.0, 'days', 14.0, 5.0, 'OK', 'api.globalpay.com'),
('cpu_utilization', 'Cluster CPU Load Average', 28.5, '%', 75.0, 90.0, 'OK', 'k8s-node-pool-1'),
('memory_utilization', 'Cluster RAM Usage', 44.2, '%', 80.0, 90.0, 'OK', 'k8s-node-pool-1');

-- The 12 Distinct Problem Runbooks (Critical, Warning, and Uncritical for all 4 Areas)

-- 1. STORAGE EXHAUSTION
INSERT OR REPLACE INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES
('RB-01-CRIT', 'Storage Critical: PostgreSQL WAL Replication Full (99.4% - 124MB Left)', 'Storage & Database', '/var/lib/postgresql/pg_wal', 'Disk usage > 99% and WAL segments unarchived', 'Tier 3 (High Risk - Human Approval Required)', 'CRITICAL: Database shutdown & replica cluster desynchronization.', 'IF WAL directory is at 99.4% due to replica lag, DO NOT delete WAL files blindly; sync to S3 cold storage with human sign-off.', 'aws s3 sync /var/lib/postgresql/pg_wal s3://ops-wal-archive/ && rm -f /var/lib/postgresql/pg_wal/*.old', 'aws s3 sync s3://ops-wal-archive/ /var/lib/postgresql/pg_wal/ || true', 'df -h /var/lib/postgresql/pg_wal | awk ''NR==2 {gsub("%", ""); if ($5 < 85) print "PASS"; else print "FAIL"}''', 'Prevents PostgreSQL emergency PANIC crash shutdown while preserving replication.'),

('RB-01-WARN', 'Storage Warning: Nginx Reverse Proxy Cache Over High-Water Mark (88.5%)', 'Storage & Caching', '/var/cache/nginx', 'Cache partition usage > 85%', 'Tier 1 (Low Risk - Safe Auto)', 'LOW: Local proxy cache only. Zero client request disruption.', 'IF cache partition exceeds 85%, purge cached static asset objects older than 24h. Zero active database risk.', 'find /var/cache/nginx -type f -mtime +1 -delete && nginx -s reload', 'echo ROLLBACK_CACHE_REBUILD', 'df -h /var/cache/nginx | awk ''NR==2 {gsub("%", ""); if ($5 < 75) print "PASS"; else print "FAIL"}''', 'Reclaims 28.5 GB storage safely with zero application downtime.'),

('RB-UNC-01', 'Storage Uncritical: Developer Sandbox & Docker Build Scratch Hygiene (54.2%)', 'Storage & Hygiene', '/tmp/builds', 'Off-peak schedule OR disk between 50% and 65%', 'Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)', 'ZERO (0%): Targets purely stale scratch build layers older than 14 days.', 'IF disk utilization is non-critical (54.2%), prune stale docker build layers silently without waking on-call engineers.', 'find /tmp/builds -type f -name ''*.tmp'' -mtime +14 -delete && journalctl --vacuum-size=500M', 'touch /tmp/builds/.maintenance_complete', 'df -h / | awk ''NR==2 {print "PASS_DISK_HEALTHY"}''', 'Routine bi-weekly container scratch hygiene.');

-- 2. WORKER THREADLOCK
INSERT OR REPLACE INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES
('RB-02-CRIT', 'Worker Critical: Payment Reconciliation Threadlock (8,400 In-Flight Jobs - $1.42M)', 'Compute & Fintech', 'Fintech py-recon-daemon', 'Worker locked and in_flight_transactions > 5000', 'Tier 3 (High Risk - Human Approval Required)', 'HIGH: Financial transaction integrity + $1.42M active settlements.', 'IF worker is locked with 8,400 in-flight payments, DO NOT kill worker process (prevents duplicate credit card charges). Escalate to Fintech SRE.', 'python3 /opt/safeops/scripts/drain_recon_locks.py && systemctl restart py-recon-daemon.service', 'systemctl restart py-recon-daemon.service', 'systemctl is-active py-recon-daemon.service', 'Enforces strict protection against financial transaction corruption.'),

('RB-02-WARN', 'Worker Warning: Email Dispatcher Celery Worker Hung on SendGrid Timeout (310s)', 'Compute & Processes', 'email-worker-02', 'Worker heartbeat missed for > 300s (DB pool healthy)', 'Tier 1 (Low Risk - Safe Auto)', 'LOW: Single worker process (email-worker-02). Zero financial data risk.', 'IF worker is hung in external SendGrid socket wait and DB pool is healthy (12%), perform graceful SIGTERM restart.', 'systemctl restart celery-worker@email-worker-02.service', 'systemctl restart celery-worker@email-worker-02-fallback.service', 'systemctl is-active celery-worker@email-worker-02.service', 'Restores email notification queue with automated message requeue.'),

('RB-UNC-02', 'Worker Uncritical: Media Image Worker Heap Compaction (15,400 Tasks)', 'Compute & Memory Hygiene', 'media-worker-05', 'Worker processed > 15,000 tasks (Worker Healthy)', 'Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)', 'ZERO (0%): Soft reload occurs between image batches. Zero dropped tasks.', 'IF image worker is healthy but has minor heap fragmentation, trigger graceful worker reload during idle lull.', 'systemctl reload-or-restart celery-worker@media-worker-05.service', 'systemctl status celery-worker@media-worker-05.service', 'systemctl is-active celery-worker@media-worker-05.service', 'Compacts Python heap memory without interrupting active image jobs.');

-- 3. MESSAGE QUEUE STREAM LAG
INSERT OR REPLACE INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES
('RB-03-CRIT', 'Queue Critical: Fraud Kafka Stream Poison Pill Crash (142,800 msgs - 92.4% Err)', 'Messaging & Security', 'fraud.transactions.v2', 'Queue backlog > 100,000 and consumer error rate > 80%', 'Tier 3 (High Risk - Human Approval Required)', 'HIGH: Fraud evaluation bypass and $4,200/hr compute burn.', 'IF error rate > 80% (poison pill crashing pods), DO NOT scale pods (prevents $4,200/hr compute burn); divert bad offset to DLQ.', 'kafka-consumer-groups --bootstrap-server kafka:9092 --group fraud-eval --topic fraud.transactions.v2 --reset-offsets --to-offset 402912 --execute', 'kafka-consumer-groups --bootstrap-server kafka:9092 --group fraud-eval --topic fraud.transactions.v2 --reset-offsets --to-offset 402911 --execute', 'echo PASS_DLQ_ROUTED', 'Prevents compute resource waste on poison pill messages in high-scale streams.'),

('RB-03-WARN', 'Queue Warning: Flash Sale Promotion Checkout Influx (28,500 msgs)', 'Messaging & Scaling', 'checkout.flash.events', 'Queue backlog > 20,000 and error rate < 0.1%', 'Tier 2 (Guarded Auto - Within Policy Limits)', 'MEDIUM: Kubernetes worker deployment. Max replicas capped at 10.', 'IF error rate < 0.1% (clean flash surge), autoscale deployment from 4 to 8 pods, strictly respecting max ceiling 10.', 'kubectl scale deployment/order-consumer --replicas=8 --namespace=orders', 'kubectl scale deployment/order-consumer --replicas=4 --namespace=orders', 'kubectl get deployment/order-consumer -o jsonpath=''{.status.readyReplicas}''', 'Autoscales consumer pods within strict cloud compute cost ceiling.'),

('RB-UNC-03', 'Queue Uncritical: Clickstream Telemetry Analytics Ripple (850 msgs)', 'Messaging & Queues', 'clicks.telemetry.raw', 'Backlog between 500 and 1,500 messages (Minor Transient Ripple)', 'Tier 1 (Uncritical - Silent Safe Auto)', 'LOW (< 5%): Spins up 1 standby consumer container.', 'IF backlog is slightly elevated during morning burst (850 msgs), spin up 1 standby pod to maintain sub-150ms processing SLA.', 'kubectl scale deployment/order-consumer --replicas=4 --namespace=orders', 'kubectl scale deployment/order-consumer --replicas=3 --namespace=orders', 'kubectl get deployment/order-consumer -o jsonpath=''{.status.readyReplicas}''', 'Smooths out transient order ripples without triggering alarms.');

-- 4. SSL/TLS CERTIFICATE ROTATION
INSERT OR REPLACE INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES
('RB-04-CRIT', 'SSL Critical: Edge API Gateway Root CA Revocation (6 Hours Left - CRL Drift)', 'Security & Ingress', 'api.globalpay.com', 'Certificate validity < 12 hours and CA revoked upstream', 'Tier 3 (High Risk - Human Approval Required)', 'CRITICAL: Edge Gateway TLS Handshake & Public Trust for api.globalpay.com.', 'IF intermediate CA is revoked upstream, automated ACME renewal cannot succeed. Escalate immediately to Security Ops Lead.', 'update-ca-certificates --fresh && nginx -s reload', 'cp /etc/ssl/backup/last_known_good.crt /etc/ssl/certs/ && nginx -s reload', 'openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/api.globalpay.com.crt', 'Protects public API gateway from using compromised or revoked certificate chains.'),

('RB-04-WARN', 'SSL Warning: Customer Web Portal TLS Certificate Expiring (4.5 Days)', 'Security & Networking', 'portal.production.io', 'Certificate validity <= 7 days (ACME HTTP-01 valid)', 'Tier 1 (Low Risk - Safe Auto)', 'LOW: Edge API Gateway. Seamless configuration reload with zero socket drop.', 'IF certificate is within 5 days of expiry and DNS records valid, trigger automated certbot renewal and seamless nginx reload.', 'certbot renew --cert-name portal.production.io --quiet && nginx -s reload', 'cp /etc/ssl/backup/last_known_good.crt /etc/ssl/certs/ && nginx -s reload', 'openssl x509 -checkend 604800 -noout -in /etc/ssl/certs/portal.production.io.crt', 'Non-destructive TLS key rotation with zero downtime.'),

('RB-UNC-04', 'SSL Uncritical: Internal Microservice Mutual TLS Health Audit (58.0 Days)', 'Security & Auditing', 'mTLS-auth.internal', 'Scheduled audit OR certificate validity at 58 days remaining', 'Tier 0 / Tier 1 (Uncritical - Preventive Health Audit)', 'ZERO (0%): Read-only cryptographic handshake validation probe.', 'IF certificate validity is healthy (58 days remaining), execute routine cryptographic trust check. No human action required.', 'openssl s_client -servername mTLS-auth.internal -connect 127.0.0.1:443 </dev/null 2>/dev/null | openssl x509 -noout -dates && echo ''AUDIT_VERIFIED_VALID''', 'echo ''AUDIT_NOOP''', 'openssl x509 -checkend 2592000 -noout -in /etc/ssl/certs/mTLS-auth.internal.crt', 'Proactive, non-urgent certificate validity verification.');
"""

with open(SQL_PATH, "w", encoding="utf-8") as f:
    f.write(new_sql)
print("MASTER_SRE_DATABASE.sql written successfully!")

# Apply to SQLite
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.executescript(new_sql)
conn.commit()

# Export JSON
conn.row_factory = sqlite3.Row
c2 = conn.cursor()
c2.execute("SELECT * FROM safety_policies")
policies = [dict(r) for r in c2.fetchall()]
c2.execute("SELECT * FROM system_metrics")
metrics = [dict(r) for r in c2.fetchall()]
c2.execute("SELECT * FROM runbooks")
runbooks = [dict(r) for r in c2.fetchall()]
c2.execute("SELECT * FROM incidents ORDER BY id DESC LIMIT 50")
incidents = [dict(r) for r in c2.fetchall()]
c2.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT 50")
audit_logs = [dict(r) for r in c2.fetchall()]
conn.close()

master_dataset = {
    "metadata": {
        "dataset_name": "SafeOps AI - Distinct Enterprise SRE Operational Database",
        "version": "3.0.0-ENTERPRISE",
        "hackathon": "Cynefian 24-Hour Student Hackathon - AI-Ops Track",
        "problem_statement": "AO-04: Automation Safe Enough to Leave Switched On",
        "team": "Idea Ignitors (XH-23) - Unnathi T M, Chaithanya N S, M Eshwar, Babitha M",
        "format": "Relational SQLite & JSON Interchange Schema",
        "distinct_telemetry": {
            "problem_1_storage": {
                "critical": "PostgreSQL WAL Exhaustion (99.4% Capacity - 124MB left - PANIC Shutdown Risk)",
                "warning": "Nginx Reverse Proxy Static Cache Exceeded (88.5% Capacity)",
                "uncritical": "Developer Sandbox & Docker Build Scratch Hygiene (54.2% Disk - 92GB Free)"
            },
            "problem_2_processes": {
                "critical": "Payment Reconciliation Engine Threadlock (8,400 In-Flight Jobs - $1.42M Volume)",
                "warning": "Email Dispatcher Celery Worker Hung on SendGrid HTTP Timeout (310s)",
                "uncritical": "Image Worker Heap Compaction & Soft Recycle (15,400 Tasks Completed)"
            },
            "problem_3_queues": {
                "critical": "Fraud Detection Kafka Stream Backlog (142,800 msgs - 92.4% Error Rate - $4,200/hr Burn)",
                "warning": "Flash Sale Promotion Checkout Influx (28,500 msgs - Autoscale 4 to 8 Pods)",
                "uncritical": "Clickstream Analytics Minor Backlog Ripple (850 msgs)"
            },
            "problem_4_ssl": {
                "critical": "Edge API Gateway Root CA Revocation (6 Hours Remaining! CRL Upstream Drift)",
                "warning": "Customer Web Portal TLS Certificate Expiring (4.5 Days)",
                "uncritical": "Internal Microservice Mutual TLS Health Audit (58.0 Days Remaining)"
            }
        }
    },
    "safety_policies": policies,
    "system_metrics": metrics,
    "runbooks": runbooks,
    "incidents": incidents,
    "audit_logs": audit_logs
}

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(master_dataset, f, indent=2)

shutil.copyfile(DB_PATH, MASTER_DB_PATH)
print("MASTER_DATABASE_DATASET.json and safeops_master.db updated with Distinct Enterprise SRE Dataset!")

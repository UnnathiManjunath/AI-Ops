"""
SafeOps AI - Database Module
SQLite database schema, initialization, and runbook definitions.
Designed for Cynefian Hackathon - AI-Ops Track (Team Idea Ignitors XH-23)
"""

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "safeops.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 1. System Metrics & Telemetry Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        metric_key TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        value REAL NOT NULL,
        unit TEXT NOT NULL,
        threshold_warn REAL NOT NULL,
        threshold_crit REAL NOT NULL,
        status TEXT NOT NULL, -- OK, WARN, CRITICAL
        server_node TEXT NOT NULL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Safety Policies & Guardrails Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS safety_policies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        policy_key TEXT UNIQUE NOT NULL,
        policy_name TEXT NOT NULL,
        value TEXT NOT NULL,
        description TEXT NOT NULL
    );
    """)

    # 3. 10 Representative Runbooks Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS runbooks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        runbook_id TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        target_subsystem TEXT NOT NULL,
        trigger_condition TEXT NOT NULL,
        safe_action_tier TEXT NOT NULL, -- Tier 1 (Low), Tier 2 (Medium), Tier 3 (High)
        blast_radius TEXT NOT NULL,
        judgment_rules TEXT NOT NULL, -- Human judgment encoded in policy
        remediation_command TEXT NOT NULL,
        rollback_command TEXT NOT NULL,
        verification_check TEXT NOT NULL,
        documentation TEXT NOT NULL
    );
    """)

    # 4. Incidents Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_code TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        fault_type TEXT NOT NULL,
        server_node TEXT NOT NULL,
        severity TEXT NOT NULL, -- LOW, MEDIUM, HIGH, CRITICAL
        status TEXT NOT NULL, -- DETECTED, DIAGNOSED, AWAITING_APPROVAL, APPROVED, REJECTED, EXECUTING, RESOLVED, FAILED, ROLLED_BACK
        current_step TEXT NOT NULL, -- detect, diagnose, risk_assess, approval, execute, verify, audit
        telemetry_snapshot TEXT, -- JSON
        root_cause TEXT,
        ai_reasoning TEXT,
        risk_tier TEXT, -- Tier 1 (Auto), Tier 2 (Guarded Auto), Tier 3 (Human Approval Required), Ambiguous (Escalated)
        blast_radius_desc TEXT,
        proposed_action TEXT,
        remediation_command TEXT,
        rollback_command TEXT,
        verification_check TEXT,
        requires_human_approval INTEGER DEFAULT 0,
        approved_by TEXT,
        approval_timestamp TIMESTAMP,
        remediation_logs TEXT,
        verification_status TEXT, -- PENDING, VERIFIED_HEALTHY, VERIFICATION_FAILED
        rollback_triggered INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        resolved_at TIMESTAMP
    );
    """)

    # 5. ITIL Audit Logs & Change Records Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        change_id TEXT UNIQUE NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        incident_code TEXT NOT NULL,
        incident_title TEXT NOT NULL,
        actor TEXT NOT NULL, -- 'AI Autonomous Agent' or 'Human Operator: Babitha M / Eshwar'
        action_type TEXT NOT NULL, -- DIAGNOSIS, APPROVAL, REMEDIATION_EXECUTE, ROLLBACK_EXECUTE, KILL_SWITCH
        risk_tier TEXT NOT NULL,
        command_executed TEXT,
        blast_radius TEXT,
        outcome TEXT NOT NULL, -- SUCCESS, FAILED, ROLLED_BACK, ESCALATED, REJECTED
        itil_justification TEXT NOT NULL,
        verification_details TEXT
    );
    """)

    conn.commit()
    conn.close()

def seed_default_data():
    conn = get_db()
    cursor = conn.cursor()

    # Check if already seeded
    cursor.execute("SELECT COUNT(*) FROM safety_policies")
    if cursor.fetchone()[0] == 0:
        # Default Safety Policies & Guardrails
        policies = [
            ("kill_switch_active", "Emergency Kill Switch", "false", "Master kill-switch that instantly freezes all automated remediation actions across the cluster."),
            ("rate_limit_per_minute", "Action Rate Limiter", "5", "Maximum automated remediations allowed per minute to prevent runaway automation loops."),
            ("max_scaling_instances", "Max Queue Worker Instances", "10", "Hard upper limit when auto-scaling queue consumer workers to prevent resource starvation."),
            ("disk_safety_floor_gb", "Disk Safety Floor", "5.0", "Minimum free disk space buffer in GB below which high-risk escalation is forced."),
            ("tier1_auto_enabled", "Tier 1 (Low Risk) Auto-Execute", "true", "Automatically execute standard non-destructive fixes without waking a human."),
            ("tier2_auto_enabled", "Tier 2 (Medium Risk) Auto-Execute", "true", "Execute medium risk fixes with mandatory pre/post health check and automatic rollback."),
            ("tier3_requires_approval", "Tier 3 (High Risk) Human-in-the-Loop", "true", "Mandate explicit human authorization before executing actions that affect data or cluster state."),
            ("escalate_ambiguity", "Zero Guessing on Ambiguous Faults", "true", "Escalate to human engineer when fault cause is ambiguous or telemetry is contradictory.")
        ]
        cursor.executemany("INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES (?, ?, ?, ?)", policies)

    # Seed Live System Metrics
    cursor.execute("SELECT COUNT(*) FROM system_metrics")
    if cursor.fetchone()[0] == 0:
        metrics = [
            ("disk_usage_pct", "Root Disk Space (/dev/sda1)", 94.2, "%", 80.0, 90.0, "CRITICAL", "prod-srv-alpha"),
            ("worker_status", "Worker Pool Health (Worker-03)", 0.0, "State (0=Stuck, 1=Alive)", 0.5, 0.0, "CRITICAL", "prod-worker-03"),
            ("queue_backlog_depth", "Message Backlog (Orders Queue)", 48250, "msgs", 10000, 30000, "CRITICAL", "kafka-cluster-01"),
            ("ssl_cert_days", "SSL/TLS Certificate Validity", 2.0, "days", 14.0, 5.0, "CRITICAL", "api-gateway-edge"),
            ("cpu_utilization", "Cluster CPU Load Average", 42.5, "%", 75.0, 90.0, "OK", "k8s-node-pool-1"),
            ("memory_utilization", "Cluster RAM Usage", 58.3, "%", 80.0, 90.0, "OK", "k8s-node-pool-1")
        ]
        cursor.executemany("INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", metrics)

    # Seed the 10 Representative Runbooks
    cursor.execute("SELECT COUNT(*) FROM runbooks")
    if cursor.fetchone()[0] == 0:
        runbooks = [
            (
                "RB-01",
                "Disk Overflow: Rotatable Application Logs vs DB Core Dump",
                "Storage & Disk",
                "/var/log & Root Filesystem",
                "Disk usage > 90% on partition /dev/sda1",
                "Tier 1 (Low Risk) for Logs; Tier 3 (High Risk) for Core Dumps",
                "Local partition only. 0 downtime risk if logs; potential diagnostic data loss if core dumps.",
                "IF disk is full due to rotatable logs in /var/log/app/*.log, compress and archive older logs. IF disk is full due to mysql / kernel core dumps, DO NOT delete; escalate to Database/Infra team.",
                "find /var/log/app/ -name '*.log.[1-9]' -mtime +2 -exec gzip {} \\; && journalctl --vacuum-time=1d",
                "tar -xvf /var/log/app/backup_pre_cleanup.tar.gz -C /",
                "df -h / | awk 'NR==2 {gsub(\"%\", \"\"); if ($5 < 75) print \"PASS\"; else print \"FAIL\"}'",
                "Encodes runbook judgment: safely clears rotated logs down to 68% disk utilization while safeguarding core dumps."
            ),
            (
                "RB-02",
                "Background Process Stuck: Worker Thread Deadlock vs DB Saturation",
                "Compute & Processes",
                "Background Celery/Redis Worker Pool",
                "Worker heartbeat missed for > 180s, processing queue stalled",
                "Tier 1 (Low Risk) for Soft Thread Stutter; Tier 3 (High Risk) if Database Pool Exhausted",
                "Single worker node (Worker-03). Zero client impact if drain succeeds.",
                "IF worker thread is in deadlock but database connection pool is healthy, send graceful SIGTERM and restart. IF worker is waiting because Postgres active connections are 100%, DO NOT restart worker (prevents thundering herd); escalate immediately.",
                "systemctl restart celery-worker@worker-03.service && sleep 3 && systemctl status celery-worker@worker-03.service",
                "systemctl stop celery-worker@worker-03.service && systemctl start celery-worker@worker-03-fallback.service",
                "systemctl is-active celery-worker@worker-03.service",
                "Handles unresponsive asynchronous worker daemon with automated heartbeat verification."
            ),
            (
                "RB-03",
                "Growing Message Queue: Traffic Surge vs Poison Pill Message",
                "Messaging & Streaming",
                "Order Processing Kafka/RabbitMQ Queue",
                "Queue backlog exceeds 30,000 messages and consumer lag increases",
                "Tier 2 (Medium Risk) with max scaling boundary (Max 10 workers)",
                "Horizontal pod autoscaler. Risk of cloud compute cost overrun if unconstrained.",
                "IF consumer error rate is < 1% (pure traffic spike), scale queue consumers from 3 to 6 (within hard limit 10). IF consumer error rate > 50% (poison pill crashing workers), DO NOT scale; divert failing message to Dead-Letter Queue (DLQ).",
                "kubectl scale deployment/order-consumer --replicas=6 --namespace=orders",
                "kubectl scale deployment/order-consumer --replicas=3 --namespace=orders",
                "kubectl get deployment/order-consumer -o jsonpath='{.status.readyReplicas}'",
                "Prevents runaway scaling by enforcing strict policy limits (max 10 replicas) and poison pill routing."
            ),
            (
                "RB-04",
                "SSL/TLS Certificate Expiration & Key Rotation",
                "Security & Networking",
                "Ingress Edge Gateway & Load Balancer",
                "Certificate expiration date <= 7 days",
                "Tier 1 (Low Risk) if ACME challenge valid; Tier 3 (High Risk) if Root CA Drift",
                "Edge API Gateway TLS terminations. Zero downtime seamless cert reload.",
                "IF certificate is within 7 days of expiry and domain DNS verification succeeds, trigger automated certbot renewal and graceful nginx reload. IF certificate chain is corrupted or domain mismatch, escalate to Security lead.",
                "certbot renew --cert-name api.production.internal --quiet && nginx -s reload",
                "cp /etc/ssl/backup/last_known_good.crt /etc/ssl/certs/ && nginx -s reload",
                "openssl x509 -checkend 604800 -noout -in /etc/ssl/certs/api.production.internal.crt",
                "Automates non-destructive TLS certificate renewal with automated validation probe."
            ),
            (
                "RB-05",
                "Memory Leak in Microservice Container",
                "Containers & Kubernetes",
                "Payment Service Pods (cgroup memory limit)",
                "Container memory usage > 92% of limit, OOMKilled risk",
                "Tier 2 (Medium Risk) Rolling Canary Restart",
                "Single pod replica in a 5-pod cluster. Zero dropped transactions.",
                "IF pod memory leak is linear over 48h and other replicas are healthy, perform a rolling zero-downtime rollout restart. IF all replicas leak simultaneously within 5 minutes, suspect memory exploit / payload bug, escalate to Dev team.",
                "kubectl rollout restart deployment/payment-service --namespace=fintech",
                "kubectl rollout undo deployment/payment-service --namespace=fintech",
                "kubectl rollout status deployment/payment-service --timeout=60s",
                "Rolling restart one pod at a time while verifying readiness probes before proceeding."
            ),
            (
                "RB-06",
                "High CPU Runaway Script / Zombie Fork Bomb",
                "Compute & Host OS",
                "Data Analytics Batch Server",
                "Host CPU pegged at 99% for > 10 minutes",
                "Tier 3 (High Risk) - Requires Human Confirmation",
                "Can terminate uncommitted analytical data jobs.",
                "IF CPU usage is tied to rogue orphan Python process with PPID=1, terminate gently with SIGTERM, then SIGKILL if unresponsive. Verify process is not critical ETL pipeline.",
                "pkill -15 -f 'orphan_analytics_worker.py' || pkill -9 -f 'orphan_analytics_worker.py'",
                "systemctl restart analytics-scheduler.service",
                "pgrep -f 'orphan_analytics_worker.py' && echo 'FAIL' || echo 'PASS'",
                "Requires operator review to ensure critical batch processing is not inadvertently interrupted."
            ),
            (
                "RB-07",
                "Read-Only Filesystem Mount Due to SCSI I/O Timeout",
                "Storage & Kernel",
                "Shared NFS / Block Storage Volume",
                "Filesystem mounted read-only (ro) following I/O error",
                "Tier 3 (High Risk) - Ambiguous / Hardware Level",
                "Cluster-wide storage availability.",
                "Read-only mount often signals underlying SAN/SAN hardware failure or bad blocks. Blindly running 'mount -o remount,rw' can destroy corrupted sectors. Policy mandates Escalation.",
                "mount -o remount,rw /mnt/data-store && touch /mnt/data-store/.healthcheck",
                "mount -o remount,ro /mnt/data-store",
                "test -w /mnt/data-store",
                "Enforces policy: prevents catastrophic automation that corrupts database tables."
            ),
            (
                "RB-08",
                "Redis Cache Connection Pool Exhaustion",
                "Caching & DB",
                "Redis Session Cluster",
                "Connected clients > 95% of maxclients limit",
                "Tier 1 (Low Risk) Idle Connection Prune",
                "Redis connection state. Transparent to active web requests.",
                "IF connection pool is exhausted due to idle leaked TCP sockets (> 300s idle), execute timeout config and prune idle connections. Do NOT flush DB.",
                "redis-cli config set timeout 60 && redis-cli client kill type normal skipme yes",
                "redis-cli config set timeout 0",
                "redis-cli info clients | grep connected_clients",
                "Safely trims leaked client connections without dropping active transactions."
            ),
            (
                "RB-09",
                "DNS Resolver Cache Poisoning & Stale Lookup Drift",
                "Networking",
                "CoreDNS / Systemd-Resolved",
                "DNS lookup latency > 2500ms or resolving to loopback",
                "Tier 1 (Low Risk) Resolver Cache Flush",
                "Host DNS cache table.",
                "IF DNS resolution times out or returns transient NXDOMAIN for internal service discovery, flush local resolver cache and test upstream 1.1.1.1 / internal DNS.",
                "systemd-resolve --flush-caches && systemctl restart systemd-resolved",
                "cp /etc/resolv.conf.bak /etc/resolv.conf",
                "dig +short auth.production.internal @127.0.0.53",
                "Restores network reachability without touching application configs."
            ),
            (
                "RB-10",
                "API Ingress Gateway Packet Drop / SYN Flood Rate Limiting",
                "Security & Gateway",
                "HAProxy / Envoy Ingress Gateway",
                "Dropped TCP connections > 5% on external edge",
                "Tier 2 (Medium Risk) Dynamic WAF / IP Rate Limit Adjustment",
                "Public API ingress traffic. Potential to rate-limit abusive subnet.",
                "IF dropped packets are traced to abusive single IP range sending malformed requests, inject temporary iptables rate-limit jail for 15 minutes. Verify valid client SLA.",
                "iptables -I INPUT -p tcp --dport 443 -m connlimit --connlimit-above 50 -j REJECT",
                "iptables -D INPUT -p tcp --dport 443 -m connlimit --connlimit-above 50 -j REJECT",
                "curl -s -o /dev/null -w '%{http_code}' https://api.production.internal/healthz",
                "Applies bounded, time-limited edge rate-limiting with automated rollback guard."
            ),
            (
                "RB-UNC-01",
                "Uncritical: Routine Preventive Disk & Cache Hygiene (/tmp & 14-Day Archives)",
                "Storage & Hygiene",
                "/tmp & Inactive App Log Archives",
                "Off-peak schedule OR disk usage between 60% and 75% (Non-Emergency)",
                "Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)",
                "Zero (0%): Targets purely stale scratch/temporary files and inactive compressed logs. Zero risk to production binaries.",
                "IF disk usage is non-critical (< 75%) and contains stale temporary files older than 7 days, purge /tmp files and compress old logs silently. Do NOT wake or page on-call engineers.",
                "find /tmp -type f -name '*.tmp' -mtime +7 -delete && find /var/log/app/ -name '*.log.[1-9]' -mtime +3 -exec gzip {} \\; && journalctl --vacuum-size=500M",
                "touch /tmp/.maintenance_complete",
                "df -h / | awk 'NR==2 {print \"PASS_DISK_HEALTHY\"}'",
                "Non-critical routine preventive hygiene executed autonomously during low-traffic hours."
            ),
            (
                "RB-UNC-02",
                "Uncritical: Routine Worker Pool Heap Trim & Soft Garbage Collection",
                "Compute & Memory Hygiene",
                "Background Worker Pool (Worker-03)",
                "Worker processed > 2,000 tasks OR scheduled off-peak idle lull (Worker Healthy)",
                "Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)",
                "Zero (0%): Soft reload occurs between task intervals. Zero dropped tasks or transaction failures.",
                "IF worker is healthy (alive) but has minor heap memory fragmentation after handling thousands of jobs, trigger graceful worker reload during idle gap. Fully autonomous with zero downtime.",
                "systemctl reload-or-restart celery-worker@worker-03.service",
                "systemctl status celery-worker@worker-03.service",
                "systemctl is-active celery-worker@worker-03.service",
                "Routine memory defragmentation for long-running worker processes."
            ),
            (
                "RB-UNC-03",
                "Uncritical: Off-Peak Minor Queue Backlog Balancing",
                "Messaging & Queues",
                "Order Processing Message Queue",
                "Queue backlog between 200 and 1,000 messages (Minor Transient Ripple)",
                "Tier 1 (Uncritical - Silent Safe Auto)",
                "Low (< 5%): Dynamically scales 1 standby consumer pod within safe bounds.",
                "IF message backlog is slightly elevated during morning burst (< 1,000 messages) and consumer error rate is 0%, spin up 1 standby consumer pod to keep latency sub-200ms. Handled silently.",
                "kubectl scale deployment/order-consumer --replicas=4 --namespace=orders",
                "kubectl scale deployment/order-consumer --replicas=3 --namespace=orders",
                "kubectl get deployment/order-consumer -o jsonpath='{.status.readyReplicas}'",
                "Off-peak queue balancing to smooth out minor order ripples without alerting staff."
            ),
            (
                "RB-UNC-04",
                "Uncritical: Preventive SSL/TLS Certificate Audit & OCSP Stapling (45-Day Health Check)",
                "Security & Auditing",
                "Edge API Gateway Ingress",
                "Scheduled weekly audit OR certificate validity at 45 days remaining",
                "Tier 0 / Tier 1 (Uncritical - Preventive Health Audit)",
                "Zero (0%): Non-destructive read-only cryptographic validation.",
                "IF certificate validity is well within safety thresholds (> 30 days remaining), execute routine cryptographic trust chain verification and pre-renewal handshake test. No human action required.",
                "openssl s_client -servername api.production.internal -connect 127.0.0.1:443 </dev/null 2>/dev/null | openssl x509 -noout -dates && echo 'AUDIT_VERIFIED_VALID'",
                "echo 'AUDIT_NOOP'",
                "openssl x509 -checkend 2592000 -noout -in /etc/ssl/certs/api.production.internal.crt",
                "Proactive, non-urgent certificate health probe ensuring zero unexpected expiration."
            )
        ]
        cursor.executemany("""
        INSERT INTO runbooks (
            runbook_id, title, category, target_subsystem, trigger_condition,
            safe_action_tier, blast_radius, judgment_rules, remediation_command,
            rollback_command, verification_check, documentation
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, runbooks)

    # Seed Initial Demo Incidents matching Figure 3
    cursor.execute("SELECT COUNT(*) FROM incidents")
    if cursor.fetchone()[0] == 0:
        demo_incidents = [
            (
                "INC-8091",
                "Disk Overflow on Primary Application Node (/dev/sda1)",
                "disk_overflow",
                "prod-srv-alpha",
                "CRITICAL",
                "DETECTED",
                "detect",
                json.dumps({"disk_usage": "94.2%", "partition": "/dev/sda1", "dir": "/var/log/app", "largest_file": "app-access.log.2 (4.2GB)"}),
                "Rotatable nginx and application stdout logs uncompressed over 14 days.",
                "Analysis confirms /var/log/app contains 18GB of compressable log files. No core dumps or mysql database directories affected. Eligible for Tier 1 safe automation within policy limits.",
                "Tier 1 (Low Risk - Safe Auto)",
                "Local /var/log partition only. Zero service downtime. Reversible from backup archive.",
                "Compress uncompressed rotated logs and vacuum system journal to reclaim 18GB.",
                "find /var/log/app/ -name '*.log.[1-9]' -mtime +2 -exec gzip {} \\; && journalctl --vacuum-time=1d",
                "tar -xvf /var/log/app/backup_pre_cleanup.tar.gz -C /",
                0,
                None,
                None,
                None,
                "PENDING",
                0
            ),
            (
                "INC-8092",
                "Background Celery Worker Deadlock (Worker-03)",
                "worker_stuck",
                "prod-worker-03",
                "CRITICAL",
                "AWAITING_APPROVAL",
                "approval",
                json.dumps({"worker_id": "worker-03", "last_heartbeat": "240s ago", "db_connections": "98/100 (HIGH)"}),
                "Worker thread stuck in semaphore wait, but database connection pool is 98% saturated.",
                "CRITICAL RUNBOOK JUDGMENT: While restarting worker would clear the deadlock, the database connection pool is at 98% saturation. An automated restart will spawn 16 new DB connections, triggering a thundering herd collapse. Requires Human Approval to authorize graceful connection drain first.",
                "Tier 3 (High Risk - Human Approval Required)",
                "Worker Pool + Database connection pool (1,200 active users). High blast radius.",
                "Gracefully drain idle DB connections before initiating rolling restart of worker-03.",
                "python3 /scripts/drain_idle_db_conns.py && systemctl restart celery-worker@worker-03.service",
                "systemctl stop celery-worker@worker-03.service && systemctl start celery-worker@worker-03-fallback.service",
                1,
                None,
                None,
                None,
                "PENDING",
                0
            )
        ]
        cursor.executemany("""
        INSERT INTO incidents (
            incident_code, title, fault_type, server_node, severity, status,
            current_step, telemetry_snapshot, root_cause, ai_reasoning,
            risk_tier, blast_radius_desc, proposed_action, remediation_command,
            rollback_command, requires_human_approval, approved_by,
            approval_timestamp, remediation_logs, verification_status, rollback_triggered
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, demo_incidents)

    # Seed Initial ITIL Audit Logs
    cursor.execute("SELECT COUNT(*) FROM audit_logs")
    if cursor.fetchone()[0] == 0:
        initial_logs = [
            (
                "CHG-1001",
                "INC-8088",
                "Automated SSL Certificate Renewal (Routine Expiry)",
                "AI Autonomous Agent",
                "REMEDIATION_EXECUTE",
                "Tier 1 (Low Risk)",
                "certbot renew --cert-name api.production.internal --quiet",
                "Zero edge gateway downtime. ACME HTTP-01 challenge verified.",
                "SUCCESS",
                "ITIL Standard Change: Pre-approved low-risk operational renewal within policy window.",
                "TLS certificate expiration extended to +90 days. Health probe 200 OK."
            ),
            (
                "CHG-1002",
                "INC-8089",
                "Redis Cache Idle Connection Pool Prune",
                "AI Autonomous Agent",
                "REMEDIATION_EXECUTE",
                "Tier 1 (Low Risk)",
                "redis-cli config set timeout 60 && redis-cli client kill type normal skipme yes",
                "Redis cache nodes only. Zero key evictions.",
                "SUCCESS",
                "ITIL Emergency Action: Reclaimed 850 leaked TCP sockets; connection pool returned to 22%.",
                "Active web sessions untouched. Latency 1.2ms."
            )
        ]
        cursor.executemany("""
        INSERT INTO audit_logs (
            change_id, incident_code, incident_title, actor, action_type,
            risk_tier, command_executed, blast_radius, outcome,
            itil_justification, verification_details
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, initial_logs)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    seed_default_data()
    print("Database initialized and seeded successfully.")

import os

APP_PATH = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\app.py"

with open(APP_PATH, "r", encoding="utf-8") as f:
    text = f.read()

start_marker = '    if fault_type == "disk_overflow":'
end_marker = '    cursor.execute("""\n        INSERT INTO incidents ('

p1 = text.find(start_marker)
p2 = text.find(end_marker)

new_fault_injection_logic = """    if fault_type == "disk_overflow":
        if sub_type in ["routine_hygiene", "uncritical_logs", "uncritical"]:
            title = "Uncritical: Developer Sandbox & Docker Build Scratch Hygiene (54.2% Disk)"
            server_node = "ci-runner-pool-02"
            severity = "LOW"
            telemetry = {
                "disk_usage": "54.2%",
                "partition": "/tmp/builds",
                "free_space": "92.0 GB free",
                "largest_file": "docker_layer_cached_7182.tmp (1.4GB)",
                "sub_type": "routine_hygiene",
                "is_uncritical": True,
                "notes": "Routine off-peak maintenance: 1.4GB of temporary scratch build layers older than 14 days. Zero blast radius."
            }
            cursor.execute("UPDATE system_metrics SET value = 54.2, status = 'OK' WHERE metric_key = 'disk_usage_pct'")
        elif sub_type in ["core_dump", "critical_disk"]:
            title = "CRITICAL: PostgreSQL Primary WAL Storage Full (99.4% Capacity - 124MB Left!)"
            server_node = "prod-db-primary-01"
            severity = "CRITICAL"
            telemetry = {
                "disk_usage": "99.4%",
                "partition": "/var/lib/postgresql/pg_wal",
                "free_space": "124 MB remaining",
                "largest_file": "0000000100000A1B0000002F (16MB x 1,840 segments)",
                "sub_type": "core_dump",
                "notes": "Postgres WAL replication bottleneck. Only 124MB left before emergency PANIC shutdown! Deleting WAL breaks replica cluster."
            }
            cursor.execute("UPDATE system_metrics SET value = 99.4, status = 'CRITICAL' WHERE metric_key = 'disk_usage_pct'")
        else:
            title = "Warning: Nginx Reverse Proxy Static Cache Exceeded (88.5% Capacity)"
            server_node = "edge-proxy-01"
            severity = "WARN"
            telemetry = {
                "disk_usage": "88.5%",
                "partition": "/var/cache/nginx",
                "free_space": "18.2 GB remaining",
                "largest_file": "proxy_cache_asset_pack_v4.tar (4.8GB)",
                "sub_type": "logs",
                "notes": "Cache storage high-water mark reached. Safe to purge expired cached static objects without downtime."
            }
            cursor.execute("UPDATE system_metrics SET value = 88.5, status = 'WARN' WHERE metric_key = 'disk_usage_pct'")

    elif fault_type == "worker_stuck":
        if sub_type in ["routine_gc_trim", "uncritical_worker", "uncritical"]:
            title = "Uncritical: Image Worker Heap Compaction & Soft Recycle (15,400 Tasks)"
            server_node = "media-worker-05"
            severity = "LOW"
            telemetry = {
                "worker_id": "media-worker-05 (PID 7102)",
                "last_heartbeat": "1s ago (ACTIVE)",
                "tasks_completed": 15400,
                "memory_fragmentation": "14.2%",
                "sub_type": "routine_gc_trim",
                "is_uncritical": True,
                "notes": "Worker fully healthy. Soft graceful heap reload during idle gap between image batches."
            }
            cursor.execute("UPDATE system_metrics SET value = 1.0, status = 'OK' WHERE metric_key = 'worker_status'")
        elif sub_type in ["db_exhaustion", "critical_worker"]:
            title = "CRITICAL: Payment Reconciliation Engine Threadlock (8,400 In-Flight Settlements)"
            server_node = "fintech-recon-01"
            severity = "CRITICAL"
            telemetry = {
                "worker_id": "py-recon-daemon (PID 4092)",
                "last_heartbeat": "340s ago (DEADLOCKED)",
                "in_flight_transactions": 8400,
                "transaction_volume": "$1,420,000 USD",
                "db_connections": "99/100 (SATURATED)",
                "sub_type": "db_exhaustion",
                "notes": "Thread deadlock waiting on Redis cluster lock. Killing worker will cause duplicate customer credit card charges!"
            }
            cursor.execute("UPDATE system_metrics SET value = 0.0, status = 'CRITICAL' WHERE metric_key = 'worker_status'")
        else:
            title = "Warning: Email Dispatcher Celery Worker Hung on SendGrid HTTP Timeout"
            server_node = "email-worker-02"
            severity = "HIGH"
            telemetry = {
                "worker_id": "email-worker-02 (PID 1840)",
                "last_heartbeat": "310s ago (IDLE_TIMEOUT)",
                "db_connections": "12/100 (HEALTHY)",
                "sub_type": "deadlock_clean",
                "notes": "Hung in external SendGrid socket wait. Zero financial risk. Database pool healthy. Safe for graceful SIGTERM restart."
            }
            cursor.execute("UPDATE system_metrics SET value = 0.0, status = 'CRITICAL' WHERE metric_key = 'worker_status'")

    elif fault_type == "queue_growth":
        if sub_type in ["routine_queue_balance", "uncritical_queue", "uncritical"]:
            title = "Uncritical: Clickstream Analytics Minor Backlog Ripple (850 msgs)"
            server_node = "kafka-analytics-pool"
            severity = "LOW"
            telemetry = {
                "queue_name": "clicks.telemetry.raw",
                "queue_depth": 850,
                "consumer_error_rate": "0.0%",
                "sub_type": "routine_queue_balance",
                "is_uncritical": True,
                "notes": "Transient morning ripple. Activate 1 standby consumer to maintain sub-150ms processing SLA."
            }
            cursor.execute("UPDATE system_metrics SET value = 850.0, status = 'OK' WHERE metric_key = 'queue_backlog_depth'")
        elif sub_type in ["poison_pill", "critical_queue"]:
            title = "CRITICAL: Fraud Detection Kafka Stream Backlog (142,800 msgs - 92.4% Error Rate)"
            server_node = "kafka-cluster-frauddetection"
            severity = "CRITICAL"
            telemetry = {
                "queue_name": "fraud.transactions.v2",
                "queue_depth": 142800,
                "consumer_error_rate": "92.4%",
                "crash_signature": "JSONDecodeError: Unterminated string at offset 402911",
                "compute_waste_risk": "$4,200/hr in cloud compute",
                "sub_type": "poison_pill",
                "notes": "Poison pill crashing consumer pods in infinite loop. Scaling pods burns compute with 0 progress! Must isolate bad offset to DLQ."
            }
            cursor.execute("UPDATE system_metrics SET value = 142800.0, status = 'CRITICAL' WHERE metric_key = 'queue_backlog_depth'")
        else:
            title = "Warning: Flash Sale Order Checkout Queue Influx (28,500 msgs)"
            server_node = "kafka-cluster-orders"
            severity = "HIGH"
            telemetry = {
                "queue_name": "checkout.flash.events",
                "queue_depth": 28500,
                "consumer_error_rate": "0.02%",
                "active_pods": 4,
                "sub_type": "traffic_surge",
                "notes": "Clean high volume promotional traffic surge. Safe to autoscale from 4 to 8 pods within policy limit (max 10)."
            }
            cursor.execute("UPDATE system_metrics SET value = 28500.0, status = 'WARN' WHERE metric_key = 'queue_backlog_depth'")

    elif fault_type == "ssl_expiry":
        if sub_type in ["routine_audit_check", "uncritical_ssl", "uncritical"]:
            title = "Uncritical: Internal Microservice Mutual TLS Health Audit (58.0 Days)"
            server_node = "mTLS-auth.internal"
            severity = "INFO"
            telemetry = {
                "domain": "mTLS-auth.internal",
                "days_remaining": 58.0,
                "ca_trust_status": "VALID_INTERNAL_CA",
                "sub_type": "routine_audit_check",
                "is_uncritical": True,
                "notes": "Proactive cryptographic handshake cipher audit & OCSP check. Zero service changes."
            }
            cursor.execute("UPDATE system_metrics SET value = 58.0, status = 'OK' WHERE metric_key = 'ssl_cert_days'")
        elif sub_type in ["root_ca_broken", "critical_ssl"]:
            title = "CRITICAL: Edge API Gateway TLS Root CA Revocation (6 Hours Remaining!)"
            server_node = "api.globalpay.com"
            severity = "CRITICAL"
            telemetry = {
                "domain": "api.globalpay.com",
                "hours_remaining": 6.2,
                "days_remaining": 0.25,
                "ca_trust_status": "REVOKED / INTERMEDIATE CRL DRIFT",
                "sub_type": "root_ca_broken",
                "notes": "Intermediate CA key compromised & revoked upstream! Automated ACME renewals will fail. Operator must manually import re-signed bundle."
            }
            cursor.execute("UPDATE system_metrics SET value = 0.25, status = 'CRITICAL' WHERE metric_key = 'ssl_cert_days'")
        else:
            title = "Warning: Customer Web Portal TLS Certificate Expiring (4.5 Days)"
            server_node = "portal.production.io"
            severity = "WARN"
            telemetry = {
                "domain": "portal.production.io",
                "days_remaining": 4.5,
                "ca_trust_status": "VALID_LETS_ENCRYPT",
                "sub_type": "routine_renew",
                "notes": "Standard renewal policy window. DNS HTTP-01 challenge ready. Safe for automated key rotation and nginx reload."
            }
            cursor.execute("UPDATE system_metrics SET value = 4.5, status = 'WARN' WHERE metric_key = 'ssl_cert_days'")
    else:
        title = f"Operational Anomaly Detected: {fault_type}"
        server_node = "prod-node-01"
        severity = "MEDIUM"
        telemetry = {"custom_event": fault_type, "timestamp": created_at}

"""

if p1 != -1 and p2 != -1:
    updated = text[:p1] + new_fault_injection_logic + text[p2:]
    with open(APP_PATH, "w", encoding="utf-8") as f:
        f.write(updated)
    print("app.py fault injection logic successfully updated with distinct scenario numbers!")
else:
    print(f"Markers not found in app.py: p1={p1}, p2={p2}")

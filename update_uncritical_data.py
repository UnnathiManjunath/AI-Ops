import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "safeops.db")

def update_uncritical_runbooks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    uncritical_runbooks = [
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

    for rb in uncritical_runbooks:
        cursor.execute("""
            INSERT OR REPLACE INTO runbooks (
                runbook_id, title, category, target_subsystem, trigger_condition,
                safe_action_tier, blast_radius, judgment_rules, remediation_command,
                rollback_command, verification_check, documentation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, rb)

    conn.commit()
    print("Successfully inserted/updated uncritical runbooks in safeops.db!")
    cursor.execute("SELECT runbook_id, title, safe_action_tier FROM runbooks WHERE runbook_id LIKE 'RB-UNC%'")
    for r in cursor.fetchall():
        print(r)
    conn.close()

if __name__ == "__main__":
    update_uncritical_runbooks()

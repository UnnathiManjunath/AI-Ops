import json
import sqlite3
import os

PROJECT_DIR = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai"

# =========================================================================
# 1. E-COMMERCE & FOOD DELIVERY DATASET (QUICKCART)
# =========================================================================
ecommerce_dataset = {
    "metadata": {
        "dataset_name": "QuickCart Global E-Commerce & Food Delivery Cloud",
        "domain": "E-Commerce, Food Delivery & Real-Time Logistics",
        "system_id": "quickcart-prod-cluster-01",
        "version": "3.1.0-ECOMMERCE",
        "team": "Idea Ignitors (XH-23) - Cynefian Hackathon"
    },
    "system_metrics": [
        {"metric_key": "disk_usage_pct", "name": "QuickCart Invoicing Storage (/var/data/quickcart)", "value": 51.4, "unit": "%", "threshold_warn": 80.0, "threshold_crit": 95.0, "status": "OK", "server_node": "quickcart-invoice-01"},
        {"metric_key": "worker_status", "name": "Rider Auto-Dispatch Pool Health", "value": 1.0, "unit": "State (0=Locked, 1=Alive)", "threshold_warn": 0.5, "threshold_crit": 0.0, "status": "OK", "server_node": "rider-dispatch-pool"},
        {"metric_key": "queue_backlog_depth", "name": "Live Rider GPS Tracking Queue", "value": 620.0, "unit": "msgs", "threshold_warn": 10000.0, "threshold_crit": 50000.0, "status": "OK", "server_node": "kafka-quickcart-edge"},
        {"metric_key": "ssl_cert_days", "name": "Restaurant Partner Gateway TLS Validity", "value": 62.0, "unit": "days", "threshold_warn": 14.0, "threshold_crit": 5.0, "status": "OK", "server_node": "kitchen.quickcart.com"},
        {"metric_key": "cpu_utilization", "name": "E-Commerce Cluster CPU Load", "value": 31.2, "unit": "%", "threshold_warn": 75.0, "threshold_crit": 90.0, "status": "OK", "server_node": "k8s-quickcart-nodes"},
        {"metric_key": "memory_utilization", "name": "E-Commerce Cluster RAM Usage", "value": 46.8, "unit": "%", "threshold_warn": 80.0, "threshold_crit": 90.0, "status": "OK", "server_node": "k8s-quickcart-nodes"}
    ],
    "safety_policies": [
        {"policy_key": "kill_switch_active", "policy_name": "Emergency Master Kill Switch", "value": "false", "description": "Instant freeze for all QuickCart automation threads across cluster."},
        {"policy_key": "rate_limit_per_minute", "policy_name": "Action Rate Limiter", "value": "5", "description": "Maximum 5 automated remediations per minute to prevent runaway loops."},
        {"policy_key": "max_scaling_instances", "policy_name": "Max Delivery Consumer Pods", "value": "10", "description": "Strict cloud compute ceiling to prevent unexpected cloud billing spikes ($3,800/hr risk)."},
        {"policy_key": "disk_safety_floor_gb", "policy_name": "Invoice Safety Floor", "value": "5.0", "description": "Minimum free disk space buffer below which high-risk escalation is mandated."},
        {"policy_key": "tier1_auto_enabled", "policy_name": "Tier 1 Safe Auto-Remediation", "value": "true", "description": "Autonomous execution of non-destructive fixes without rider disruption."},
        {"policy_key": "tier3_requires_approval", "policy_name": "Tier 3 Human Authorization Gate", "value": "true", "description": "Mandatory human sign-off before modifying active orders or payment channels."}
    ],
    "runbooks": [
        {
            "runbook_id": "QC-DISK-CRIT",
            "title": "QuickCart Critical: Customer Order Invoicing & Tax Ledger Partition Full (98.7%)",
            "category": "E-Commerce Storage",
            "target_subsystem": "/var/data/quickcart/invoices",
            "trigger_condition": "Invoice partition disk usage > 98% (Only 450MB remaining!)",
            "safe_action_tier": "Tier 3 (High Risk - Human Approval Required)",
            "blast_radius": "CRITICAL: Complete checkout checkout block + database write lock.",
            "judgment_rules": "IF invoice partition is at 98.7%, customer orders cannot be confirmed. DO NOT delete invoices; snapshot older tax records to S3 glacier storage with human sign-off.",
            "remediation_command": "aws s3 sync /var/data/quickcart/invoices/2025/ s3://quickcart-tax-cold/ && find /var/data/quickcart/invoices/2025/ -type f -delete",
            "rollback_command": "aws s3 sync s3://quickcart-tax-cold/ /var/data/quickcart/invoices/2025/ || true",
            "verification_check": "df -h /var/data/quickcart/invoices | awk 'NR==2 {gsub(\"%\", \"\"); if ($5 < 80) print \"PASS\"; else print \"FAIL\"}'",
            "documentation": "Protects tax invoices and fiscal compliance while restoring checkout operations."
        },
        {
            "runbook_id": "QC-DISK-WARN",
            "title": "QuickCart Warning: Delivery Rider GPS Location Telemetry Log Overflow (89.2%)",
            "category": "E-Commerce Storage",
            "target_subsystem": "/var/log/rider_gps",
            "trigger_condition": "GPS location log usage > 85%",
            "safe_action_tier": "Tier 1 (Low Risk - Safe Auto)",
            "blast_radius": "LOW: Rider telemetry logs only. Zero customer order disruption.",
            "judgment_rules": "IF GPS log partition exceeds 85%, compress and archive raw breadcrumbs older than 48h to reclaim 34 GB. Safe for autonomous execution.",
            "remediation_command": "find /var/log/rider_gps/ -name '*.trace' -mtime +2 -exec gzip {} \\; && journalctl --vacuum-time=1d",
            "rollback_command": "find /var/log/rider_gps/ -name '*.trace.gz' -exec gunzip {} \\;",
            "verification_check": "df -h /var/log/rider_gps | awk 'NR==2 {gsub(\"%\", \"\"); if ($5 < 75) print \"PASS\"; else print \"FAIL\"}'",
            "documentation": "Compresses old delivery rider GPS traces to reclaim 34 GB safely."
        },
        {
            "runbook_id": "QC-DISK-UNC",
            "title": "QuickCart Uncritical: Restaurant Menu Image Preview Cache Hygiene (51.4%)",
            "category": "E-Commerce Hygiene",
            "target_subsystem": "/var/cache/menu_renders",
            "trigger_condition": "Off-peak schedule OR cache between 45% and 60%",
            "safe_action_tier": "Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)",
            "blast_radius": "ZERO (0%): Purely temporary restaurant menu preview images.",
            "judgment_rules": "IF disk utilization is non-critical (51.4%), prune stale restaurant dish thumbnails silently without waking engineers.",
            "remediation_command": "find /var/cache/menu_renders -type f -mtime +14 -delete",
            "rollback_command": "touch /var/cache/menu_renders/.maintenance_complete",
            "verification_check": "df -h /var/cache/menu_renders | awk 'NR==2 {print \"PASS_DISK_HEALTHY\"}'",
            "documentation": "Routine off-peak menu image thumbnail garbage collection."
        },
        {
            "runbook_id": "QC-WORKER-CRIT",
            "title": "QuickCart Critical: Live Rider Auto-Dispatch Engine Threadlock (3,420 Orders Waiting!)",
            "category": "E-Commerce Logistics",
            "target_subsystem": "rider-dispatch-daemon",
            "trigger_condition": "Dispatch daemon locked and pending orders > 3,000",
            "safe_action_tier": "Tier 3 (High Risk - Human Approval Required)",
            "blast_radius": "HIGH: 3,420 hungry customer deliveries + rider dispatch queue.",
            "judgment_rules": "IF dispatch daemon is deadlocked with 3,420 active orders, DO NOT kill worker process (prevents duplicate rider dispatch and order loss). Human approval required to pause order ingress before restart.",
            "remediation_command": "python3 /opt/quickcart/scripts/drain_active_rider_locks.py && systemctl restart rider-dispatch-daemon.service",
            "rollback_command": "systemctl restart rider-dispatch-daemon.service",
            "verification_check": "systemctl is-active rider-dispatch-daemon.service",
            "documentation": "Safeguards live food delivery rider assignment against double allocation."
        },
        {
            "runbook_id": "QC-WORKER-WARN",
            "title": "QuickCart Warning: Promotional WhatsApp / SMS Notification Worker Stalled (280s)",
            "category": "E-Commerce Notifications",
            "target_subsystem": "promo-sender-03",
            "trigger_condition": "Worker heartbeat missed for > 250s (Twilio socket wait)",
            "safe_action_tier": "Tier 1 (Low Risk - Safe Auto)",
            "blast_radius": "LOW: Marketing notification queue only. Zero customer order or payment risk.",
            "judgment_rules": "IF worker is hung in external Twilio gateway timeout, perform graceful SIGTERM restart with automatic notification retry.",
            "remediation_command": "systemctl restart celery-worker@promo-sender-03.service",
            "rollback_command": "systemctl restart celery-worker@promo-sender-03-fallback.service",
            "verification_check": "systemctl is-active celery-worker@promo-sender-03.service",
            "documentation": "Restores marketing notification worker safely with message requeue."
        },
        {
            "runbook_id": "QC-WORKER-UNC",
            "title": "QuickCart Uncritical: Customer Loyalty Points Calculator Soft Recycle (25,000 Users)",
            "category": "E-Commerce Compute",
            "target_subsystem": "loyalty-calc-01",
            "trigger_condition": "Worker processed > 20,000 users (Worker Healthy)",
            "safe_action_tier": "Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)",
            "blast_radius": "ZERO (0%): Soft reload occurs between batch calculations.",
            "judgment_rules": "IF loyalty worker is healthy but has minor heap fragmentation, trigger graceful reload during off-peak lull.",
            "remediation_command": "systemctl reload-or-restart celery-worker@loyalty-calc-01.service",
            "rollback_command": "systemctl status celery-worker@loyalty-calc-01.service",
            "verification_check": "systemctl is-active celery-worker@loyalty-calc-01.service",
            "documentation": "Defragments Python heap memory on loyalty points batch workers."
        },
        {
            "runbook_id": "QC-QUEUE-CRIT",
            "title": "QuickCart Critical: Live Rider Location Kafka Poison Pill Crash (184,000 msgs - 88.2% Err)",
            "category": "E-Commerce Streaming",
            "target_subsystem": "riders.gps.stream",
            "trigger_condition": "Queue backlog > 100,000 and consumer error rate > 80%",
            "safe_action_tier": "Tier 3 (High Risk - Human Approval Required)",
            "blast_radius": "HIGH: Delivery ETA accuracy and $3,800/hr cloud compute burn.",
            "judgment_rules": "IF consumer error rate is > 80% (malformed geofence coordinate crashing pods), DO NOT scale pods (prevents $3,800/hr compute burn); divert bad offset to DLQ with human sign-off.",
            "remediation_command": "kafka-consumer-groups --bootstrap-server kafka:9092 --group rider-gps --topic riders.gps.stream --reset-offsets --to-offset 891043 --execute",
            "rollback_command": "kafka-consumer-groups --bootstrap-server kafka:9092 --group rider-gps --topic riders.gps.stream --reset-offsets --to-offset 891042 --execute",
            "verification_check": "echo PASS_DLQ_ROUTED",
            "documentation": "Quarantines bad geofence payloads to unblock rider location tracking."
        },
        {
            "runbook_id": "QC-QUEUE-WARN",
            "title": "QuickCart Warning: Midnight Biryani Flash Sale Checkout Surge (32,400 msgs)",
            "category": "E-Commerce Scaling",
            "target_subsystem": "orders.checkout.live",
            "trigger_condition": "Queue backlog > 20,000 and error rate < 0.1%",
            "safe_action_tier": "Tier 2 (Guarded Auto - Within Policy Limits)",
            "blast_radius": "MEDIUM: Kubernetes consumer deployment. Capped at max 10 pods.",
            "judgment_rules": "IF error rate < 0.1% (clean flash sale traffic), autoscale consumers from 3 to 7 pods within policy limit 10.",
            "remediation_command": "kubectl scale deployment/order-consumer --replicas=7 --namespace=orders",
            "rollback_command": "kubectl scale deployment/order-consumer --replicas=3 --namespace=orders",
            "verification_check": "kubectl get deployment/order-consumer -o jsonpath='{.status.readyReplicas}'",
            "documentation": "Autoscales checkout consumers to drain promotion rush smoothly."
        },
        {
            "runbook_id": "QC-QUEUE-UNC",
            "title": "QuickCart Uncritical: Restaurant Review Notification Queue Ripple (620 msgs)",
            "category": "E-Commerce Queues",
            "target_subsystem": "restaurant.reviews",
            "trigger_condition": "Backlog between 400 and 1,000 messages (Minor Transient Ripple)",
            "safe_action_tier": "Tier 1 (Uncritical - Silent Safe Auto)",
            "blast_radius": "LOW (< 5%): Spins up 1 standby consumer container.",
            "judgment_rules": "IF backlog has minor morning ripple (620 msgs), activate 1 standby pod to maintain sub-150ms latency.",
            "remediation_command": "kubectl scale deployment/order-consumer --replicas=4 --namespace=orders",
            "rollback_command": "kubectl scale deployment/order-consumer --replicas=3 --namespace=orders",
            "verification_check": "kubectl get deployment/order-consumer -o jsonpath='{.status.readyReplicas}'",
            "documentation": "Smooths out transient review notifications silently."
        },
        {
            "runbook_id": "QC-SSL-CRIT",
            "title": "QuickCart Critical: Restaurant Kitchen Gateway Root CA Revocation (4 Hours Left!)",
            "category": "E-Commerce Security",
            "target_subsystem": "kitchen.quickcart.com",
            "trigger_condition": "Certificate validity < 12 hours and CA revoked upstream",
            "safe_action_tier": "Tier 3 (High Risk - Human Approval Required)",
            "blast_radius": "CRITICAL: Restaurant order transmission and live kitchen displays.",
            "judgment_rules": "IF intermediate CA is revoked upstream, automated ACME renewal cannot succeed. Escalate immediately to Security Ops Lead for manual re-pinning.",
            "remediation_command": "update-ca-certificates --fresh && nginx -s reload",
            "rollback_command": "cp /etc/ssl/backup/last_known_good.crt /etc/ssl/certs/ && nginx -s reload",
            "verification_check": "openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/kitchen.quickcart.com.crt",
            "documentation": "Prevents kitchen order tablets from disconnecting due to untrusted certificates."
        },
        {
            "runbook_id": "QC-SSL-WARN",
            "title": "QuickCart Warning: Mobile App Public Gateway TLS Expiring (3.8 Days)",
            "category": "E-Commerce Ingress",
            "target_subsystem": "api.quickcart.com",
            "trigger_condition": "Certificate validity <= 5 days (ACME DNS valid)",
            "safe_action_tier": "Tier 1 (Low Risk - Safe Auto)",
            "blast_radius": "LOW: Public Ingress Gateway. Zero dropped socket connections.",
            "judgment_rules": "IF certificate is within 5 days of expiry and DNS records valid, trigger automated certbot renewal and seamless nginx reload.",
            "remediation_command": "certbot renew --cert-name api.quickcart.com --quiet && nginx -s reload",
            "rollback_command": "cp /etc/ssl/backup/last_known_good.crt /etc/ssl/certs/ && nginx -s reload",
            "verification_check": "openssl x509 -checkend 604800 -noout -in /etc/ssl/certs/api.quickcart.com.crt",
            "documentation": "Automated seamless TLS rotation for public mobile app ingress."
        },
        {
            "runbook_id": "QC-SSL-UNC",
            "title": "QuickCart Uncritical: Warehouse Logistics Mutual TLS Health Audit (62.0 Days)",
            "category": "E-Commerce Auditing",
            "target_subsystem": "warehouse-auth.internal",
            "trigger_condition": "Scheduled audit OR certificate validity at 62 days remaining",
            "safe_action_tier": "Tier 0 / Tier 1 (Uncritical - Preventive Health Audit)",
            "blast_radius": "ZERO (0%): Read-only cryptographic handshake validation probe.",
            "judgment_rules": "IF certificate validity is healthy (62 days remaining), execute routine cryptographic trust check. No human action required.",
            "remediation_command": "openssl s_client -servername warehouse-auth.internal -connect 127.0.0.1:443 </dev/null 2>/dev/null | openssl x509 -noout -dates && echo 'AUDIT_VERIFIED_VALID'",
            "rollback_command": "echo 'AUDIT_NOOP'",
            "verification_check": "openssl x509 -checkend 2592000 -noout -in /etc/ssl/certs/warehouse-auth.internal.crt",
            "documentation": "Proactive cryptographic validity audit on warehouse logistics mTLS."
        }
    ]
}

# =========================================================================
# 2. HEALTHCARE & MEDICAL ICU DATASET (LIFECARE)
# =========================================================================
healthcare_dataset = {
    "metadata": {
        "dataset_name": "LifeCare Hospital & Medical ICU Patient Cloud",
        "domain": "Hospital Healthcare, Patient Vitals & Emergency EMS",
        "system_id": "lifecare-icu-cluster-04",
        "version": "3.1.0-HEALTHCARE",
        "team": "Idea Ignitors (XH-23) - Cynefian Hackathon"
    },
    "system_metrics": [
        {"metric_key": "disk_usage_pct", "name": "ICU Cardiac Waveform Storage (/var/data/icu)", "value": 48.2, "unit": "%", "threshold_warn": 80.0, "threshold_crit": 95.0, "status": "OK", "server_node": "icu-cardiac-srv-01"},
        {"metric_key": "worker_status", "name": "Emergency Ambulance Dispatch Health", "value": 1.0, "unit": "State (0=Locked, 1=Alive)", "threshold_warn": 0.5, "threshold_crit": 0.0, "status": "OK", "server_node": "ems-dispatch-srv"},
        {"metric_key": "queue_backlog_depth", "name": "Patient Bedside Vital Signs Queue", "value": 410.0, "unit": "msgs", "threshold_warn": 10000.0, "threshold_crit": 50000.0, "status": "OK", "server_node": "kafka-medical-vitals"},
        {"metric_key": "ssl_cert_days", "name": "Telemedicine Video Gateway TLS Validity", "value": 75.0, "unit": "days", "threshold_warn": 14.0, "threshold_crit": 5.0, "status": "OK", "server_node": "telemed.lifecare.org"},
        {"metric_key": "cpu_utilization", "name": "Hospital Core Telemetry CPU Load", "value": 24.5, "unit": "%", "threshold_warn": 75.0, "threshold_crit": 90.0, "status": "OK", "server_node": "k8s-med-nodes"},
        {"metric_key": "memory_utilization", "name": "Hospital Core Telemetry RAM Usage", "value": 39.8, "unit": "%", "threshold_warn": 80.0, "threshold_crit": 90.0, "status": "OK", "server_node": "k8s-med-nodes"}
    ],
    "safety_policies": [
        {"policy_key": "kill_switch_active", "policy_name": "Emergency Master Kill Switch", "value": "false", "description": "Instant freeze for all hospital automation threads across medical cluster."},
        {"policy_key": "rate_limit_per_minute", "policy_name": "Action Rate Limiter", "value": "5", "description": "Strict rate limit of max 5 automated actions per minute to prevent loops."},
        {"policy_key": "max_scaling_instances", "policy_name": "Max Hospital Telemetry Pods", "value": "10", "description": "Strict ceiling on hospital Kubernetes pods to prevent network congestion."},
        {"policy_key": "disk_safety_floor_gb", "policy_name": "ICU Storage Safety Floor", "value": "5.0", "description": "Minimum free space buffer below which high-risk clinical escalation is forced."},
        {"policy_key": "tier1_auto_enabled", "policy_name": "Tier 1 Safe Auto-Remediation", "value": "true", "description": "Autonomous execution of non-clinical administrative fixes."},
        {"policy_key": "tier3_requires_approval", "policy_name": "Tier 3 Clinical Human Gate", "value": "true", "description": "Mandatory human physician/SRE approval before touching clinical vitals or medical state."}
    ],
    "runbooks": [
        {
            "runbook_id": "MED-DISK-CRIT",
            "title": "LifeCare Critical: ICU Cardiac Telemetry Waveform Storage Full (99.1% - 180MB Left!)",
            "category": "Medical Storage",
            "target_subsystem": "/var/data/icu/cardiac_ecg",
            "trigger_condition": "Cardiac waveform partition > 99% (Only 180MB remaining!)",
            "safe_action_tier": "Tier 3 (High Risk - Human Approval Required)",
            "blast_radius": "CRITICAL: Continuous ECG waveforms for 42 intensive-care patients.",
            "judgment_rules": "IF cardiac waveform partition is at 99.1%, deleting files destroys clinical diagnostic evidence! Safely sync older records to HIPAA-compliant medical cold storage with human sign-off.",
            "remediation_command": "aws s3 sync /var/data/icu/cardiac_ecg/archive/ s3://lifecare-hipaa-cold/ && rm -f /var/data/icu/cardiac_ecg/archive/*.dat",
            "rollback_command": "aws s3 sync s3://lifecare-hipaa-cold/ /var/data/icu/cardiac_ecg/archive/ || true",
            "verification_check": "df -h /var/data/icu/cardiac_ecg | awk 'NR==2 {gsub(\"%\", \"\"); if ($5 < 85) print \"PASS\"; else print \"FAIL\"}'",
            "documentation": "Preserves continuous patient ECG clinical records under strict HIPAA compliance."
        },
        {
            "runbook_id": "MED-DISK-WARN",
            "title": "LifeCare Warning: Radiology PACS X-Ray Image Preview Cache High (87.6%)",
            "category": "Medical Storage",
            "target_subsystem": "/var/cache/xray_pacs",
            "trigger_condition": "Radiology cache usage > 85%",
            "safe_action_tier": "Tier 1 (Low Risk - Safe Auto)",
            "blast_radius": "LOW: Local PACS preview image cache only. Zero primary medical record risk.",
            "judgment_rules": "IF radiology cache exceeds 85%, purge cached DICOM preview images older than 72h. Primary hospital archive remains intact. Reclaims 45 GB.",
            "remediation_command": "find /var/cache/xray_pacs/ -type f -mtime +3 -delete && systemctl reload dcm4chee.service",
            "rollback_command": "echo 'ROLLBACK_DICOM_PREVIEWS'",
            "verification_check": "df -h /var/cache/xray_pacs | awk 'NR==2 {gsub(\"%\", \"\"); if ($5 < 75) print \"PASS\"; else print \"FAIL\"}'",
            "documentation": "Purges temporary PACS preview images without affecting master patient X-rays."
        },
        {
            "runbook_id": "MED-DISK-UNC",
            "title": "LifeCare Uncritical: Nurse Shift Log & Attendance Scratch Hygiene (48.2%)",
            "category": "Medical Hygiene",
            "target_subsystem": "/tmp/nurse_shifts",
            "trigger_condition": "Off-peak schedule OR disk between 40% and 55%",
            "safe_action_tier": "Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)",
            "blast_radius": "ZERO (0%): Temporary administrative nurse attendance scratch files.",
            "judgment_rules": "IF disk utilization is non-critical (48.2%), purge stale nurse attendance scratch files older than 14 days silently without waking hospital staff.",
            "remediation_command": "find /tmp/nurse_shifts -type f -name '*.tmp' -mtime +14 -delete",
            "rollback_command": "touch /tmp/nurse_shifts/.maintenance_complete",
            "verification_check": "df -h /tmp/nurse_shifts | awk 'NR==2 {print \"PASS_DISK_HEALTHY\"}'",
            "documentation": "Routine administrative scratch cleanup with zero clinical impact."
        },
        {
            "runbook_id": "MED-WORKER-CRIT",
            "title": "LifeCare Critical: Emergency Ambulance Dispatch Service Threadlock (18 Active 911 Calls!)",
            "category": "Medical EMS",
            "target_subsystem": "ems-dispatch-srv",
            "trigger_condition": "EMS dispatch worker locked with > 10 active ambulance dispatches",
            "safe_action_tier": "Tier 3 (High Risk - Human Approval Required)",
            "blast_radius": "CRITICAL: 18 live emergency ambulance response routes.",
            "judgment_rules": "IF EMS dispatch worker is locked with 18 incoming ambulance calls, DO NOT kill worker process (prevents lost ambulance dispatches). Human operator sign-off required to failover to backup radio relay before restart.",
            "remediation_command": "python3 /opt/lifecare/scripts/failover_ems_radio_relay.py && systemctl restart ems-dispatch-srv.service",
            "rollback_command": "systemctl restart ems-dispatch-srv.service",
            "verification_check": "systemctl is-active ems-dispatch-srv.service",
            "documentation": "Guarantees continuous 911 emergency ambulance dispatch routing."
        },
        {
            "runbook_id": "MED-WORKER-WARN",
            "title": "LifeCare Warning: Hospital Pharmacy Medication Restock Sync Stalled (320s)",
            "category": "Medical Pharmacy",
            "target_subsystem": "pharmacy-sync-02",
            "trigger_condition": "Worker heartbeat missed for > 300s (Supplier wholesale API timeout)",
            "safe_action_tier": "Tier 1 (Low Risk - Safe Auto)",
            "blast_radius": "LOW: Non-urgent medication restock inventory sync. Zero bedside patient risk.",
            "judgment_rules": "IF worker is hung waiting on supplier wholesale API, perform graceful SIGTERM restart with automatic inventory message requeue.",
            "remediation_command": "systemctl restart celery-worker@pharmacy-sync-02.service",
            "rollback_command": "systemctl restart celery-worker@pharmacy-sync-02-fallback.service",
            "verification_check": "systemctl is-active celery-worker@pharmacy-sync-02.service",
            "documentation": "Restores hospital pharmacy inventory background sync safely."
        },
        {
            "runbook_id": "MED-WORKER-UNC",
            "title": "LifeCare Uncritical: Patient Discharge Document PDF Generator Soft Recycle (8,000 PDFs)",
            "category": "Medical Compute",
            "target_subsystem": "pdf-gen-pool-03",
            "trigger_condition": "Worker processed > 5,000 PDFs (Worker Healthy)",
            "safe_action_tier": "Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)",
            "blast_radius": "ZERO (0%): Soft reload occurs between discharge document batches.",
            "judgment_rules": "IF PDF generator worker is healthy but has minor heap fragmentation, trigger graceful reload during off-peak night lull.",
            "remediation_command": "systemctl reload-or-restart celery-worker@pdf-gen-pool-03.service",
            "rollback_command": "systemctl status celery-worker@pdf-gen-pool-03.service",
            "verification_check": "systemctl is-active celery-worker@pdf-gen-pool-03.service",
            "documentation": "Compacts memory on hospital discharge document generation daemons."
        },
        {
            "runbook_id": "MED-QUEUE-CRIT",
            "title": "LifeCare Critical: Bedside Vital Signs Alert Stream Crash Loop (96,000 msgs - 94.1% Err)",
            "category": "Medical Vitals",
            "target_subsystem": "vitals.patient.telemetry",
            "trigger_condition": "Queue backlog > 50,000 and consumer error rate > 80%",
            "safe_action_tier": "Tier 3 (High Risk - Human Approval Required)",
            "blast_radius": "HIGH: Bedside vital signs monitoring telemetry and false alarm suppression.",
            "judgment_rules": "IF consumer error rate is > 80% (malformed pulse oximeter firmware telemetry crashing pods), DO NOT scale pods; isolate bad offset to Medical Quarantine Queue with human sign-off.",
            "remediation_command": "kafka-consumer-groups --bootstrap-server kafka:9092 --group bedside-vitals --topic vitals.patient.telemetry --reset-offsets --to-offset 302194 --execute",
            "rollback_command": "kafka-consumer-groups --bootstrap-server kafka:9092 --group bedside-vitals --topic vitals.patient.telemetry --reset-offsets --to-offset 302193 --execute",
            "verification_check": "echo PASS_DLQ_ROUTED",
            "documentation": "Quarantines malformed pulse oximeter telemetry to restore vital signs alerting."
        },
        {
            "runbook_id": "MED-QUEUE-WARN",
            "title": "LifeCare Warning: Outpatient Blood Lab Results Notification Backlog (19,800 msgs)",
            "category": "Medical Labs",
            "target_subsystem": "lab.results.broadcast",
            "trigger_condition": "Queue backlog > 15,000 and error rate < 0.1%",
            "safe_action_tier": "Tier 2 (Guarded Auto - Within Policy Limits)",
            "blast_radius": "MEDIUM: Outpatient notification pods. Capped at max 10 pods.",
            "judgment_rules": "IF error rate < 0.1% (morning blood test rush), autoscale consumer pods from 2 to 6 pods within policy limit 10.",
            "remediation_command": "kubectl scale deployment/order-consumer --replicas=6 --namespace=orders",
            "rollback_command": "kubectl scale deployment/order-consumer --replicas=2 --namespace=orders",
            "verification_check": "kubectl get deployment/order-consumer -o jsonpath='{.status.readyReplicas}'",
            "documentation": "Autoscales outpatient lab notification consumers to deliver test results."
        },
        {
            "runbook_id": "MED-QUEUE-UNC",
            "title": "LifeCare Uncritical: Hospital Cafeteria Patient Meal Order Ripple (410 msgs)",
            "category": "Medical Queues",
            "target_subsystem": "dietary.meal_orders",
            "trigger_condition": "Backlog between 300 and 800 messages (Minor Transient Ripple)",
            "safe_action_tier": "Tier 1 (Uncritical - Silent Safe Auto)",
            "blast_radius": "LOW (< 5%): Spins up 1 standby consumer container.",
            "judgment_rules": "IF backlog has minor morning ripple (410 msgs), activate 1 standby pod to maintain sub-150ms processing SLA.",
            "remediation_command": "kubectl scale deployment/order-consumer --replicas=4 --namespace=orders",
            "rollback_command": "kubectl scale deployment/order-consumer --replicas=3 --namespace=orders",
            "verification_check": "kubectl get deployment/order-consumer -o jsonpath='{.status.readyReplicas}'",
            "documentation": "Smooths out hospital dietary meal order notifications silently."
        },
        {
            "runbook_id": "MED-SSL-CRIT",
            "title": "LifeCare Critical: Telemedicine Video Gateway Root CA Revocation (5 Hours Left!)",
            "category": "Medical Security",
            "target_subsystem": "telemed.lifecare.org",
            "trigger_condition": "Certificate validity < 12 hours and CA revoked upstream",
            "safe_action_tier": "Tier 3 (High Risk - Human Approval Required)",
            "blast_radius": "CRITICAL: Live remote doctor video consultations + HIPAA compliance.",
            "judgment_rules": "IF intermediate CA is revoked upstream, automated ACME renewal cannot succeed. Escalate immediately to Hospital Chief Information Security Officer (CISO).",
            "remediation_command": "update-ca-certificates --fresh && nginx -s reload",
            "rollback_command": "cp /etc/ssl/backup/last_known_good.crt /etc/ssl/certs/ && nginx -s reload",
            "verification_check": "openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/telemed.lifecare.org.crt",
            "documentation": "Protects live telemedicine remote patient video consultations from disconnection."
        },
        {
            "runbook_id": "MED-SSL-WARN",
            "title": "LifeCare Warning: Patient Health Records Portal TLS Expiring (4.2 Days)",
            "category": "Medical Ingress",
            "target_subsystem": "portal.lifecare.org",
            "trigger_condition": "Certificate validity <= 5 days (ACME HTTP-01 valid)",
            "safe_action_tier": "Tier 1 (Low Risk - Safe Auto)",
            "blast_radius": "LOW: Public patient records portal. Seamless configuration reload.",
            "judgment_rules": "IF certificate is within 5 days of expiry and DNS records valid, trigger automated certbot renewal and seamless nginx reload.",
            "remediation_command": "certbot renew --cert-name portal.lifecare.org --quiet && nginx -s reload",
            "rollback_command": "cp /etc/ssl/backup/last_known_good.crt /etc/ssl/certs/ && nginx -s reload",
            "verification_check": "openssl x509 -checkend 604800 -noout -in /etc/ssl/certs/portal.lifecare.org.crt",
            "documentation": "Automated seamless TLS rotation for patient records portal."
        },
        {
            "runbook_id": "MED-SSL-UNC",
            "title": "LifeCare Uncritical: Medical IoT Device Encrypted Gateway Health Audit (75.0 Days)",
            "category": "Medical Auditing",
            "target_subsystem": "devices.lifecare.internal",
            "trigger_condition": "Scheduled audit OR certificate validity at 75 days remaining",
            "safe_action_tier": "Tier 0 / Tier 1 (Uncritical - Preventive Health Audit)",
            "blast_radius": "ZERO (0%): Read-only cryptographic handshake validation probe.",
            "judgment_rules": "IF certificate validity is healthy (75 days remaining), execute routine cryptographic trust check. No human action required.",
            "remediation_command": "openssl s_client -servername devices.lifecare.internal -connect 127.0.0.1:443 </dev/null 2>/dev/null | openssl x509 -noout -dates && echo 'AUDIT_VERIFIED_VALID'",
            "rollback_command": "echo 'AUDIT_NOOP'",
            "verification_check": "openssl x509 -checkend 2592000 -noout -in /etc/ssl/certs/devices.lifecare.internal.crt",
            "documentation": "Proactive cryptographic validity audit on hospital medical IoT devices."
        }
    ]
}

# Write JSON files
with open(os.path.join(PROJECT_DIR, "DATASET_ECOMMERCE_QUICKCART.json"), "w", encoding="utf-8") as f:
    json.dump(ecommerce_dataset, f, indent=2)

with open(os.path.join(PROJECT_DIR, "DATASET_HEALTHCARE_LIFECARE.json"), "w", encoding="utf-8") as f:
    json.dump(healthcare_dataset, f, indent=2)

print("Generated DATASET_ECOMMERCE_QUICKCART.json and DATASET_HEALTHCARE_LIFECARE.json!")
